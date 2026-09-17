"""Core bersama untuk analisis dan eksperimen Q-Learning rute lari loop 5 km.

Jangan menduplikasi aturan environment di notebook scenario. Semua notebook memanggil
modul ini agar data OSM, reward, action mask, dan metrik selalu konsisten.
"""

from __future__ import annotations

import ast
import re
from collections import defaultdict
from pathlib import Path
from typing import Any

import folium
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import osmnx as ox
import pandas as pd
from IPython.display import display
from pyproj import Transformer


# ============================================================
# A. KONFIGURASI PROYEK, DATA OSM, DAN TRAINING
# ============================================================

PROJECT_DIR = Path(__file__).resolve().parent
DATA_DIR = PROJECT_DIR / "data_osm_5km"
GRAPH_PATH = DATA_DIR / "graf_jalan_kaki_5km.graphml"
RESULT_DIR = PROJECT_DIR / "hasil_bab_4" / "training_qlearning_5km"

START_LAT = -7.282187
START_LON = 112.709282
TARGET_DISTANCE_M = 5_000
DISTANCE_TOLERANCE = 0.10
MIN_DISTANCE_M = TARGET_DISTANCE_M * (1 - DISTANCE_TOLERANCE)
MAX_DISTANCE_M = TARGET_DISTANCE_M * (1 + DISTANCE_TOLERANCE)
DOWNLOAD_RADIUS_M = 3_025

ALLOW_REVISIT = True
REVISIT_AFTER_RATIO = 0.50
MAX_NODE_VISITS = 2
PROGRESS_BINS = 16

NEUTRAL_COMFORT_SCORE = 0.50
RETURN_PHASE_RATIO = 0.50
RETURN_REWARD_SCALE = 0.40
# Penalti ringan apabila, sebelum fase pulang, sebuah action justru membuat
# posisi geometris agen lebih dekat ke start.
OUTWARD_PENALTY_SCALE = 0.40
SUCCESS_BONUS = 80.0
OVER_DISTANCE_PENALTY = -50.0
NO_ACTION_PENALTY = -45.0
EARLY_RETURN_PENALTY = -45.0
STEP_LIMIT_PENALTY = -40.0
REVISIT_PENALTY = -8.0

ALPHA = 0.15
GAMMA = 0.95
EPSILON_START = 1.00
EPSILON_END = 0.05
EPISODES = 2_500
MAX_STEPS_PER_EPISODE = 220
SEEDS = (0, 1, 2, 3, 4)
ROLLING_WINDOW = 50

TERMINATION_REASONS = (
    "success",
    "over_distance",
    "no_available_action",
    "early_return",
    "step_limit",
)

# Kolom yang menjadi hasil evaluasi utama pada BAB IV. Kolom diagnosis seperti
# ukuran Q-table dan jumlah revisit tetap dapat dipakai secara internal, tetapi
# tidak ditampilkan sebagai metrik pembanding utama antar-scenario.
EVALUATION_RESULT_COLUMNS = (
    "scenario",
    "seed",
    "is_loop",
    "total_distance_m",
    "absolute_distance_error_m",
    "total_reward",
    "mean_comfort",
    "return_progress_ratio",
    "distance_to_start_at_end_m",
    "termination_reason",
)

# Kolom yang ditampilkan secara vertikal di notebook. Scenario tidak diperlukan
# di sini karena satu notebook hanya menjalankan satu scenario.
EVALUATION_DISPLAY_COLUMNS = EVALUATION_RESULT_COLUMNS[2:]


def configure_osmnx() -> None:
    """Menetapkan cache dan tag OSM agar seluruh notebook memakai data seragam."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    ox.settings.use_cache = True
    ox.settings.cache_folder = str(DATA_DIR / "cache")
    ox.settings.log_console = False
    ox.settings.useful_tags_way = list(set(ox.settings.useful_tags_way + ["surface"]))


def get_start_node(graph: nx.MultiDiGraph) -> int:
    """Melakukan snapping koordinat input pengguna ke node terdekat pada graf."""
    to_projected = Transformer.from_crs(
        "EPSG:4326", graph.graph["crs"], always_xy=True
    )
    start_x, start_y = to_projected.transform(START_LON, START_LAT)
    return int(ox.distance.nearest_nodes(graph, X=start_x, Y=start_y))


def load_or_download_graph(force_download: bool = False):
    """Memuat GraphML yang sama atau mengunduhnya bila belum tersedia.

    Returns:
        graph, start_node, graph_path, downloaded_now
    """
    configure_osmnx()
    if GRAPH_PATH.exists() and not force_download:
        graph = ox.io.load_graphml(GRAPH_PATH)
        return graph, get_start_node(graph), GRAPH_PATH, False

    graph_wgs84 = ox.graph_from_point(
        center_point=(START_LAT, START_LON),
        dist=DOWNLOAD_RADIUS_M,
        dist_type="bbox",
        network_type="walk",
        simplify=True,
        retain_all=False,
        truncate_by_edge=True,
    )
    graph = ox.project_graph(graph_wgs84)
    ox.io.save_graphml(graph, filepath=GRAPH_PATH)
    return graph, get_start_node(graph), GRAPH_PATH, True


# ============================================================
# B. COMFORT SCORE PADA EDGE
# ============================================================

HIGHWAY_SCORES = {
    "footway": 0.95, "pedestrian": 0.95, "path": 0.85,
    "living_street": 0.80, "residential": 0.75, "service": 0.60,
    "unclassified": 0.55, "tertiary": 0.45, "tertiary_link": 0.45,
    "secondary": 0.35, "secondary_link": 0.35, "track": 0.35,
    "primary": 0.20, "primary_link": 0.20, "trunk": 0.10,
    "trunk_link": 0.10, "steps": 0.10,
}
SURFACE_SCORES = {
    "asphalt": 1.00, "concrete": 0.90, "paved": 0.90,
    "paving_stones": 0.75, "sett": 0.65, "compacted": 0.55,
    "fine_gravel": 0.45, "gravel": 0.30, "dirt": 0.25,
    "ground": 0.20, "unpaved": 0.20,
}
WEIGHT_HIGHWAY = 0.55
WEIGHT_SURFACE = 0.30
WEIGHT_WIDTH = 0.15
WIDTH_MIN_M = 1.0
WIDTH_MAX_M = 5.0
WIDTH_MIN_SCORE = 0.25
WIDTH_MAX_SCORE = 1.00


def is_missing(value: Any) -> bool:
    return value is None or value is pd.NA or (
        isinstance(value, float) and np.isnan(value)
    )


def osm_values(value: Any) -> list[str]:
    """Mengubah tag tunggal atau list hasil simplify menjadi list string."""
    if is_missing(value):
        return []
    if isinstance(value, str):
        text = value.strip()
        if text.startswith("[") and text.endswith("]"):
            try:
                parsed = ast.literal_eval(text)
                if isinstance(parsed, (list, tuple, set)):
                    return [str(item).strip().lower() for item in parsed]
            except (ValueError, SyntaxError):
                pass
        return [text.lower()]
    if isinstance(value, (list, tuple, set)):
        return [str(item).strip().lower() for item in value]
    return [str(value).strip().lower()]


def parse_width_m(value: Any) -> float | None:
    if is_missing(value) or isinstance(value, (list, tuple, set)):
        return None
    text = str(value).strip().lower().replace(",", ".")
    if text.startswith("[") or ";" in text:
        return None
    match = re.fullmatch(
        r"(\d+(?:\.\d+)?)\s*(?:m|meter|metre|meters|metres)?", text
    )
    if match is None:
        return None
    width_m = float(match.group(1))
    return width_m if width_m > 0 else None


def conservative_score(value: Any, score_map: dict[str, float], neutral: float) -> float:
    values = osm_values(value)
    return neutral if not values else min(score_map.get(item, neutral) for item in values)


def width_score(value: Any) -> float:
    width_m = parse_width_m(value)
    if width_m is None:
        return NEUTRAL_COMFORT_SCORE
    proportion = np.clip((width_m - WIDTH_MIN_M) / (WIDTH_MAX_M - WIDTH_MIN_M), 0.0, 1.0)
    return float(WIDTH_MIN_SCORE + proportion * (WIDTH_MAX_SCORE - WIDTH_MIN_SCORE))


def add_comfort_scores(graph: nx.MultiDiGraph) -> None:
    """Menambahkan komponen dan comfort score ke semua edge."""
    for _, _, _, data in graph.edges(keys=True, data=True):
        highway_score = conservative_score(
            data.get("highway"), HIGHWAY_SCORES, NEUTRAL_COMFORT_SCORE
        )
        surface_score = conservative_score(
            data.get("surface"), SURFACE_SCORES, NEUTRAL_COMFORT_SCORE
        )
        edge_width_score = width_score(data.get("width"))
        comfort = (
            WEIGHT_HIGHWAY * highway_score
            + WEIGHT_SURFACE * surface_score
            + WEIGHT_WIDTH * edge_width_score
        )
        data["highway_score"] = float(highway_score)
        data["surface_score"] = float(surface_score)
        data["width_score"] = float(edge_width_score)
        data["comfort_score"] = float(np.clip(comfort, 0.0, 1.0))


# ============================================================
# C. ACTION, STATE, DAN ENVIRONMENT
# ============================================================

class EdgeAction:
    """Satu action adalah edge spesifik dengan node tujuan dan key tertentu."""

    def __init__(
        self,
        next_node: int,
        key: Any,
        length_m: float,
        comfort_score: float,
        data: dict,
    ):
        self.next_node = next_node
        self.key = key
        self.length_m = length_m
        self.comfort_score = comfort_score
        self.data = data

    def get_action_id(self) -> tuple[int, Any]:
        return (self.next_node, self.key)


def build_actions(graph: nx.MultiDiGraph) -> dict[int, list[EdgeAction]]:
    """Menyimpan semua edge keluar tanpa membuang edge paralel."""
    actions_by_node: dict[int, list[EdgeAction]] = defaultdict(list)
    for u, v, key, data in graph.edges(keys=True, data=True):
        length_m = float(data.get("length", 0.0))
        if length_m > 0:
            actions_by_node[int(u)].append(
                EdgeAction(
                    int(v),
                    key,
                    length_m,
                    float(data["comfort_score"]),
                    data,
                )
            )
    for node in actions_by_node:
        actions_by_node[node].sort(key=lambda action: (action.next_node, str(action.key)))
    return actions_by_node


def build_state(environment, scenario: str) -> tuple:
    """Membentuk state A-C tanpa mengubah aturan environment."""
    if scenario == "A":
        return (environment.current_node,)
    if scenario == "B":
        return (environment.current_node, environment.progress_bin())
    if scenario == "C":
        return (
            environment.current_node,
            environment.previous_node,
            environment.progress_bin(),
        )
    raise ValueError(f"Scenario tidak dikenal: {scenario}")


class RunningRouteEnvironment:
    """Environment Q-Learning loop 5 km yang dibangun dari scratch."""

    def __init__(
        self,
        start_node: int,
        scenario: str,
        actions_by_node: dict[int, list[EdgeAction]],
        node_xy: dict[int, tuple[float, float]],
    ):
        self.start_node = int(start_node)
        self.scenario = scenario
        self.actions_by_node = actions_by_node
        self.node_xy = node_xy
        self.reset()

    def reset(self) -> tuple:
        self.current_node = self.start_node
        self.previous_node = -1
        self.total_distance_m = 0.0
        self.step_count = 0
        self.node_visits = defaultdict(int, {self.start_node: 1})
        self.revisit_count = 0
        self.path_nodes = [self.start_node]
        self.path_actions: list[tuple[int, EdgeAction]] = []
        self.return_phase_steps = 0
        self.return_progress_steps = 0
        # Bernilai True bila episode ini pernah berada pada node yang memiliki
        # edge legal langsung ke start dengan total jarak 4,5--5,5 km.
        # Ini metrik diagnosis; bukan aturan untuk memaksa agen memilih edge itu.
        self.closing_action_was_available = False
        self.done = False
        self.is_loop = False
        self.termination_reason = "running"
        return build_state(self, self.scenario)

    def progress_bin(self) -> int:
        raw_bin = int(self.total_distance_m / MAX_DISTANCE_M * PROGRESS_BINS)
        return min(PROGRESS_BINS - 1, max(0, raw_bin))

    def straight_distance_to_start(self, node: int) -> float:
        x, y = self.node_xy[node]
        start_x, start_y = self.node_xy[self.start_node]
        return float(np.hypot(x - start_x, y - start_y))

    def available_actions(self) -> list[EdgeAction]:
        """Menghasilkan action legal (action mask) untuk posisi agen saat ini.

        Semua edge yang keluar dari ``current_node`` belum tentu boleh dipilih.
        Fungsi ini menyaring edge tersebut menjadi tiga kelompok:

        - fresh_actions: menuju node yang belum pernah dikunjungi;
        - closing_actions: langsung kembali ke start dengan jarak loop yang valid;
        - revisit_actions: menuju node lama, tetapi hanya sebagai fallback di
          bagian akhir rute.

        Daftar hasil fungsi ini adalah satu-satunya daftar action yang dapat
        dipilih oleh epsilon-greedy. Jadi action mask adalah aturan legalitas,
        bukan reward dan bukan policy pemilihan action.
        """
        fresh_actions, closing_actions, revisit_actions = [], [], []

        # Ambil seluruh edge spesifik dari node sekarang. Pada MultiDiGraph,
        # dua edge dapat menuju node tujuan yang sama tetapi memiliki ``key``
        # berbeda; keduanya tetap diperiksa sebagai action yang berbeda.
        for action in self.actions_by_node.get(self.current_node, []):
            next_node = action.next_node

            # Perkiraan total jarak bila agen memilih edge ini. Nilai ini harus
            # diperiksa sebelum action dipilih, khususnya untuk closing action.
            next_distance = self.total_distance_m + action.length_m

            # Edge yang menuju start hanya boleh ditawarkan bila edge tersebut
            # benar-benar dapat menyelesaikan loop 4,5--5,5 km. Bila kembali
            # lebih awal atau setelah batas maksimum, edge ke start ditutup.
            # ``continue`` penting agar start tidak ikut diperlakukan sebagai
            # fresh action ataupun revisit action.
            if next_node == self.start_node:
                if (
                    self.current_node != self.start_node
                    and MIN_DISTANCE_M <= next_distance <= MAX_DISTANCE_M
                ):
                    closing_actions.append(action)
                continue

            # Prioritas utama: perluas rute ke node yang belum pernah dikunjungi.
            # Ini mengurangi putar-balik kecil dan membuat agen mengeksplorasi
            # graf sebelum memakai node yang sama lagi.
            if self.node_visits[next_node] == 0:
                fresh_actions.append(action)
                continue

            # Revisit bukan action normal. Ia baru diizinkan setelah agen sudah
            # menempuh 50% target (2,5 km) dan node tujuan belum dikunjungi dua
            # kali. Dengan syarat ini revisit dapat membantu agen pulang saat
            # fresh action habis, tetapi tidak bebas berputar sejak awal rute.
            if (
                ALLOW_REVISIT
                and self.total_distance_m >= REVISIT_AFTER_RATIO * TARGET_DISTANCE_M
                and self.node_visits[next_node] < MAX_NODE_VISITS
            ):
                revisit_actions.append(action)

        # Jika list tidak kosong, agen setidaknya pernah mempunyai kesempatan
        # legal untuk menyelesaikan loop pada decision point ini. Flag hanya
        # berubah False -> True dan di-reset saat episode baru dimulai, sehingga
        # pemanggilan available_actions() berulang tidak menghitung ganda.
        if closing_actions:
            self.closing_action_was_available = True

        # Jika masih ada node baru, agen boleh memilih fresh, revisit yang
        # sudah legal, atau closing action. Sebelum 50% target,
        # ``revisit_actions`` pasti kosong; setelahnya, agen tidak lagi dipaksa
        # terus menjelajah jalan baru dan dapat memilih jalur lama untuk pulang.
        if fresh_actions:
            return fresh_actions + revisit_actions + closing_actions

        # revisit_actions hanya dapat terisi jika ALLOW_REVISIT=True serta
        # seluruh syarat revisit terpenuhi di loop sebelumnya. Karena itu tidak
        # perlu memeriksa ALLOW_REVISIT lagi pada tahap pengembalian ini.
        if len(revisit_actions) > 0:
            return revisit_actions + closing_actions

        # Jika fresh dan revisit sama-sama tidak ada, satu-satunya action legal
        # yang mungkin tersisa adalah menutup loop. Bila list ini juga kosong,
        # caller akan menjalankan terminasi ``no_available_action``.
        return closing_actions

    def stop_without_action(self) -> tuple[tuple, float, bool, dict]:
        self.done = True
        self.termination_reason = "no_available_action"
        return build_state(self, self.scenario), NO_ACTION_PENALTY, True, self.info()

    def step(self, action: EdgeAction) -> tuple[tuple, float, bool, dict]:
        if self.done:
            raise RuntimeError("Episode selesai. Panggil reset() sebelum step().")

        legal_ids = {candidate.get_action_id() for candidate in self.available_actions()}
        if action.get_action_id() not in legal_ids:
            raise ValueError("Action tidak legal untuk state environment saat ini.")

        current_node = self.current_node
        next_node = action.next_node
        distance_before = self.straight_distance_to_start(current_node)
        # Fase awal ditentukan sebelum action dijalankan. Dengan demikian edge
        # yang mulai pada 2.490 m tetap diperlakukan sebagai bagian fase awal,
        # meskipun setelah edge jarak rute melewati 2.500 m.
        in_outward_phase = (
            self.total_distance_m < RETURN_PHASE_RATIO * TARGET_DISTANCE_M
        )
        is_revisit = self.node_visits[next_node] > 0

        self.total_distance_m += action.length_m
        self.previous_node = current_node
        self.current_node = next_node
        self.path_nodes.append(next_node)
        self.path_actions.append((current_node, action))
        self.node_visits[next_node] += 1
        self.step_count += 1

        distance_after = self.straight_distance_to_start(next_node)
        in_return_phase = self.total_distance_m >= RETURN_PHASE_RATIO * TARGET_DISTANCE_M
        if in_return_phase:
            self.return_phase_steps += 1
            if distance_after < distance_before:
                self.return_progress_steps += 1

        reward = (action.comfort_score - NEUTRAL_COMFORT_SCORE) * (
            action.length_m / 100.0
        )

        if is_revisit and next_node != self.start_node:
            self.revisit_count += 1
            reward += REVISIT_PENALTY

        if next_node == self.start_node and MIN_DISTANCE_M <= self.total_distance_m <= MAX_DISTANCE_M:
            self.done = True
            self.is_loop = True
            self.termination_reason = "success"
            reward += SUCCESS_BONUS
        elif next_node == self.start_node:
            self.done = True
            self.termination_reason = "early_return"
            reward += EARLY_RETURN_PENALTY
        elif self.total_distance_m > MAX_DISTANCE_M:
            self.done = True
            self.termination_reason = "over_distance"
            reward += OVER_DISTANCE_PENALTY
        elif self.step_count >= MAX_STEPS_PER_EPISODE:
            self.done = True
            self.termination_reason = "step_limit"
            reward += STEP_LIMIT_PENALTY
        elif in_outward_phase and distance_after < distance_before:
            # Pada fase awal, agen tidak dilarang bergerak mendekati start,
            # tetapi menerima penalti proporsional terhadap besar gerakannya.
            # Ini menyeimbangkan reward comfort tinggi yang dapat menarik agen
            # kembali ke area start terlalu cepat.
            reward -= OUTWARD_PENALTY_SCALE * (
                distance_before - distance_after
            ) / 100.0
        elif in_return_phase:
            reward += RETURN_REWARD_SCALE * (distance_before - distance_after) / 100.0

        info = self.info()
        info["is_revisit"] = is_revisit
        info["edge_comfort"] = action.comfort_score
        info["edge_length_m"] = action.length_m
        return build_state(self, self.scenario), float(reward), self.done, info

    def info(self) -> dict:
        return {
            "is_loop": self.is_loop,
            "termination_reason": self.termination_reason,
            "total_distance_m": self.total_distance_m,
            "step_count": self.step_count,
            "revisit_count": self.revisit_count,
            "distance_to_start_at_end_m": self.straight_distance_to_start(
                self.current_node
            ),
            "return_phase_steps": self.return_phase_steps,
            "return_progress_steps": self.return_progress_steps,
        }


# ============================================================
# D. POLICY, TRAINING, EVALUASI, DAN METRIK DIAGNOSIS
# ============================================================

def choose_action(q_table, state: tuple, actions: list[EdgeAction], rng, epsilon: float):
    if rng.random() < epsilon:
        return actions[int(rng.integers(len(actions)))]
    values = np.array([
        q_table[state].get(action.get_action_id(), 0.0) for action in actions
    ])
    best_indices = np.flatnonzero(np.isclose(values, values.max()))
    return actions[int(rng.choice(best_indices))]


def route_metrics(environment: RunningRouteEnvironment, total_reward: float) -> dict:
    edge_length = sum(action.length_m for _, action in environment.path_actions)
    mean_comfort = (
        sum(
            action.comfort_score * action.length_m
            for _, action in environment.path_actions
        ) / edge_length
        if edge_length
        else np.nan
    )
    unique_edges = len({
        (u, action.next_node, action.key)
        for u, action in environment.path_actions
    })
    intermediate_nodes = environment.path_nodes[1:-1]
    return {
        "is_loop": environment.is_loop,
        "termination_reason": environment.termination_reason,
        "total_distance_m": environment.total_distance_m,
        "distance_km": environment.total_distance_m / 1000.0,
        "absolute_distance_error_m": abs(
            environment.total_distance_m - TARGET_DISTANCE_M
        ),
        "overshoot_m": max(0.0, environment.total_distance_m - MAX_DISTANCE_M),
        "distance_to_start_at_end_m": environment.straight_distance_to_start(
            environment.current_node
        ),
        "return_progress_ratio": (
            environment.return_progress_steps / environment.return_phase_steps
            if environment.return_phase_steps
            else np.nan
        ),
        "return_phase_steps": environment.return_phase_steps,
        "return_progress_steps": environment.return_progress_steps,
        "closing_action_was_available": environment.closing_action_was_available,
        "steps": environment.step_count,
        "total_reward": total_reward,
        "mean_comfort": mean_comfort,
        "revisit_count": environment.revisit_count,
        "repeated_intermediate_nodes": len(intermediate_nodes) - len(
            set(intermediate_nodes)
        ),
        "unique_edge_ratio": (
            unique_edges / len(environment.path_actions)
            if environment.path_actions
            else 0.0
        ),
    }


def train_q_learning(
    scenario: str,
    seed: int,
    start_node: int,
    actions_by_node: dict[int, list[EdgeAction]],
    node_xy: dict[int, tuple[float, float]],
):
    environment = RunningRouteEnvironment(
        start_node, scenario, actions_by_node, node_xy
    )
    rng = np.random.default_rng(seed)
    q_table = defaultdict(dict)
    history_rows = []
    for episode in range(EPISODES):
        state = environment.reset()
        epsilon = EPSILON_END + (EPSILON_START - EPSILON_END) * (
            1 - episode / max(1, EPISODES - 1)
        )
        episode_reward = 0.0

        for _ in range(MAX_STEPS_PER_EPISODE):
            actions = environment.available_actions()
            if not actions:
                next_state, stop_reward, done, _ = environment.stop_without_action()
                reward = stop_reward
                episode_reward += stop_reward
                next_actions = []
            else:
                action = choose_action(q_table, state, actions, rng, epsilon)
                next_state, reward, done, _ = environment.step(action)
                episode_reward += reward
                next_actions = [] if done else environment.available_actions()

                if not done and not next_actions:
                    _, stop_reward, done, _ = environment.stop_without_action()
                    reward += stop_reward
                    episode_reward += stop_reward

                future_value = max(
                    (
                        q_table[next_state].get(
                            next_action.get_action_id(), 0.0
                        )
                        for next_action in next_actions
                    ),
                    default=0.0,
                )
                old_value = q_table[state].get(action.get_action_id(), 0.0)
                q_table[state][action.get_action_id()] = old_value + ALPHA * (
                    reward + GAMMA * future_value - old_value
                )

            state = next_state
            if done:
                break

        if not environment.done:
            environment.done = True
            environment.termination_reason = "step_limit"
            episode_reward += STEP_LIMIT_PENALTY

        metrics = route_metrics(environment, episode_reward)
        metrics.update({
            "scenario": scenario,
            "seed": seed,
            "episode": episode + 1,
            "epsilon": epsilon,
            "q_state_count": len(q_table),
        })
        history_rows.append(metrics)

    return q_table, pd.DataFrame(history_rows)


def evaluate_greedy(
    scenario: str,
    q_table,
    seed: int,
    start_node: int,
    actions_by_node: dict[int, list[EdgeAction]],
    node_xy: dict[int, tuple[float, float]],
):
    environment = RunningRouteEnvironment(
        start_node, scenario, actions_by_node, node_xy
    )
    rng = np.random.default_rng(seed + 100_000)
    state = environment.reset()
    total_reward = 0.0

    for _ in range(MAX_STEPS_PER_EPISODE):
        actions = environment.available_actions()
        if not actions:
            _, reward, _, _ = environment.stop_without_action()
            total_reward += reward
            break
        action = choose_action(q_table, state, actions, rng, epsilon=0.0)
        state, reward, done, _ = environment.step(action)
        total_reward += reward
        if done:
            break
    else:
        environment.done = True
        environment.termination_reason = "step_limit"
        total_reward += STEP_LIMIT_PENALTY

    return environment, route_metrics(environment, total_reward)


def termination_rate_table(results_df: pd.DataFrame) -> pd.DataFrame:
    """Menghitung rate semua jenis terminasi dari training atau evaluasi."""
    rows = []
    total = len(results_df)
    for reason in TERMINATION_REASONS:
        count = int((results_df["termination_reason"] == reason).sum())
        rows.append({
            "termination_reason": reason,
            "count": count,
            "termination_rate": count / total if total else 0.0,
            "termination_rate_percent": 100 * count / total if total else 0.0,
        })
    return pd.DataFrame(rows)


def diagnosis_summary(metrics_df: pd.DataFrame) -> pd.DataFrame:
    """Ringkasan metrik baru untuk membedakan kegagalan antar scenario."""
    return pd.DataFrame([
        {
            "scenario": metrics_df["scenario"].iloc[0],
            "distance_to_start_at_end_mean_m": metrics_df[
                "distance_to_start_at_end_m"
            ].mean(),
            "return_progress_ratio_mean": metrics_df[
                "return_progress_ratio"
            ].mean(),
            "closing_action_available_rate": metrics_df[
                "closing_action_was_available"
            ].mean(),
            "q_state_count_mean": metrics_df["q_state_count"].mean(),
        }
    ])


# ============================================================
# E. GRAFIK DAN PETA INTERAKTIF
# ============================================================

def plot_training_charts(history_df: pd.DataFrame, scenario: str) -> Path:
    mean_history = history_df.groupby("episode", as_index=False).agg(
        success_rate=("is_loop", "mean"),
        mean_reward=("total_reward", "mean"),
        mean_distance_km=("distance_km", "mean"),
        mean_comfort=("mean_comfort", "mean"),
        mean_q_state_count=("q_state_count", "mean"),
        mean_epsilon=("epsilon", "mean"),
    )
    rolling = (
        mean_history.set_index("episode")
        .rolling(ROLLING_WINDOW, min_periods=1)
        .mean()
        .reset_index()
    )

    figure, axes = plt.subplots(3, 2, figsize=(14, 13))
    figure.suptitle(
        f"Training Q-Learning Scenario {scenario} - rata-rata {ROLLING_WINDOW} episode",
        fontsize=14,
        fontweight="bold",
    )

    axes[0, 0].plot(rolling["episode"], rolling["success_rate"], color="#16A34A")
    axes[0, 0].set(
        title=f"Rata-rata Keberhasilan {ROLLING_WINDOW} Episode Terakhir",
        xlabel="Episode",
        ylabel="Proporsi is_loop",
        ylim=(-0.02, 1.02),
    )

    axes[0, 1].plot(rolling["episode"], rolling["mean_reward"], color="#2563EB")
    axes[0, 1].set(
        title=f"Rata-rata Reward {ROLLING_WINDOW} Episode Terakhir",
        xlabel="Episode",
        ylabel="Reward",
    )

    axes[1, 0].plot(rolling["episode"], rolling["mean_distance_km"], color="#7C3AED")
    axes[1, 0].axhline(
        TARGET_DISTANCE_M / 1000, color="black", linestyle="--", label="Target 5 km"
    )
    axes[1, 0].axhline(
        MIN_DISTANCE_M / 1000, color="#9CA3AF", linestyle=":", label="Batas valid"
    )
    axes[1, 0].axhline(MAX_DISTANCE_M / 1000, color="#9CA3AF", linestyle=":")
    axes[1, 0].set(
        title=f"Rata-rata Jarak {ROLLING_WINDOW} Episode Terakhir",
        xlabel="Episode",
        ylabel="Jarak (km)",
    )
    axes[1, 0].legend()

    axes[1, 1].plot(rolling["episode"], rolling["mean_comfort"], color="#F59E0B")
    axes[1, 1].set(
        title=f"Rata-rata Skor Kenyamanan {ROLLING_WINDOW} Episode Terakhir",
        xlabel="Episode",
        ylabel="Comfort score",
        ylim=(0, 1),
    )

    axes[2, 0].plot(rolling["episode"], rolling["mean_q_state_count"], color="#DC2626")
    axes[2, 0].set(
        title="Jumlah State Q-table",
        xlabel="Episode",
        ylabel="Jumlah state",
    )

    axes[2, 1].plot(
        mean_history["episode"], mean_history["mean_epsilon"], color="#0891B2"
    )
    axes[2, 1].set(
        title="Nilai Epsilon per Episode",
        xlabel="Episode",
        ylabel="Epsilon",
        ylim=(0, 1.05),
    )

    for axis in axes.flat:
        axis.grid(alpha=0.25)
    plt.tight_layout()
    RESULT_DIR.mkdir(parents=True, exist_ok=True)
    chart_path = RESULT_DIR / f"grafik_training_{scenario}.png"
    figure.savefig(chart_path, dpi=160, bbox_inches="tight")
    plt.show()
    return chart_path


TERMINATION_LABELS = {
    "success": "Berhasil loop",
    "over_distance": "Melebihi 5,5 km",
    "no_available_action": "Tidak ada action",
    "early_return": "Kembali terlalu awal",
    "step_limit": "Batas langkah",
}


TERMINATION_COLORS = {
    "success": "#16A34A",
    "over_distance": "#DC2626",
    "no_available_action": "#7C3AED",
    "early_return": "#EA580C",
    "step_limit": "#475569",
}


def plot_diagnosis_charts(history_df: pd.DataFrame, scenario: str) -> Path:
    """Menampilkan diagnosis ringkas dengan rata-rata bergerak per 50 episode."""
    episode_summary = history_df.groupby("episode", as_index=False).agg(
        distance_to_start_at_end_mean_m=(
            "distance_to_start_at_end_m", "mean"
        ),
        return_progress_ratio_mean=("return_progress_ratio", "mean"),
        closing_action_available_rate=("closing_action_was_available", "mean"),
    )
    rolling = (
        episode_summary.set_index("episode")
        .rolling(ROLLING_WINDOW, min_periods=1)
        .mean()
        .reset_index()
    )

    figure, axes = plt.subplots(2, 2, figsize=(14, 10))
    figure.suptitle(
        f"Diagnosis Training Scenario {scenario} - rata-rata {ROLLING_WINDOW} episode",
        fontsize=14,
        fontweight="bold",
    )

    axes[0, 0].plot(
        rolling["episode"],
        rolling["distance_to_start_at_end_mean_m"],
        color="#0F766E",
    )
    axes[0, 0].set(
        title=f"Rata-rata Jarak Akhir ke Start {ROLLING_WINDOW} Episode Terakhir",
        xlabel="Episode",
        ylabel="Meter",
    )

    axes[0, 1].plot(
        rolling["episode"],
        rolling["return_progress_ratio_mean"],
        color="#2563EB",
    )
    axes[0, 1].set(
        title="Konsistensi Bergerak Mendekati Start",
        xlabel="Episode",
        ylabel="Proporsi langkah",
        ylim=(-0.02, 1.02),
    )

    axes[1, 0].plot(
        rolling["episode"],
        rolling["closing_action_available_rate"] * 100,
        color="#16A34A",
    )
    axes[1, 0].set(
        title="Peluang Closing Action Tersedia",
        xlabel="Episode",
        ylabel="Rate (%)",
        ylim=(-1, 101),
    )

    # Semua tipe terminasi digabung ke panel diagnosis terakhir agar tidak
    # memerlukan gambar termination rate terpisah.
    episode_rates = pd.DataFrame({"episode": sorted(history_df["episode"].unique())})
    for reason in TERMINATION_REASONS:
        rate_by_episode = (
            history_df.assign(
                is_reason=history_df["termination_reason"].eq(reason).astype(float)
            )
            .groupby("episode", as_index=False)["is_reason"]
            .mean()
            .rename(columns={"is_reason": reason})
        )
        episode_rates = episode_rates.merge(rate_by_episode, on="episode", how="left")
    rolling_rates = (
        episode_rates.set_index("episode")
        .rolling(ROLLING_WINDOW, min_periods=1)
        .mean()
        .reset_index()
    )
    for reason in TERMINATION_REASONS:
        axes[1, 1].plot(
            rolling_rates["episode"],
            rolling_rates[reason] * 100,
            label=TERMINATION_LABELS[reason],
            color=TERMINATION_COLORS[reason],
            linewidth=2,
        )
    axes[1, 1].set(
        title=f"Termination Rate {ROLLING_WINDOW} Episode Terakhir",
        xlabel="Episode",
        ylabel="Rate (%)",
        ylim=(-1, 101),
    )
    axes[1, 1].legend(title="Tipe terminasi", fontsize=8)

    for axis in axes.flat:
        axis.grid(alpha=0.25)
    plt.tight_layout()
    RESULT_DIR.mkdir(parents=True, exist_ok=True)
    chart_path = RESULT_DIR / f"grafik_diagnosis_{scenario}.png"
    figure.savefig(chart_path, dpi=160, bbox_inches="tight")
    plt.show()
    return chart_path


def edge_latlon(
    current_node: int,
    action: EdgeAction,
    node_xy: dict[int, tuple[float, float]],
    to_wgs84: Transformer,
) -> list[tuple[float, float]]:
    geometry = action.data.get("geometry")
    coordinates = (
        list(geometry.coords)
        if hasattr(geometry, "coords")
        else [node_xy[current_node], node_xy[action.next_node]]
    )
    current_x, current_y = node_xy[current_node]
    if np.hypot(
        coordinates[-1][0] - current_x, coordinates[-1][1] - current_y
    ) < np.hypot(coordinates[0][0] - current_x, coordinates[0][1] - current_y):
        coordinates.reverse()
    return [
        (lat, lon)
        for lon, lat in (to_wgs84.transform(x, y) for x, y in coordinates)
    ]


def node_latlon(node: int, node_xy, to_wgs84) -> tuple[float, float]:
    lon, lat = to_wgs84.transform(*node_xy[node])
    return lat, lon


def km_marker(number: int, color: str):
    html = (
        f'<div style="width:26px;height:26px;line-height:26px;text-align:center;'
        f'border-radius:50%;background:{color};color:#fff;border:2px solid #fff;'
        f'font:700 12px Arial,sans-serif;box-shadow:0 1px 4px rgba(0,0,0,.4)">'
        f'{number}</div>'
    )
    return folium.DivIcon(
        html=html,
        icon_size=(26, 26),
        icon_anchor=(13, 13),
        class_name="route-km-number",
    )


def make_route_map(graph, trial: dict, scenario: str, node_xy) -> folium.Map:
    environment = trial["environment"]
    metrics = trial["metrics"]
    to_wgs84 = Transformer.from_crs(graph.graph["crs"], "EPSG:4326", always_xy=True)
    start = node_latlon(environment.start_node, node_xy, to_wgs84)
    route_map = folium.Map(
        location=start, zoom_start=15, tiles="OpenStreetMap", control_scale=True
    )
    km_colors = ["#2457F5", "#00A884", "#F59E0B", "#8B3DFF", "#EF4444"]

    cumulative_m = 0.0
    for current_node, action in environment.path_actions:
        color_index = min(4, int(cumulative_m // 1000))
        folium.PolyLine(
            edge_latlon(current_node, action, node_xy, to_wgs84),
            color=km_colors[color_index],
            weight=6,
            opacity=0.92,
            tooltip=f"Segmen KM {color_index}-{color_index + 1}",
        ).add_to(route_map)
        cumulative_m += action.length_m

    folium.Marker(
        start,
        tooltip="START - KM 0",
        popup="<b>START</b><br>KM 0",
        icon=folium.Icon(color="green", icon="play", prefix="fa"),
    ).add_to(route_map)

    cumulative_m = 0.0
    next_km = 1
    for current_node, action in environment.path_actions:
        cumulative_m += action.length_m
        while next_km <= 5 and cumulative_m >= next_km * 1000:
            if not (next_km == 5 and metrics["is_loop"]):
                location = edge_latlon(current_node, action, node_xy, to_wgs84)[-1]
                folium.Marker(
                    location,
                    tooltip=f"KM {next_km}",
                    icon=km_marker(next_km, km_colors[next_km - 1]),
                ).add_to(route_map)
            next_km += 1

    if metrics["is_loop"]:
        from_wgs84 = Transformer.from_crs("EPSG:4326", graph.graph["crs"], always_xy=True)
        x, y = from_wgs84.transform(start[1], start[0])
        finish_lon, finish_lat = to_wgs84.transform(x + 12, y + 12)
        finish_location = (finish_lat, finish_lon)
        finish_color = "purple"
        finish_tooltip = "FINISH - KM 5 (posisi asli sama dengan start)"
    else:
        finish_location = node_latlon(environment.path_nodes[-1], node_xy, to_wgs84)
        finish_color = "red"
        finish_tooltip = "FINISH - rute belum kembali ke start"

    folium.Marker(
        finish_location,
        tooltip=finish_tooltip,
        popup=f"<b>FINISH</b><br>{metrics['distance_km']:.2f} km",
        icon=folium.Icon(color=finish_color, icon="flag-checkered", prefix="fa"),
    ).add_to(route_map)
    return route_map


# ============================================================
# F. FUNGSI TUNGGAL YANG DIPANGGIL NOTEBOOK SCENARIO
# ============================================================

def select_representative_trial(trials: list[dict]) -> tuple[dict, str]:
    """Memilih satu Q-table/seed untuk divisualisasikan pada peta.

    Rute valid selalu lebih penting daripada rute gagal. Jika belum ada loop
    valid, peta menjadi alat diagnosis: pilih rute yang panjangnya paling dekat
    dengan target terlebih dahulu. Jarak akhir ke start hanya dipakai sebagai
    pembeda agar rute yang berhenti terlalu dini tidak tampak sebagai terbaik.
    """
    valid_loop_trials = [
        trial for trial in trials if trial["metrics"]["is_loop"]
    ]

    if valid_loop_trials:
        selected = min(
            valid_loop_trials,
            key=lambda trial: (
                trial["metrics"]["absolute_distance_error_m"],
                -np.nan_to_num(trial["metrics"]["mean_comfort"], nan=-1),
                -np.nan_to_num(trial["metrics"]["return_progress_ratio"], nan=-1),
                trial["metrics"]["seed"],
            ),
        )
        reason = (
            f"Dipilih dari {len(valid_loop_trials)} loop valid: galat jarak "
            "paling kecil; jika setara, comfort lalu return progress lebih tinggi."
        )
        return selected, reason

    selected = min(
        trials,
        key=lambda trial: (
            trial["metrics"]["absolute_distance_error_m"],
            trial["metrics"]["distance_to_start_at_end_m"],
            -np.nan_to_num(trial["metrics"]["mean_comfort"], nan=-1),
            -np.nan_to_num(trial["metrics"]["return_progress_ratio"], nan=-1),
            trial["metrics"]["seed"],
        ),
    )
    reason = (
        "Tidak ada loop valid, sehingga dipilih rute dengan galat jarak "
        "paling kecil; jika setara, jarak akhir ke start paling kecil, "
        "comfort tertinggi, lalu return progress tertinggi."
    )
    return selected, reason


def run_scenario_experiment(graph, start_node: int, scenario: str) -> dict:
    """Menjalankan satu scenario A-C dengan core yang sama."""
    if scenario not in {"A", "B", "C"}:
        raise ValueError("Scenario harus A, B, atau C.")

    RESULT_DIR.mkdir(parents=True, exist_ok=True)
    add_comfort_scores(graph)
    actions_by_node = build_actions(graph)
    node_xy = {
        int(node): (float(data["x"]), float(data["y"]))
        for node, data in graph.nodes(data=True)
    }

    histories, evaluation_rows, trials = [], [], []
    print(f"Menjalankan Scenario {scenario}: {len(SEEDS)} seed x {EPISODES:,} episode")

    for seed in SEEDS:
        q_table, history = train_q_learning(
            scenario, seed, start_node, actions_by_node, node_xy
        )
        environment, metrics = evaluate_greedy(
            scenario, q_table, seed, start_node, actions_by_node, node_xy
        )
        metrics.update({
            "scenario": scenario,
            "seed": seed,
            "q_state_count": len(q_table),
        })
        histories.append(history)
        evaluation_rows.append(metrics)
        trials.append({
            "environment": environment,
            "metrics": metrics,
            "q_table": q_table,
        })
        print(
            f"seed={seed}: {metrics['termination_reason']}, "
            f"{metrics['distance_km']:.2f} km, "
            f"is_loop={metrics['is_loop']}"
        )

    history_df = pd.concat(histories, ignore_index=True)
    # metrics_df menyimpan detail internal untuk diagnosis dan pemilihan peta.
    # evaluation_df adalah hasil evaluasi ringkas yang dipakai pada BAB IV.
    metrics_df = pd.DataFrame(evaluation_rows)
    evaluation_df = metrics_df.loc[:, list(EVALUATION_RESULT_COLUMNS)].copy()
    diagnosis_df = diagnosis_summary(metrics_df)
    training_termination_df = termination_rate_table(history_df)
    evaluation_termination_df = termination_rate_table(metrics_df)

    history_path = RESULT_DIR / f"training_history_{scenario}.csv"
    metrics_path = RESULT_DIR / f"evaluation_metrics_{scenario}.csv"
    diagnosis_path = RESULT_DIR / f"diagnosis_metrics_{scenario}.csv"
    training_termination_path = RESULT_DIR / f"termination_rates_training_{scenario}.csv"
    evaluation_termination_path = RESULT_DIR / f"termination_rates_evaluation_{scenario}.csv"
    history_df.to_csv(history_path, index=False)
    evaluation_df.to_csv(metrics_path, index=False)
    diagnosis_df.to_csv(diagnosis_path, index=False)
    training_termination_df.to_csv(training_termination_path, index=False)
    evaluation_termination_df.to_csv(evaluation_termination_path, index=False)

    # Tabel evaluasi sengaja dibatasi pada metrik yang menjawab tujuan penelitian.
    # Metrik diagnosis training ditampilkan dalam grafik terpisah di bawahnya.
    print("Tampilan vertikal metrik evaluasi utama per seed")
    display(
        evaluation_df.sort_values("seed")
        .set_index("seed")
        .loc[:, list(EVALUATION_DISPLAY_COLUMNS)]
        .T
    )

    chart_path = plot_training_charts(history_df, scenario)
    diagnosis_chart_path = plot_diagnosis_charts(history_df, scenario)

    representative, representative_reason = select_representative_trial(trials)
    selected_metrics = representative["metrics"]
    print("=== Q-TABLE / SEED YANG DIPILIH UNTUK PETA ===")
    print(f"Scenario: {scenario}; seed: {selected_metrics['seed']}")
    print(
        "Metrik: "
        f"is_loop={selected_metrics['is_loop']}, "
        f"jarak={selected_metrics['total_distance_m']:.2f} m, "
        f"galat={selected_metrics['absolute_distance_error_m']:.2f} m, "
        f"comfort={selected_metrics['mean_comfort']:.3f}, "
        f"return_progress={selected_metrics['return_progress_ratio']:.3f}, "
        f"jarak akhir ke start={selected_metrics['distance_to_start_at_end_m']:.2f} m, "
        f"terminasi={selected_metrics['termination_reason']}"
    )
    print(f"Alasan: {representative_reason}")
    route_map = make_route_map(graph, representative, scenario, node_xy)
    map_path = RESULT_DIR / f"peta_interaktif_scenario_{scenario}.html"
    route_map.save(map_path)
    display(route_map)

    print(f"History: {history_path}")
    print(f"Evaluasi: {metrics_path}")
    print(f"Diagnosis: {diagnosis_path}")
    print(f"Termination rate training: {training_termination_path}")
    print(f"Termination rate evaluasi: {evaluation_termination_path}")
    print(f"Grafik training utama: {chart_path}")
    print(f"Grafik diagnosis: {diagnosis_chart_path}")
    print(f"Peta: {map_path}")

    return {
        "scenario": scenario,
        "history": history_df,
        "metrics": evaluation_df,
        "evaluation_details": metrics_df,
        "diagnosis": diagnosis_df,
        "training_termination_rates": training_termination_df,
        "evaluation_termination_rates": evaluation_termination_df,
        "trials": trials,
        "representative": representative,
        "representative_reason": representative_reason,
    }

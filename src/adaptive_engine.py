from typing import Optional
from puzzle_generator import EASY, MEDIUM, HARD, DIFFICULTY_LEVELS
from tracker import PerformanceTracker


class AdaptiveEngine:
    """
    Rule-based adaptive engine using recent accuracy and speed.

    Rules (per current difficulty, using a sliding window of N attempts):

    - If accuracy >= 0.8 AND avg time <= fast_threshold  -> level up.
    - If accuracy <= 0.4 OR  avg time >= slow_threshold -> level down.
    - Otherwise                                            stay.
    """

    def __init__(self, fast_threshold: float = 6.0, slow_threshold: float = 12.0, window_size: int = 5):
        self.fast_threshold = fast_threshold
        self.slow_threshold = slow_threshold
        self.window_size = window_size

    def _next_level_up(self, difficulty: str) -> str:
        if difficulty == EASY:
            return MEDIUM
        if difficulty == MEDIUM:
            return HARD
        return HARD

    def _next_level_down(self, difficulty: str) -> str:
        if difficulty == HARD:
            return MEDIUM
        if difficulty == MEDIUM:
            return EASY
        return EASY

    def suggest_next_difficulty(self, tracker: PerformanceTracker, current_difficulty: str) -> str:
        acc = tracker.last_n_accuracy(current_difficulty, self.window_size)
        avg_t = tracker.last_n_avg_time(current_difficulty, self.window_size)

        # If not enough data yet, keep same level
        if acc is None or avg_t is None:
            return current_difficulty

        # Doing very well and fast -> move up
        if acc >= 0.8 and avg_t <= self.fast_threshold:
            return self._next_level_up(current_difficulty)

        # Struggling or very slow -> move down
        if acc <= 0.4 or avg_t >= self.slow_threshold:
            return self._next_level_down(current_difficulty)

        # In the “learning zone” -> stay at same level
        return current_difficulty

    def recommend_start_level(self, tracker: PerformanceTracker) -> str:
        """
        Simple heuristic for recommended next starting level based on
        per-difficulty accuracy. Prefer a level where accuracy is in
        a "good challenge" band [0.6, 0.85].
        """
        summary = tracker.summary_by_difficulty()
        best_level: Optional[str] = None

        for level in DIFFICULTY_LEVELS:
            if level in summary:
                acc = summary[level]["accuracy"]
                if 0.6 <= acc <= 0.85:
                    best_level = level

        # Fall back to MEDIUM if no good band found
        if best_level is None:
            best_level = MEDIUM

        return best_level

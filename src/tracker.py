import statistics
from typing import List, Dict, Any, Optional


class PerformanceTracker:
    def __init__(self):
        self.attempts: List[Dict[str, Any]] = []

    def log_attempt(self, difficulty: str, correct: bool, time_taken: float):
        self.attempts.append(
            {
                "difficulty": difficulty,
                "correct": correct,
                "time": time_taken,
            }
        )

    def overall_accuracy(self) -> float:
        if not self.attempts:
            return 0.0
        correct_count = sum(1 for a in self.attempts if a["correct"])
        return correct_count / len(self.attempts)

    def average_time(self) -> float:
        if not self.attempts:
            return 0.0
        return statistics.mean(a["time"] for a in self.attempts)

    def last_n_accuracy(self, difficulty: str, n: int = 5) -> Optional[float]:
        filtered = [a for a in self.attempts if a["difficulty"] == difficulty]
        if not filtered:
            return None
        last_n = filtered[-n:]
        correct_count = sum(1 for a in last_n if a["correct"])
        return correct_count / len(last_n)

    def last_n_avg_time(self, difficulty: str, n: int = 5) -> Optional[float]:
        filtered = [a for a in self.attempts if a["difficulty"] == difficulty]
        if not filtered:
            return None
        last_n = filtered[-n:]
        return statistics.mean(a["time"] for a in last_n)

    def attempts_by_difficulty(self, difficulty: str):
        return [a for a in self.attempts if a["difficulty"] == difficulty]

    def summary_by_difficulty(self):
        difficulties = sorted({a["difficulty"] for a in self.attempts})
        summary = {}
        for d in difficulties:
            attempts = self.attempts_by_difficulty(d)
            if not attempts:
                continue
            acc = sum(1 for a in attempts if a["correct"]) / len(attempts)
            avg_t = statistics.mean(a["time"] for a in attempts)
            summary[d] = {"accuracy": acc, "avg_time": avg_t, "count": len(attempts)}
        return summary

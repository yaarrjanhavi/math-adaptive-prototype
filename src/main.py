import csv
import os
import time
from typing import List, Dict, Any

from colorama import Fore, Style, init

from puzzle_generator import generate_puzzle, EASY, MEDIUM, HARD
from tracker import PerformanceTracker
from adaptive_engine import AdaptiveEngine

init(autoreset=True)


def choose_initial_difficulty():
    print("Choose starting difficulty:")
    print("1) Easy")
    print("2) Medium")
    print("3) Hard")
    while True:
        choice = input("Enter 1/2/3: ").strip()
        if choice == "1":
            return EASY
        if choice == "2":
            return MEDIUM
        if choice == "3":
            return HARD
        print("Invalid choice, try again.")


def append_to_csv_log(
    filename: str,
    row: Dict[str, Any],
):
    file_exists = os.path.exists(filename)
    fieldnames = [
        "name",
        "difficulty",
        "op",
        "a",
        "b",
        "correct",
        "time",
    ]
    with open(filename, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)


def compute_half_trends(attempts: List[Dict[str, Any]]):
    """
    Compute accuracy and avg time for first half vs second half of attempts.
    Returns dict with stats or None if fewer than 2 attempts.
    """
    if len(attempts) < 2:
        return None

    mid = len(attempts) // 2
    first_half = attempts[:mid]
    second_half = attempts[mid:]

    def acc(lst):
        if not lst:
            return 0.0
        return sum(1 for a in lst if a["correct"]) / len(lst)

    def avg_time(lst):
        if not lst:
            return 0.0
        return sum(a["time"] for a in lst) / len(lst)

    return {
        "first": {"accuracy": acc(first_half), "avg_time": avg_time(first_half), "count": len(first_half)},
        "second": {"accuracy": acc(second_half), "avg_time": avg_time(second_half), "count": len(second_half)},
    }


def run_session():
    print("=" * 50)
    print("Welcome to Math Adventures - Adaptive Practice!")
    name = input("Enter your name: ").strip() or "Learner"
    print(f"Hi {name}! Let's practice some math.\n")

    current_difficulty = choose_initial_difficulty()
    tracker = PerformanceTracker()
    engine = AdaptiveEngine()

    num_questions = 15
    print(f"\nYou will get up to {num_questions} questions. Type 'q' to quit early.\n")

    for i in range(1, num_questions + 1):
        print("-" * 40)
        print(f"Question {i} (Difficulty: {current_difficulty})")

        question_text, correct_answer, meta = generate_puzzle(current_difficulty)
        print("Solve:", question_text)

        start = time.time()
        user_input = input("Your answer (or 'q' to quit): ").strip()
        if user_input.lower() == "q":
            print("Ending session early.\n")
            break

        try:
            user_answer = int(user_input)
        except ValueError:
            print(Fore.RED + "Invalid input. Counting as incorrect.")
            user_answer = None

        end = time.time()
        time_taken = end - start

        correct = (user_answer == correct_answer)
        if correct:
            print(Fore.GREEN + "Correct!")
        else:
            print(Fore.RED + f"Incorrect. The correct answer was {correct_answer}.")

        print(f"Time taken: {time_taken:.1f} seconds")
        tracker.log_attempt(current_difficulty, correct, time_taken)

        # Log to CSV for future ML / analysis
        csv_row = {
            "name": name,
            "difficulty": current_difficulty,
            "op": meta["op"],
            "a": meta["a"],
            "b": meta["b"],
            "correct": int(correct),
            "time": round(time_taken, 3),
        }
        append_to_csv_log("session_log.csv", csv_row)

        # Adaptive step
        current_difficulty = engine.suggest_next_difficulty(tracker, current_difficulty)

    print("\n" + "=" * 50)
    print("Session Summary")
    total = len(tracker.attempts)
    overall_acc = tracker.overall_accuracy()
    avg_time = tracker.average_time()
    print(f"Total questions: {total}")
    print(f"Overall accuracy: {overall_acc * 100:.1f}%")
    print(f"Average time per question: {avg_time:.1f} seconds")

    # Per-difficulty breakdown
    summary = tracker.summary_by_difficulty()
    if summary:
        print("\nBreakdown by difficulty:")
        print(f"{'Level':<10} {'Count':<8} {'Accuracy':<12} {'Avg Time (s)':<12}")
        for level, stats in summary.items():
            print(
                f"{level:<10} {stats['count']:<8} {stats['accuracy'] * 100:>6.1f}%"
                f" {stats['avg_time']:>12.1f}"
            )

    # Trend: first half vs second half
    trends = compute_half_trends(tracker.attempts)
    if trends:
        print("\nProgress trend (first half vs second half):")
        f1 = trends["first"]
        s2 = trends["second"]
        print(
            f"First half  - {f1['count']} questions, "
            f"accuracy {f1['accuracy'] * 100:.1f}%, "
            f"avg time {f1['avg_time']:.1f}s"
        )
        print(
            f"Second half - {s2['count']} questions, "
            f"accuracy {s2['accuracy'] * 100:.1f}%, "
            f"avg time {s2['avg_time']:.1f}s"
        )

    recommended = engine.recommend_start_level(tracker)
    print(f"\nRecommended starting level for next time: {Fore.CYAN}{recommended}{Style.RESET_ALL}")
    print("Thanks for playing, keep practicing!")


if __name__ == "__main__":
    run_session()

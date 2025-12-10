# Math Adventures – Adaptive Learning Prototype  
Short Technical Note (1–2 pages)

## 1. Objective

The goal of this prototype is to demonstrate how AI-style adaptive logic can personalize math practice for children (ages 5–10) by automatically adjusting difficulty based on performance. [file:1]  
The system focuses on keeping learners in an optimal challenge zone: not too easy, not too hard. [file:1]

---

## 2. System Architecture & Flow

### Components

- **Puzzle Generator (`puzzle_generator.py`)**  
  Generates arithmetic questions (addition, subtraction, multiplication, division) at three difficulty levels: Easy, Medium, Hard. [file:1]

- **Performance Tracker (`tracker.py`)**  
  Logs each attempt with:
  - Difficulty
  - Correctness (True/False)
  - Response time in seconds  
  It can compute overall accuracy, average time, per-difficulty stats, and windowed metrics over the last *N* attempts.

- **Adaptive Engine (`adaptive_engine.py`)**  
  Implements rule-based logic that decides the next difficulty and recommends a starting level for the next session. [file:1]

- **CLI Orchestrator (`main.py`)**  
  Provides a simple command-line interface, runs the question loop, logs attempts to both memory and CSV, and displays the final summary.

### Flow Diagram (Text)

1. User enters name and selects initial difficulty (Easy / Medium / Hard). [file:1]  
2. For each question:
   - `main.py` calls `generate_puzzle(difficulty)` to get a question and the correct answer.
   - The user answers; `main.py` records correctness and response time.
   - `tracker.py` logs the attempt in memory.
   - The attempt is also appended as a row in `session_log.csv`.
   - `adaptive_engine.py` uses recent performance to choose the next difficulty. [file:1]
3. At session end:
   - `tracker.py` computes overall and per-difficulty stats.
   - `adaptive_engine.py` recommends a starting level for next time.
   - `main.py` prints the summary and trends.

---

## 3. Adaptive Logic (Rule-Based)

The adaptive logic is intentionally rule-based for simplicity and transparency, while still using core metrics: recent accuracy and average response time. [file:1]

For the current difficulty level, the engine looks at a sliding window of the last *N* attempts at that level (e.g., N = 5):

- Let:
  - \( \text{acc} = \) accuracy over last *N* attempts at this difficulty.
  - \( \text{avg\_t} = \) average response time over last *N* attempts.

- Tunable thresholds:
  - `fast_threshold` (e.g., 6 seconds)
  - `slow_threshold` (e.g., 12 seconds)

**Rules:**

- If `acc >= 0.8` **and** `avg_t <= fast_threshold` → **increase** difficulty (Easy → Medium → Hard).  
- If `acc <= 0.4` **or** `avg_t >= slow_threshold` → **decrease** difficulty (Hard → Medium → Easy).  
- Otherwise → keep the same difficulty.

This directly encodes:

- Doing well and fast ⇒ learner is ready for more challenge.  
- Struggling or very slow ⇒ learner may need easier problems and more practice.  
- In-between ⇒ learner stays at a level that appears suitably challenging.

### Recommended Starting Level

At session end, the engine examines per-difficulty accuracy and prefers levels where accuracy lies in a “good challenge band” (e.g., 60–85%).  
If no level falls in this band, it defaults to Medium as a safe generic recommendation. [file:1]

---

## 4. Metrics Tracked and How They Influence Difficulty

The system tracks:

- **Correctness per question**  
  Used for:
  - Overall accuracy.
  - Per-difficulty accuracy.
  - Sliding-window accuracy for adaptive decisions.

- **Response time per question**  
  Used to:
  - Compute average time across the session.
  - Measure speed in the sliding window to distinguish “fast & accurate” from “slow or hesitant”.

- **Per-difficulty aggregates**  
  Count, accuracy, and average time for each of Easy, Medium, Hard. [file:1]

These metrics influence the system in three ways:

1. **Real-time difficulty selection**  
   - The sliding-window accuracy and time thresholds are the core of the rule-based adaptive engine.

2. **Session summary & progress trend**  
   - Overall accuracy/time and per-difficulty breakdown are shown to give the learner (or instructor) immediate feedback. [file:1]  
   - A simple trend compares first half vs second half performance to indicate whether speed and accuracy improved or declined over the session.

3. **Future data-driven improvement**  
   - Each attempt is logged to `session_log.csv` with: name, difficulty, operation, operands, correctness, and time.  
   - This creates a dataset suitable for training a lightweight ML model in the future.

---

## 5. Why Rule-Based (for Now) and How to Extend with ML

This prototype uses a **rule-based adaptive engine** instead of training a model, for several reasons: [file:1]

- **Simplicity & clarity**: Threshold-based rules are easy to explain and reason about in a short assignment.  
- **Low data requirement**: The system works from the first session; no historical data is needed.  
- **Alignment with learning goals**: The core objective is to show understanding of adaptive logic, not to build a heavy ML system. [file:1]

However, the design is **ML-ready**:

- The CSV log includes all inputs and outcomes needed to train models such as:
  - A logistic regression that predicts the probability of success at each difficulty. [file:1]
  - A small decision tree that suggests the next difficulty given recent performance features. [file:1]
- As more data is collected from real learners, such models could replace or enhance the rule-based engine, while still using the same interfaces (`suggest_next_difficulty`, `recommend_start_level`).

---

## 6. Handling Noisy or Inconsistent Performance (Discussion)

In real usage, learners may guess quickly, get distracted, or have occasional outliers in response time. Potential strategies include: [file:1]

- Using sliding windows and averages (already done) instead of single-question decisions.  
- Ignoring extreme outliers in time (e.g., very large values when the learner leaves the keyboard).  
- Applying small “cooldown” periods before changing difficulty again, to avoid oscillations.

These extensions are not fully implemented, but the current architecture makes it straightforward to add such logic later.

---

## 7. Scaling Beyond Basic Math (Discussion)

The same structure can scale to: [file:1]

- More granular math topics (fractions, word problems, geometry).  
- Other domains like language learning (vocabulary, reading comprehension) or science quizzes.

The key idea is to keep:

- A **generator** that can tag questions by topic/difficulty.  
- A **tracker** that logs performance and timing.  
- An **adaptive engine** that uses these logs to pick the next appropriate challenge.

This prototype demonstrates that pattern on a small, focused problem. [file:1]

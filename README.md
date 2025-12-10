# Math Adventures – Adaptive Learning Prototype

This project is a minimal adaptive math practice tool for children (ages 5–10). It generates basic arithmetic puzzles and automatically adjusts difficulty based on the learner’s recent performance to keep them in an optimal challenge zone. [file:1]

---

## Features

- Three difficulty levels: **Easy**, **Medium**, **Hard**. [file:1]  
- Dynamic puzzle generation for addition, subtraction, multiplication, and division. [file:1]  
- Performance tracking: correctness and response time for each question. [file:1]  
- Rule-based adaptive engine that moves difficulty up, down, or keeps it stable based on recent accuracy and speed. [file:1]  
- End-of-session summary with:
  - Overall accuracy and average response time. [file:1]
  - Per-difficulty stats (count, accuracy, average time). [file:1]
  - Simple progress trend (first half vs second half of the session).
  - Recommended starting level for the next session.  
- CSV logging (`session_log.csv`) of all attempts for future data analysis or ML experiments.

---

## Project Structure
```
math-adaptive-prototype/
├─ README.md
├─ TECHNICAL_NOTE.md
├─ requirements.txt
└─ src/
├─ main.py
├─ puzzle_generator.py
├─ tracker.py
└─ adaptive_engine.py
```

- `puzzle_generator.py`: Generates math puzzles for each difficulty level. [file:1]  
- `tracker.py`: Tracks correctness and response time across the session. [file:1]  
- `adaptive_engine.py`: Contains the rule-based adaptive logic and next-level recommendation. [file:1]  
- `main.py`: Command-line interface tying everything together, including logging and summaries.

---

## Installation
```
git clone https://github.com/yaarrjanhavi/math-adaptive-prototype.git
cd math-adaptive-prototype
pip install -r requirements.txt
```

Use `pip3` if needed.

---

## Usage
From the project root:
```
python -m src.main
```

If that does not work in your environment:
```
cd src
python main.py
```

Flow:

1. Enter learner name.  
2. Choose initial difficulty (Easy / Medium / Hard). [file:1]  
3. Answer up to 15 adaptive questions (or quit early with `q`).  
4. View summary, trend, and recommended starting level for next time.

---

## Future Work

- Use the logged `session_log.csv` to train a lightweight ML model (e.g., logistic regression or decision tree) to predict the best next difficulty. [file:1]  
- Extend the engine to more topics (fractions, word problems) and other domains beyond math. [file:1]



import random

EASY = "Easy"
MEDIUM = "Medium"
HARD = "Hard"

DIFFICULTY_LEVELS = [EASY, MEDIUM, HARD]


def generate_puzzle(difficulty: str):
    """
    Generate a math puzzle based on difficulty.
    Returns: question_text (str), correct_answer (int), metadata (dict)
    """
    if difficulty == EASY:
        a = random.randint(0, 9)
        b = random.randint(0, 9)
        op = random.choice(["+", "-"])
    elif difficulty == MEDIUM:
        op = random.choice(["+", "-", "*"])
        if op == "*":
            a = random.randint(2, 9)
            b = random.randint(2, 9)
        else:
            a = random.randint(10, 50)
            b = random.randint(1, 30)
    else:
        op = random.choice(["+", "-", "*", "/"])
        if op == "/":
            b = random.randint(2, 12)
            ans = random.randint(2, 12)
            a = ans * b
        elif op == "*":
            a = random.randint(5, 20)
            b = random.randint(5, 20)
        else:
            a = random.randint(50, 200)
            b = random.randint(10, 100)

    if op == "+":
        correct_answer = a + b
    elif op == "-":
        correct_answer = a - b
    elif op == "*":
        correct_answer = a * b
    else:
        correct_answer = a // b

    question_text = f"{a} {op} {b} = ?"
    metadata = {"a": a, "b": b, "op": op, "difficulty": difficulty}
    return question_text, correct_answer, metadata

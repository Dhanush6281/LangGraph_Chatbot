import re
from datetime import datetime


def calculator(expression):
    try:
        return str(eval(expression))
    except Exception:
        return "Invalid mathematical expression."


def current_time():
    return datetime.now().strftime("%d-%m-%Y %I:%M:%S %p")


def detect_tool(prompt):
    prompt = prompt.strip()

    lower_prompt = prompt.lower()

    # Time / Date
    if any(
        word in lower_prompt
        for word in [
            "time",
            "date",
            "today",
            "current time",
            "current date",
        ]
    ):
        return "time", None

    # Calculator
    expression = re.sub(r"[^0-9+\-*/(). ]", "", prompt)

    if expression.strip():

        if any(op in expression for op in ["+", "-", "*", "/"]):
            return "calculator", expression

    return None, None
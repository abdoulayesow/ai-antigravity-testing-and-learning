import datetime
import math

def get_current_time(args=None):
    """Returns the current time."""
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def calculate(expression):
    """Evaluates a mathematical expression."""
    try:
        # Safety: only allow specific characters
        allowed = set("0123456789+-*/(). ")
        if not all(c in allowed for c in expression):
            return "Error: Invalid characters in expression."
        return str(eval(expression, {"__builtins__": None}, {}))
    except Exception as e:
        return f"Error calculating: {e}"

available_tools = {
    "get_current_time": get_current_time,
    "calculate": calculate
}

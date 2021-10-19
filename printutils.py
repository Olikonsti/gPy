import threading

GLOBAL = {}
ERRORS = []
std_lib_lines = 34

def error(text, line_index, word_index):
    print(f"""
-------------------
Error: {text}

line: {line_index + 1}
action: {GLOBAL["in"].current_action}
""")
    ERRORS.append(f"""
-------------------
Error: {text}

line: {line_index + 1}
action: {GLOBAL["in"].current_action}
""")

def make_math(op, int1, int2):
    return eval(f"int1 {op} int2")

def check_operator(operator, var1, var2):
    if operator == "==":
        if var1 == var2:
            return True
        else:
            return False
    elif operator == "!=":
        if var1 != var2:
            return True
        else:
            return False
    elif operator == ">":
        if var1 > var2:
            return True
        else:
            return False
    elif operator == "<":
        if var1 < var2:
            return True
        else:
            return False

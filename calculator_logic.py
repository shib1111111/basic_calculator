OPERATIONS = ["Addition", "Subtraction", "Multiplication", "Division"]

def calculate(num1, num2, operation):
    if operation == "Addition":
        return num1 + num2
    elif operation == "Subtraction":
        return num1 - num2
    elif operation == "Multiplication":
        return num1 * num2
    elif operation == "Division":
        if num2 == 0:
            return "Cannot divide by zero"
        else:
            return num1 / num2

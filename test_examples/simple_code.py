"""
Simple Python file - Should get LOW RISK
This is a basic calculator with minimal complexity
"""

def add(a, b):
    """Add two numbers"""
    return a + b

def subtract(a, b):
    """Subtract two numbers"""
    return a - b

def multiply(a, b):
    """Multiply two numbers"""
    return a * b

def divide(a, b):
    """Divide two numbers"""
    if b == 0:
        return None
    return a / b

# Simple usage
if __name__ == "__main__":
    print("Calculator")
    print(add(5, 3))
    print(subtract(10, 4))

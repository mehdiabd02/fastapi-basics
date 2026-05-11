def add(num1: int, num2: int) -> int:
    return num1 + num2

def subtract(num1: int, num2: int) -> int:
    return num1 - num2

def multiply(num1: int, num2: int) -> int:
    return num1 * num2 

def divide(num1: int, num2: int) -> float:
    if num2 == 0:
        raise ValueError("Cannot divide by zero")
    return num1 / num2

class BankAccount:
    def __init__(self, balance: float = 0.0):
        self.balance = balance

    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self.balance += amount

    def withdraw(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        if amount > self.balance:
            raise ValueError("Insufficient funds")
        self.balance -= amount
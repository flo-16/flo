#!/usr/bin/env python3

def fib5(n: int) -> int:
    if n == 0: return n  # Spezialfall
    last: int = 0  # Am Anfang auf fib(0) setzen
    next: int = 1  # Am Anfang auf fib(1) setzen
    for _ in range(1, n):
        last, next = next, last + next
    return next


if __name__ == "__main__":
    print(fib5(5))
    print(fib5(50))


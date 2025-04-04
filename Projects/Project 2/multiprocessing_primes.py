from multiprocessing import Process, Value, Lock
import time 
import math

def is_prime(n):
    if n <= 1: 
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True


# This function is run by all processes
# 'with lock' is used to make sure that only 1 process can access the shared_result variable at a time.
def find_highest_prime(start, end, shared_result, lock):
    highest_prime = 0
    for num in range(start, end):
        if is_prime(num):
            highest_prime = num
    with lock:
        if highest_prime > shared_result.value:
            shared_result.value = highest_prime # Only the highest prime value from each process is saved to the shared value.


def fibonacci(n):
    a, b = 0, 1
    sequence = [a, b]
    for _ in range(2, n + 1):
        a, b = b, a + b
        sequence.append(b)
    return ' '.join(map(str, sequence)) # Fibonacci sequence should be separated by spaces instead of looking like 1 huge value.


def factorial(n): 
    return math.factorial(n)


# Main function to control flow
# Each process has a range of 20 numbers to check for primes.
if __name__ == "__main__":
    start_time = time.time()
    num_processes = 5
    n = 100 # Full sequence for Fibonacci won't print if 'n' is too high
    range_per_process = n // num_processes
    shared_result = Value('i', 0)
    lock = Lock()

    processes = [
        Process(
            target=find_highest_prime, 
            args=(i * range_per_process, (i + 1) * range_per_process, shared_result, lock))
        for i in range(num_processes)
    ]

    for p in processes:
        p.start()
    for p in processes:
        p.join()

    highest_prime = shared_result.value
    end_time = time.time()
    print(f"Highest prime: {shared_result.value}")
    print(f"Time taken: {end_time - start_time:.2f} seconds")

    fib_result = fibonacci(highest_prime)
    fact_result = factorial(highest_prime)
    print(f"Fibonacci of {highest_prime}: {fib_result}")
    print(f"Factorial of {highest_prime}: {fact_result}")
from multiprocessing import Process, Value, Lock
import time 
import math
import sys

sys.set_int_max_str_digits(1000000)


def is_prime(n):
    if n <= 1: 
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True


# This function is run by all processes
# 'with lock' is used to make sure that only 1 process can access the shared_result variable at a time.
def find_highest_prime(shared_result, lock, time_limit):
    highest_prime = 0 # Start checking from 0
    start_time = time.time()

    while time.time() - start_time < time_limit:
        if is_prime(highest_prime):
            with lock:
                if highest_prime > shared_result.value:
                    shared_result.value = highest_prime # Only the highest prime value from each process is saved to the shared value.
        highest_prime += 1


def fibonacci(n):
    fib_digit_limit = 10000
    if n > fib_digit_limit: 
        print(f"Fibonacci of {n} is too large to display.  This digit limit is {fib_digit_limit}.  Calculating new value(limit value)...")
        n = fib_digit_limit

    a, b = 0, 1
    for i in range(n):
        a, b = b, a + b
    print(f"The Fibonacci number for {n} is: {a}")
       


def factorial(n): 
    fact_digit_limit = 10000
    if n > fact_digit_limit: 
        print(f"Fibonacci of {n} is too large to display.  This digit limit is {fact_digit_limit}.  Calculating new value(limit value)...")
        n = fact_digit_limit

    result = math.factorial(n)
    print(f"The Factorial of {n} is: {result}")


# Main function to control flow
# All processes run in parallel
if __name__ == "__main__":
    start_time = time.time()
    num_processes = 5
    time_limit = 180
    shared_result = Value('i', 0)
    lock = Lock()

    # Creates a list of processes and defines the range of numbers that each process should work in.
    # Each process is told to run the function 'find_highest_prime'
    processes = [
        Process(
            target=find_highest_prime, 
            args=(shared_result, lock, time_limit)
            )
        for _ in range(num_processes)
    ]

    for p in processes:
        p.start()
    for p in processes:
        p.join()

    highest_prime = shared_result.value
    end_time = time.time()
    print(f"Highest prime found in 3 minutes: {highest_prime}")
    print(f"Time taken: {end_time - start_time:.2f} seconds")

    fibonacci_process = Process(target=fibonacci, args=(highest_prime,))
    factorial_process = Process(target=factorial, args=(highest_prime,))

    fibonacci_process.start()
    factorial_process.start()

    fibonacci_process.join()
    factorial_process.join()
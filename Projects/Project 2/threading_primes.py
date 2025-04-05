import threading
import time
import math
import sys

sys.set_int_max_str_digits(1000000)
highest_prime = 0
lock = threading.Lock()

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True


# This is the function that each thread runs to check for prime numbers
# 'lock' is used to prevent the threads from accessing the 'highest_prime' variable at the same time. Prevents threads from overwriting each other.
def worker(starting_number, end_time, lock):
    global highest_prime
    n = starting_number
    while time.time() < end_time:
        if is_prime(n):
            with lock:
                if n > highest_prime:
                    highest_prime = n
        n += 1


# This function defines the number of threads and the time limit for each thread
def threaded_pool():
    num_threads = 5
    end_time = time.time() + 180

    # Creates a list threads and defines the task for each thread.
    # The worker function is the task that each thread needs to execute.
    threads = []
    for i in range(num_threads):
        thread = threading.Thread(target=worker, 
                                  args=(i, end_time, lock)
                                  )                            
        threads.append(thread)
        thread.start()

    # Wait for threads to finish and join
    for thread in threads:
        thread.join()
        
    return highest_prime



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


# Main control flow
if __name__ == "__main__":
    start_time = time.time()
    highest_prime = threaded_pool()
    end_time = time.time()

    print(f"Highest prime found in 3 minutes: {highest_prime}")
    print(f"Time taken: {end_time - start_time:.2f} seconds")

    fib_thread = threading.Thread(target=fibonacci, args=(highest_prime,))
    fact_thread = threading.Thread(target=factorial, args=(highest_prime,))

    fib_thread.start()
    fact_thread.start()

    fib_thread.join()
    fact_thread.join()
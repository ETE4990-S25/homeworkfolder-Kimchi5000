from queue import Queue, Empty
import threading
import time
import math


largest_prime = 0 # Global variable to store the largest prime number.
lock = threading.Lock() # Creates a lock to prevent multiple threads from changing largest_prime at the same time.

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True


# This is the function that each thread runs to check for prime numbers
# Each thread checks its own range of numbers from the work_queue
def worker(work_queue, end_time, lock):
    global largest_prime
    while not work_queue.empty():
            start, end = work_queue.get()
            for n in range(start, end):
                if time.time() >= end_time:
                    return 
                if is_prime(n):
                    with lock:
                        if n > largest_prime:
                            largest_prime = n
            work_queue.task_done()


# This function creates a queue to hold a range of numbers
# The function also creates the desired number of threads and splits the workload amongst them.
def threaded_pool():
    work_queue = Queue()
    num_threads = 5
    n = 100 
    range_per_thread = n // num_threads

    # Adds different ranges of numbesr for each thread to work on
    for i in range(num_threads):
        work_queue.put((i * range_per_thread, (i + 1) * range_per_thread))

    # Creating threads
    threads = []
    end_time = time.time() + 3 * 60
    for _ in range(num_threads):
        thread = threading.Thread(target=worker, args=(work_queue, end_time, lock))
        threads.append(thread)
        thread.start()

    # Wait for threads to finish and join
    for thread in threads:
        thread.join()
        
    return largest_prime


def fibonacci(n):
    a, b = 0, 1
    sequence = [a, b]
    for _ in range(2, n + 1):
        a, b = b, a + b
        sequence.append(b)
    return ' '.join(map(str, sequence))

    
def factorial(n):
    return math.factorial(n)


# Main control flow
if __name__ == "__main__":
    start_time = time.time()
    highest_prime = threaded_pool()
    end_time = time.time()

    print(f"Highest prime: {highest_prime}")
    print(f"Time taken: {end_time - start_time:.2f} seconds")

    fib_result = fibonacci(highest_prime)
    fact_result = factorial(highest_prime)
    print(f"Fibonacci of {highest_prime}: {fib_result}")
    print(f"Factorial of {highest_prime}: {fact_result}")
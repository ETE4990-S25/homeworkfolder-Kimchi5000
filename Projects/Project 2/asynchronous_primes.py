import asyncio
import math
import time
import sys

sys.set_int_max_str_digits(1000000)

# The functions used for this asynchronous application are the same as the multiprocessing one
# The 'async' keyword used before the function definitions creates each function as a coroutine.
# Creating the functions as a coroutine allows tasks to be suspended while waiting for a result and allows other tasks to be run in the meantime.
async def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True


# The 'await' keyword allows the current coroutine(find_highest_prime) to be suspended while waiting on the result of "is_prime".
async def find_highest_prime(shared_value, lock, time_limit):
    highest_prime = 0 # Start checking from 0
    start_time = time.time()

    while time.time() - start_time < time_limit:
        if await is_prime(highest_prime):
            async with lock:
                if highest_prime > shared_value[0]:
                    shared_value[0] = highest_prime # Only the highest prime value from each process is saved to the shared value.
        highest_prime += 1


async def fibonacci(n):
    fib_digit_limit = 1000
    if n > fib_digit_limit: 
        print(f"Fibonacci of {n} is too large to display.  This digit limit is {fib_digit_limit}.  Calculating new value(limit value)...")
        n = fib_digit_limit

    a, b = 0, 1
    for i in range(n):
        a, b = b, a + b
    print(f"The Fibonacci number for {n} is: {a}")

async def factorial(n):
    fact_digit_limit = 1000
    if n > fact_digit_limit: 
        print(f"Fibonacci of {n} is too large to display.  This digit limit is {fact_digit_limit}.  Calculating new value(limit value)...")
        n = fact_digit_limit

    result = math.factorial(n)
    print(f"The Factorial of {n} is: {result}")


# This is the main flow logic
# This is the event loop and it is the 'core' of the application that is responsible for suspending and scheduling tasks.
async def main():
    shared_value = [0]
    lock = asyncio.Lock()
    start_time = time.time()  
    num_tasks = 5
    time_limit = 180

    # A list of tasks is created
    # Each task is told to run the 'find_highest_prime' coroutine
    # Parameters: Each task is told to access and update the same variable(shared_value), 'lock' prevents tasks from access and updating 'shared_value' at the same time, each task has time limit of 180s
    tasks = [
        find_highest_prime(shared_value, lock, time_limit)
        for i in range(num_tasks)
    ]

    # 'asyncio.gather(*tasks)' schedules all the tasks to run concurrently.
    # Each task runs until completion or until it hits an 'await' statement.
    # If a task hits an await statement, it is suspended while the event loop allows other tasks to gather results.
    await asyncio.gather(*tasks)

    highest_prime = shared_value[0]

    print(f"Highest prime found in 3 minutes: {highest_prime}")

    
    # The coroutines for finding the fibonacci sequence and factorial run at the same time.
    fib_result = await fibonacci(highest_prime)
    fact_result = await factorial(highest_prime)
    print(f"Fibonacci of {highest_prime}: {fib_result}")
    print(f"Factorial of {highest_prime}: {fact_result}")
              
    total_time = time.time() - start_time 
    print(f"Total runtime: {total_time:.2f} seconds")


if __name__ == "__main__":
    asyncio.run(main())


import asyncio
import math
import time

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
async def find_highest_prime(start, end, end_time):
    highest_prime = 0
    for num in range(start, end):
        if time.time() >= end_time: 
            break
        if await is_prime(num):
            highest_prime = num
    return highest_prime

async def fibonacci(n):
    a, b = 0, 1
    sequence = [a, b]
    for _ in range(2, n + 1):
        a, b = b, a + b
        sequence.append(b)
    return ' '.join(map(str, sequence))

async def factorial(n):
    return math.factorial(n)


# This is the main flow logic
# This is the event loop and it is the 'core' of the application that is responsible for suspending and scheduling tasks.
async def main():
    start_time = time.time()  
    num_tasks = 5
    n = 100 
    range_per_task = n // num_tasks
    end_time = start_time + 3 * 60 

    # A list of tasks is created
    # Each task calls on the 'find_highest_prime' coroutine for the specified range.
    tasks = [
        find_highest_prime(i * range_per_task, (i + 1) * range_per_task, end_time)
        for i in range(num_tasks)
    ]

    # 'asyncio.gather(*tasks)' schedules all the tasks to run concurrently.
    # Each task runs until completion or until it hits an 'await' statement.
    # If a task hits an await statement, it is suspended while the event loop allows other tasks to gather results.
    # Since each task calls on the 'find_highest_prime' coroutine, the highest prime from each task is collected and returned to 'main()'.
    highest_primes = await asyncio.gather(*tasks)
    highest_prime = max(highest_primes) # Determines the highest prime from the results.

    print(f"Highest prime: {highest_prime}")

    
    # The coroutines for finding the fibonacci sequence and factorial are suspended until the main can determine the highest prime number.
    fibonacci = await fibonacci(highest_prime)
    factorial = await factorial(highest_prime)
    print(f"Fibonacci of {highest_prime}: {fibonacci}")
    print(f"Factorial of {highest_prime}: {factorial}")

    total_time = time.time() - start_time 
    print(f"Total runtime: {total_time:.2f} seconds")


if __name__ == "__main__":
    asyncio.run(main())


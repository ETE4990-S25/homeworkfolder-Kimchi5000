#Name: Namho Kye

# Basic Lambda Function; Create a lambda function that takes one arguments and returns even or odd. 
even_or_odd = lambda x: "Even" if x % 2 == 0 else "Odd"
number = 5
print(f"The number {number} is {even_or_odd(number)}.")


# Advanced lambda Function; Create a lambda function that takes a list and returns their sum 
sum_of_list = lambda lst: sum(lst)
numbers = [1, 2, 3]
print(f"The sum of the list {numbers} is {sum_of_list(numbers)}.")


# Sorting with Lambda 
people = [("Alice", 30), ("Bob", 25), ("Charlie", 35), ("David", 20)]
sorted_people = sorted(people, key=lambda person: person[1]) #The lambda function takes each tuple and returns the second element. The sorted() function sorts the ages in ascending order.
print("Sorted by age:", sorted_people)


# Filtering with Lambda - filter()
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
even_numbers = list(filter(lambda x: x % 2 == 0, numbers))
print("Even numbers:", even_numbers)


# Mapping with Lambda - map()
alist = [1, 2, 3]
print(list(
        map(
            lambda x: x * 2, #Doubles each number in the list
            alist
            )))


# Reducing with Lambda - reduce()
from functools import reduce

numbers = [1, 2, 3, 4, 5]
sum = reduce(lambda x, y: x + y, numbers) #The reduce() function applies the lambda function cumulatively in order to reduce to a single value
print(sum)


# Enumerate with or without Lambda - enumerate() 
animals = ['dog', 'cat', 'rabbit', 'hamster']

for index, animal in enumerate(animals, start=1):
    print(f"Animal {index} = {animal}")


# zip with or without lambda (may combine enumerate like in class) - zip()
names = ['Alice', 'Bob', 'Charlie']
ages = [25, 30, 35]

combined_list = list(enumerate(zip(names, ages), start=1))

for index, (name, age) in combined_list:
    print(f"Name: {name}, Age: {age}")
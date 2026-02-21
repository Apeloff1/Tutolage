// ============================================================================
// CODEDOCK QUANTUM NEXUS - CODING BIBLE CONTENT
// The Complete Day 1 to Godtier Programming Manual
// Version: 4.2.0 | 16 Comprehensive Chapters
// ============================================================================

import { BibleChapter } from '../../types';

export const CODING_BIBLE: BibleChapter[] = [
  // ========== BEGINNER TIER ==========
  {
    id: 'day1',
    day: 1,
    tier: 'beginner',
    title: 'The Genesis',
    subtitle: 'Your First Line of Code',
    icon: 'sunny',
    color: '#22C55E',
    unlocked: true,
    estimatedTime: '30 min',
    sections: [
      {
        title: 'Welcome, Future Developer',
        content: `Today marks the beginning of your coding journey. By the end of this chapter, you will understand what programming is and write your very first program.

Programming is simply giving instructions to a computer in a language it understands. Think of it like writing a recipe - each step must be clear and precise.

Every expert was once a beginner. The key is to start, make mistakes, and learn from them.`,
        tips: ['Every expert was once a beginner', 'Mistakes are how we learn', 'Take breaks when frustrated']
      },
      {
        title: 'What is Code?',
        content: `Code is text that tells a computer what to do. Just like how English has grammar rules, programming languages have syntax rules.

The computer reads your code line by line, from top to bottom, and executes each instruction in order. This is called sequential execution.`,
        code: `# This is a comment - the computer ignores it
# Comments help explain your code to humans

# Below is actual code that runs:
print("Hello, World!")

# The print() function displays text on screen`,
        language: 'python',
        tips: ['Comments start with # in Python', 'Indentation matters in Python', 'Strings need quotes']
      },
      {
        title: 'Variables: Storing Information',
        content: `Variables are like labeled boxes that store data. You give them a name and put something inside. You can then use that name to access the stored value.

Variable names should be descriptive - 'user_age' is better than 'x'.`,
        code: `# Creating variables
name = "Alex"
age = 25
is_learning = True
height = 5.9

# Using variables
print(name)
print("Age:", age)
print("Learning:", is_learning)`,
        language: 'python',
        tips: ['Use snake_case for variable names', 'Variables can be reassigned', 'Choose descriptive names']
      },
      {
        title: 'Data Types',
        content: `Different types of data need different storage. Python automatically detects the type, but understanding them is crucial.

The four basic types are:
- Strings: Text in quotes ("Hello")
- Integers: Whole numbers (42, -10, 0)
- Floats: Decimal numbers (3.14, -0.5)
- Booleans: True or False`,
        code: `# Strings - text data
greeting = "Hello, World!"
name = 'Alice'  # Single or double quotes work

# Integers - whole numbers
age = 25
count = -10
zero = 0

# Floats - decimal numbers
pi = 3.14159
temperature = -5.5

# Booleans - True or False
is_active = True
is_finished = False

# Check the type
print(type(greeting))  # <class 'str'>
print(type(age))       # <class 'int'>`,
        language: 'python'
      }
    ],
    exercises: [
      {
        id: 'ex1-1',
        title: 'Hello You!',
        description: 'Create a variable with your name and print a personalized greeting.',
        starterCode: '# Store your name in a variable\n# Then print "Hello, [your name]!"\n\n',
        language: 'python',
        hints: ['Use a variable like: my_name = "..."', 'Use print() to display output', 'You can combine strings with +'],
        solution: 'my_name = "Alex"\nprint("Hello, " + my_name + "!")'
      }
    ]
  },
  {
    id: 'day2',
    day: 2,
    tier: 'beginner',
    title: 'The Flow',
    subtitle: 'Making Decisions in Code',
    icon: 'git-branch',
    color: '#3B82F6',
    unlocked: true,
    estimatedTime: '45 min',
    sections: [
      {
        title: 'Conditional Statements',
        content: `Programs need to make decisions. The if statement checks if something is true and acts accordingly.

This is called conditional logic - the code runs only if a condition is met.`,
        code: `age = 18

if age >= 18:
    print("You are an adult")
    print("You can vote!")
else:
    print("You are a minor")
    print("You cannot vote yet")`,
        language: 'python',
        tips: ['Indentation defines code blocks', 'The colon : is required', 'else is optional']
      },
      {
        title: 'Multiple Conditions with elif',
        content: `Use elif (else if) to check multiple conditions in sequence. Python checks each condition from top to bottom and executes the first one that is True.`,
        code: `score = 85

if score >= 90:
    grade = "A"
    print("Excellent!")
elif score >= 80:
    grade = "B"
    print("Good job!")
elif score >= 70:
    grade = "C"
    print("Passing")
elif score >= 60:
    grade = "D"
    print("Needs improvement")
else:
    grade = "F"
    print("Failed")

print(f"Your grade: {grade}")`,
        language: 'python'
      },
      {
        title: 'Comparison Operators',
        content: `These operators compare values and return True or False. They are the foundation of conditional logic.

Available operators:
== Equal to
!= Not equal to
>  Greater than
<  Less than
>= Greater than or equal
<= Less than or equal`,
        code: `x = 10
y = 5

print(x == y)   # False - not equal
print(x != y)   # True  - not equal
print(x > y)    # True  - 10 > 5
print(x < y)    # False - 10 is not < 5
print(x >= 10)  # True  - 10 >= 10
print(y <= 5)   # True  - 5 <= 5

# Common mistake: = vs ==
# = assigns a value
# == compares values`,
        language: 'python',
        warning: 'Do not confuse = (assignment) with == (comparison)!'
      },
      {
        title: 'Logical Operators',
        content: `Combine multiple conditions with and, or, not. These let you create complex decision logic.

- and: Both conditions must be True
- or: At least one must be True  
- not: Reverses True/False`,
        code: `age = 25
has_license = True
has_car = False

# and - both must be true
if age >= 18 and has_license:
    print("Can drive legally")

# or - at least one must be true
if has_license or has_car:
    print("Has some driving capability")

# not - reverses the boolean
if not has_car:
    print("Does not have a car")

# Combining them
if age >= 18 and has_license and not has_car:
    print("Can drive but needs a car")`,
        language: 'python'
      }
    ]
  },
  {
    id: 'day3',
    day: 3,
    tier: 'beginner',
    title: 'The Loop',
    subtitle: 'Repeating Actions Efficiently',
    icon: 'repeat',
    color: '#8B5CF6',
    unlocked: true,
    estimatedTime: '45 min',
    sections: [
      {
        title: 'Why Loops?',
        content: `Instead of writing the same code 100 times, loops let you repeat actions automatically. This is one of programming's most powerful features.

Loops save time, reduce errors, and make code maintainable.`,
        code: `# Without loops (tedious and error-prone!)
print(1)
print(2)
print(3)
print(4)
print(5)

# With a loop (elegant and scalable!)
for i in range(1, 6):
    print(i)

# Same result, much better code!`,
        language: 'python'
      },
      {
        title: 'For Loops',
        content: `For loops iterate over a sequence - perfect when you know how many times to repeat. The range() function generates numbers.`,
        code: `# Loop through numbers
for num in range(5):
    print(num)  # 0, 1, 2, 3, 4

# range(start, stop, step)
for num in range(0, 10, 2):
    print(num)  # 0, 2, 4, 6, 8

# Loop through a list
fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
    print(f"I like {fruit}")

# Loop with index using enumerate
for index, fruit in enumerate(fruits):
    print(f"{index}: {fruit}")`,
        language: 'python',
        tips: ['range(5) gives 0,1,2,3,4 (not 5!)', 'enumerate() gives both index and value']
      },
      {
        title: 'While Loops',
        content: `While loops continue as long as a condition is true. Use them when you do not know in advance how many iterations you need.`,
        code: `count = 0

while count < 5:
    print(f"Count is: {count}")
    count += 1  # CRITICAL: Must update or infinite loop!

print("Loop finished!")

# Practical example: User input
password = ""
while password != "secret":
    password = input("Enter password: ")
print("Access granted!")`,
        language: 'python',
        warning: 'Always ensure your while loop can end! An infinite loop will freeze your program.'
      },
      {
        title: 'Break and Continue',
        content: `Control loop flow precisely:
- break: Exit the loop immediately
- continue: Skip to the next iteration`,
        code: `# break - exit when found
for i in range(10):
    if i == 5:
        print("Found 5, stopping!")
        break
    print(i)
# Output: 0, 1, 2, 3, 4, Found 5, stopping!

print("---")

# continue - skip specific values
for i in range(10):
    if i % 2 == 0:  # Skip even numbers
        continue
    print(i)
# Output: 1, 3, 5, 7, 9`,
        language: 'python'
      }
    ]
  },
  {
    id: 'day4',
    day: 4,
    tier: 'foundation',
    title: 'The Function',
    subtitle: 'Reusable Code Blocks',
    icon: 'cube',
    color: '#F59E0B',
    unlocked: true,
    estimatedTime: '50 min',
    sections: [
      {
        title: 'What are Functions?',
        content: `Functions are reusable blocks of code with a name. Write once, use many times. They help organize code, avoid repetition (DRY principle), and make testing easier.`,
        code: `# Defining a function
def greet(name):
    """Greet a person by name."""
    return f"Hello, {name}!"

# Using the function
message = greet("Alice")
print(message)  # Hello, Alice!

# Reuse with different inputs
print(greet("Bob"))    # Hello, Bob!
print(greet("Charlie")) # Hello, Charlie!`,
        language: 'python',
        tips: ['Function names should be verbs', 'Use docstrings to document', 'Keep functions small and focused']
      },
      {
        title: 'Parameters and Arguments',
        content: `Parameters are variables in the function definition (placeholders). Arguments are actual values you pass when calling the function.`,
        code: `def add(a, b):  # a, b are parameters
    """Add two numbers."""
    return a + b

result = add(5, 3)  # 5, 3 are arguments
print(result)  # 8

# Default parameters
def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"

print(greet("Alice"))           # Hello, Alice!
print(greet("Bob", "Hi"))       # Hi, Bob!
print(greet("Eve", greeting="Hey"))  # Hey, Eve!

# Multiple return values
def get_stats(numbers):
    return min(numbers), max(numbers), sum(numbers)

low, high, total = get_stats([1, 2, 3, 4, 5])
print(f"Min: {low}, Max: {high}, Sum: {total}")`,
        language: 'python'
      },
      {
        title: 'Return Values',
        content: `Functions can return values using the return statement. Without return, they return None. A function stops executing when it hits return.`,
        code: `def square(n):
    """Return the square of n."""
    return n * n

def print_square(n):
    """Print the square (no return)."""
    print(n * n)

result1 = square(4)        # result1 = 16
result2 = print_square(4)  # Prints 16, result2 = None

print(f"square returned: {result1}")
print(f"print_square returned: {result2}")

# Early return pattern
def is_adult(age):
    if age < 0:
        return False  # Invalid age
    return age >= 18`,
        language: 'python'
      },
      {
        title: 'Scope: Local vs Global',
        content: `Variables inside functions are local - they only exist inside that function. Global variables exist everywhere but should be used sparingly.`,
        code: `x = 10  # Global variable

def my_func():
    y = 5   # Local variable
    print(f"Inside function: x={x}, y={y}")

my_func()
print(f"Outside function: x={x}")
# print(y)  # ERROR! y does not exist here

# Modifying global (avoid if possible)
counter = 0

def increment():
    global counter
    counter += 1

increment()
print(counter)  # 1`,
        language: 'python',
        tips: ['Avoid global variables when possible', 'Pass values as parameters instead', 'Local scope is safer']
      }
    ]
  },
  {
    id: 'day5',
    day: 5,
    tier: 'foundation',
    title: 'The Collection',
    subtitle: 'Lists, Dicts, and More',
    icon: 'layers',
    color: '#EC4899',
    unlocked: true,
    estimatedTime: '60 min',
    sections: [
      {
        title: 'Lists: Ordered Collections',
        content: `Lists store multiple items in order. They can be modified (mutable) and can contain any data type, including other lists.`,
        code: `# Creating lists
numbers = [1, 2, 3, 4, 5]
mixed = ["hello", 42, True, 3.14]
empty = []

# Accessing items (0-indexed)
print(numbers[0])   # 1 (first)
print(numbers[-1])  # 5 (last)
print(numbers[1:3]) # [2, 3] (slice)

# Modifying lists
numbers.append(6)       # Add to end: [1,2,3,4,5,6]
numbers.insert(0, 0)    # Insert at index: [0,1,2,3,4,5,6]
numbers.remove(3)       # Remove value 3
del numbers[0]          # Delete by index
popped = numbers.pop()  # Remove and return last

print(numbers)`,
        language: 'python'
      },
      {
        title: 'List Operations',
        content: `Python provides powerful built-in operations for lists. Master these and you will be much more productive.`,
        code: `nums = [3, 1, 4, 1, 5, 9, 2, 6]

# Sorting
nums.sort()              # Sort in place: [1,1,2,3,4,5,6,9]
sorted_nums = sorted([3,1,2])  # Return new sorted list

# Reversing
nums.reverse()           # Reverse in place
reversed_nums = nums[::-1]  # Return reversed copy

# Useful functions
print(len(nums))    # Length: 8
print(sum(nums))    # Sum: 31
print(min(nums))    # Minimum: 1
print(max(nums))    # Maximum: 9

# List comprehension (powerful!)
squares = [x**2 for x in range(5)]
print(squares)  # [0, 1, 4, 9, 16]

evens = [x for x in range(10) if x % 2 == 0]
print(evens)  # [0, 2, 4, 6, 8]`,
        language: 'python'
      },
      {
        title: 'Dictionaries: Key-Value Pairs',
        content: `Dictionaries store key-value pairs. Think of them as real dictionaries: word -> definition. They provide O(1) lookup time.`,
        code: `# Creating a dictionary
person = {
    "name": "Alice",
    "age": 30,
    "city": "NYC",
    "skills": ["Python", "JavaScript"]
}

# Accessing values
print(person["name"])      # Alice
print(person.get("age"))   # 30
print(person.get("job", "Unknown"))  # Unknown (default)

# Modifying
person["email"] = "alice@example.com"  # Add new
person["age"] = 31                      # Update existing
del person["city"]                      # Delete

# Iterating
for key in person:
    print(f"{key}: {person[key]}")

for key, value in person.items():
    print(f"{key} = {value}")`,
        language: 'python'
      },
      {
        title: 'Sets and Tuples',
        content: `Sets: Unordered collections of unique items. Great for removing duplicates and set operations.
Tuples: Ordered but immutable (cannot be changed after creation).`,
        code: `# Sets - unique values only
numbers = {1, 2, 2, 3, 3, 3}
print(numbers)  # {1, 2, 3}

# Set operations
a = {1, 2, 3, 4}
b = {3, 4, 5, 6}
print(a | b)  # Union: {1, 2, 3, 4, 5, 6}
print(a & b)  # Intersection: {3, 4}
print(a - b)  # Difference: {1, 2}

# Remove duplicates from list
names = ["Alice", "Bob", "Alice", "Charlie", "Bob"]
unique = list(set(names))
print(unique)  # ['Alice', 'Bob', 'Charlie']

# Tuples - immutable
point = (10, 20)
x, y = point  # Unpacking
print(f"x={x}, y={y}")

# Tuples are great for returning multiple values
def get_dimensions():
    return (1920, 1080)

width, height = get_dimensions()`,
        language: 'python'
      }
    ]
  },
  {
    id: 'day6',
    day: 6,
    tier: 'foundation',
    title: 'The String',
    subtitle: 'Text Manipulation Mastery',
    icon: 'text',
    color: '#14B8A6',
    unlocked: true,
    estimatedTime: '40 min',
    sections: [
      {
        title: 'String Basics',
        content: `Strings are sequences of characters. They are immutable - you cannot change them in place, only create new strings.`,
        code: `# Creating strings
single = 'Hello'
double = "World"
multi = """This is a
multi-line string"""

# String concatenation
full = single + " " + double
print(full)  # Hello World

# String repetition
line = "-" * 20
print(line)  # --------------------

# Length
print(len(full))  # 11`,
        language: 'python'
      },
      {
        title: 'String Methods',
        content: `Python strings have many useful built-in methods. These return new strings (strings are immutable).`,
        code: `text = "  Hello, World!  "

# Case methods
print(text.upper())       # "  HELLO, WORLD!  "
print(text.lower())       # "  hello, world!  "
print(text.title())       # "  Hello, World!  "

# Whitespace
print(text.strip())       # "Hello, World!"
print(text.lstrip())      # "Hello, World!  "

# Finding and replacing
print(text.find("World")) # 9 (index)
print(text.replace("World", "Python"))

# Splitting and joining
words = "apple,banana,cherry".split(",")
print(words)  # ['apple', 'banana', 'cherry']

joined = " - ".join(words)
print(joined)  # "apple - banana - cherry"`,
        language: 'python'
      },
      {
        title: 'String Formatting',
        content: `Modern Python uses f-strings (formatted string literals) for easy and readable string formatting.`,
        code: `name = "Alice"
age = 30
score = 95.5

# f-strings (recommended)
print(f"Name: {name}, Age: {age}")
print(f"Score: {score:.1f}%")  # 1 decimal place
print(f"Name: {name:>10}")     # Right align, 10 chars

# Expressions in f-strings
print(f"In 5 years: {age + 5}")
print(f"Uppercase: {name.upper()}")

# Multi-line f-string
message = f"""
Dear {name},
Your score is {score}%.
{"Congratulations!" if score >= 90 else "Keep trying!"}
"""
print(message)`,
        language: 'python'
      }
    ]
  },
  // ========== INTERMEDIATE TIER ==========
  {
    id: 'day7',
    day: 7,
    tier: 'intermediate',
    title: 'The Class',
    subtitle: 'Object-Oriented Programming',
    icon: 'construct',
    color: '#06B6D4',
    unlocked: true,
    estimatedTime: '60 min',
    sections: [
      {
        title: 'What is OOP?',
        content: `Object-Oriented Programming (OOP) organizes code into "objects" that contain data (attributes) and behavior (methods). A class is a blueprint for creating objects.

OOP helps model real-world entities and makes code reusable and maintainable.`,
        code: `# A class is a blueprint
class Dog:
    # Class attribute (shared by all instances)
    species = "Canis familiaris"
    
    # Constructor - runs when creating object
    def __init__(self, name, breed, age):
        # Instance attributes (unique to each instance)
        self.name = name
        self.breed = breed
        self.age = age
    
    # Method - function inside class
    def bark(self):
        return f"{self.name} says Woof!"
    
    def describe(self):
        return f"{self.name} is a {self.age} year old {self.breed}"

# Creating objects (instances)
my_dog = Dog("Max", "Labrador", 3)
your_dog = Dog("Bella", "Poodle", 5)

print(my_dog.bark())      # Max says Woof!
print(your_dog.describe())  # Bella is a 5 year old Poodle`,
        language: 'python'
      },
      {
        title: 'Inheritance',
        content: `Classes can inherit from other classes, gaining their attributes and methods. This promotes code reuse and creates logical hierarchies.`,
        code: `class Animal:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def speak(self):
        raise NotImplementedError("Subclass must implement")
    
    def describe(self):
        return f"{self.name} is {self.age} years old"

class Dog(Animal):  # Inherits from Animal
    def speak(self):
        return f"{self.name} barks: Woof!"

class Cat(Animal):
    def speak(self):
        return f"{self.name} meows: Meow!"
    
    def purr(self):  # Cat-specific method
        return f"{self.name} purrs..."

# Usage
dog = Dog("Rex", 3)
cat = Cat("Whiskers", 5)

print(dog.speak())      # Rex barks: Woof!
print(cat.speak())      # Whiskers meows: Meow!
print(dog.describe())   # Rex is 3 years old (inherited)
print(cat.purr())       # Whiskers purrs...`,
        language: 'python'
      },
      {
        title: 'Encapsulation',
        content: `Encapsulation hides internal details and exposes only what is necessary. Use _ prefix for "protected" and __ for "private" attributes.`,
        code: `class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self._balance = balance  # Protected (convention)
        self.__pin = "1234"      # Private (name mangled)
    
    def deposit(self, amount):
        if amount > 0:
            self._balance += amount
            return True
        return False
    
    def withdraw(self, amount):
        if 0 < amount <= self._balance:
            self._balance -= amount
            return True
        return False
    
    def get_balance(self):
        return self._balance
    
    @property
    def balance(self):
        """Property for controlled access."""
        return self._balance

# Usage
account = BankAccount("Alice", 100)
account.deposit(50)
print(account.balance)     # 150
print(account.get_balance())  # 150`,
        language: 'python'
      }
    ]
  },
  {
    id: 'day8',
    day: 8,
    tier: 'intermediate',
    title: 'The File',
    subtitle: 'Reading and Writing Data',
    icon: 'document',
    color: '#F97316',
    unlocked: true,
    estimatedTime: '40 min',
    sections: [
      {
        title: 'Reading Files',
        content: `Python makes file handling easy. Always use the 'with' statement to ensure files are properly closed.`,
        code: `# Reading entire file
with open("example.txt", "r") as file:
    content = file.read()
    print(content)

# Reading line by line (memory efficient)
with open("example.txt", "r") as file:
    for line in file:
        print(line.strip())

# Reading into a list
with open("example.txt", "r") as file:
    lines = file.readlines()
    print(lines)`,
        language: 'python'
      },
      {
        title: 'Writing Files',
        content: `Write data to files using 'w' (overwrite) or 'a' (append) mode.`,
        code: `# Writing (overwrites existing content)
with open("output.txt", "w") as file:
    file.write("Hello, World!\\n")
    file.write("Line 2\\n")

# Appending (adds to existing content)
with open("output.txt", "a") as file:
    file.write("New line appended\\n")

# Writing multiple lines
lines = ["Line 1", "Line 2", "Line 3"]
with open("output.txt", "w") as file:
    file.writelines(line + "\\n" for line in lines)`,
        language: 'python'
      },
      {
        title: 'Working with JSON',
        content: `JSON is a popular format for storing and transmitting data. Python has built-in support.`,
        code: `import json

# Python dict to JSON string
data = {
    "name": "Alice",
    "age": 30,
    "skills": ["Python", "JavaScript"]
}

json_string = json.dumps(data, indent=2)
print(json_string)

# JSON string to Python dict
parsed = json.loads(json_string)
print(parsed["name"])  # Alice

# Save to file
with open("data.json", "w") as file:
    json.dump(data, file, indent=2)

# Load from file
with open("data.json", "r") as file:
    loaded = json.load(file)
    print(loaded)`,
        language: 'python'
      }
    ]
  },
  {
    id: 'day10',
    day: 10,
    tier: 'intermediate',
    title: 'The Error',
    subtitle: 'Exception Handling',
    icon: 'bug',
    color: '#EF4444',
    unlocked: true,
    estimatedTime: '45 min',
    sections: [
      {
        title: 'Why Handle Errors?',
        content: `Programs encounter errors. Without handling, they crash. With proper exception handling, they recover gracefully and provide useful feedback.`,
        code: `# Without handling - CRASH!
# result = 10 / 0  # ZeroDivisionError

# With handling - SAFE
try:
    result = 10 / 0
except ZeroDivisionError:
    print("Cannot divide by zero!")
    result = 0

print(f"Result: {result}")

# Catching the error object
try:
    x = int("not a number")
except ValueError as e:
    print(f"Error occurred: {e}")`,
        language: 'python'
      },
      {
        title: 'Try-Except-Else-Finally',
        content: `The complete error handling structure gives you fine-grained control.`,
        code: `def safe_divide(a, b):
    try:
        result = a / b
    except ZeroDivisionError:
        print("Error: Division by zero!")
        return None
    except TypeError:
        print("Error: Invalid types!")
        return None
    else:
        # Runs only if no exception occurred
        print("Division successful!")
        return result
    finally:
        # Always runs, regardless of exception
        print("Cleanup completed")

print(safe_divide(10, 2))   # Success!
print(safe_divide(10, 0))   # Division by zero!
print(safe_divide("a", 2))  # Invalid types!`,
        language: 'python'
      },
      {
        title: 'Raising Exceptions',
        content: `Create your own exceptions when validation fails or something goes wrong in your code.`,
        code: `def set_age(age):
    if not isinstance(age, int):
        raise TypeError("Age must be an integer!")
    if age < 0:
        raise ValueError("Age cannot be negative!")
    if age > 150:
        raise ValueError("Age seems unrealistic!")
    return age

# Using the function
try:
    user_age = set_age(-5)
except ValueError as e:
    print(f"Validation error: {e}")
except TypeError as e:
    print(f"Type error: {e}")

# Custom exception class
class InsufficientFundsError(Exception):
    def __init__(self, balance, amount):
        self.balance = balance
        self.amount = amount
        super().__init__(f"Cannot withdraw {amount}. Balance: {balance}")`,
        language: 'python'
      }
    ]
  },
  // ========== ADVANCED TIER ==========
  {
    id: 'day14',
    day: 14,
    tier: 'advanced',
    title: 'The Algorithm',
    subtitle: 'Problem Solving Patterns',
    icon: 'analytics',
    color: '#8B5CF6',
    unlocked: true,
    estimatedTime: '90 min',
    sections: [
      {
        title: 'Big O Notation',
        content: `Big O describes how code performance scales with input size. Understanding this helps you write efficient code.

Common complexities (best to worst):
- O(1) - Constant: Same time regardless of size
- O(log n) - Logarithmic: Time grows slowly (binary search)
- O(n) - Linear: Time grows proportionally
- O(n log n) - Linearithmic: Good sorting algorithms
- O(n^2) - Quadratic: Nested loops, avoid for large data`,
        code: `# O(1) - Constant time
def get_first(arr):
    return arr[0] if arr else None

# O(n) - Linear time
def find_max(arr):
    max_val = arr[0]
    for num in arr:  # Loops through all elements
        if num > max_val:
            max_val = num
    return max_val

# O(n^2) - Quadratic time (nested loops)
def has_duplicate(arr):
    for i in range(len(arr)):
        for j in range(i + 1, len(arr)):
            if arr[i] == arr[j]:
                return True
    return False

# O(n) - Better duplicate check with set
def has_duplicate_fast(arr):
    seen = set()
    for item in arr:
        if item in seen:
            return True
        seen.add(item)
    return False`,
        language: 'python'
      },
      {
        title: 'Two Pointers Pattern',
        content: `Use two pointers moving through data to solve problems efficiently. Common for array and string problems.`,
        code: `# Check if string is palindrome
def is_palindrome(s):
    s = s.lower().replace(" ", "")
    left, right = 0, len(s) - 1
    
    while left < right:
        if s[left] != s[right]:
            return False
        left += 1
        right -= 1
    return True

print(is_palindrome("A man a plan a canal Panama"))  # True

# Two Sum (sorted array)
def two_sum_sorted(nums, target):
    left, right = 0, len(nums) - 1
    
    while left < right:
        current_sum = nums[left] + nums[right]
        if current_sum == target:
            return [left, right]
        elif current_sum < target:
            left += 1
        else:
            right -= 1
    return []

print(two_sum_sorted([1, 2, 3, 4, 6], 6))  # [1, 3]`,
        language: 'python'
      },
      {
        title: 'Sliding Window Pattern',
        content: `Maintain a "window" over data that slides through. Efficient for subarray/substring problems.`,
        code: `# Maximum sum of k consecutive elements
def max_sum_subarray(arr, k):
    if len(arr) < k:
        return None
    
    # Calculate first window
    window_sum = sum(arr[:k])
    max_sum = window_sum
    
    # Slide the window
    for i in range(k, len(arr)):
        window_sum += arr[i] - arr[i - k]  # Add new, remove old
        max_sum = max(max_sum, window_sum)
    
    return max_sum

print(max_sum_subarray([1, 4, 2, 10, 2, 3, 1, 0, 20], 4))  # 24

# Longest substring without repeating characters
def longest_unique_substring(s):
    char_set = set()
    left = 0
    max_length = 0
    
    for right in range(len(s)):
        while s[right] in char_set:
            char_set.remove(s[left])
            left += 1
        char_set.add(s[right])
        max_length = max(max_length, right - left + 1)
    
    return max_length

print(longest_unique_substring("abcabcbb"))  # 3`,
        language: 'python'
      },
      {
        title: 'Hash Map Pattern',
        content: `Use hash maps (dictionaries) for O(1) lookup. Transforms many O(n^2) problems to O(n).`,
        code: `# Two Sum (unsorted) - Classic interview question
def two_sum(nums, target):
    seen = {}  # value -> index
    
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    
    return []

print(two_sum([2, 7, 11, 15], 9))  # [0, 1]

# Group anagrams
def group_anagrams(words):
    groups = {}
    
    for word in words:
        key = "".join(sorted(word))
        if key not in groups:
            groups[key] = []
        groups[key].append(word)
    
    return list(groups.values())

words = ["eat", "tea", "tan", "ate", "nat", "bat"]
print(group_anagrams(words))
# [['eat', 'tea', 'ate'], ['tan', 'nat'], ['bat']]`,
        language: 'python'
      }
    ]
  },
  {
    id: 'day21',
    day: 21,
    tier: 'advanced',
    title: 'The Async',
    subtitle: 'Concurrent Programming',
    icon: 'flash',
    color: '#F59E0B',
    unlocked: true,
    estimatedTime: '75 min',
    sections: [
      {
        title: 'Understanding Async',
        content: `Asynchronous programming allows code to run without blocking while waiting for I/O operations. Perfect for API calls, file operations, and network requests.`,
        code: `import asyncio

# Synchronous (blocking) - slow!
def sync_fetch():
    import time
    time.sleep(1)  # Blocks everything
    return "data"

# Asynchronous (non-blocking) - fast!
async def async_fetch():
    await asyncio.sleep(1)  # Does not block
    return "data"

# The difference: async allows other code to run while waiting`,
        language: 'python'
      },
      {
        title: 'Async/Await in Python',
        content: `Use async def to define coroutines and await to call them. asyncio.gather() runs multiple coroutines concurrently.`,
        code: `import asyncio

async def fetch_data(url, delay):
    print(f"Fetching {url}...")
    await asyncio.sleep(delay)  # Simulate network delay
    print(f"Got data from {url}")
    return f"Data from {url}"

async def main():
    # Sequential - takes 3 seconds
    # result1 = await fetch_data("api/users", 1)
    # result2 = await fetch_data("api/posts", 1)
    # result3 = await fetch_data("api/comments", 1)
    
    # Concurrent - takes 1 second!
    results = await asyncio.gather(
        fetch_data("api/users", 1),
        fetch_data("api/posts", 1),
        fetch_data("api/comments", 1)
    )
    
    for result in results:
        print(result)

# Run the async main function
# asyncio.run(main())`,
        language: 'python'
      },
      {
        title: 'JavaScript Async',
        content: `JavaScript is built for async programming with Promises and async/await. Almost all I/O is async by default.`,
        code: `// Async function returns a Promise
async function fetchUser(id) {
  const response = await fetch(\`/api/users/\${id}\`);
  if (!response.ok) {
    throw new Error('User not found');
  }
  const data = await response.json();
  return data;
}

// Using with .then/.catch
fetchUser(1)
  .then(user => console.log(user))
  .catch(err => console.error(err));

// Using with async/await (cleaner)
async function main() {
  try {
    const user = await fetchUser(1);
    console.log(user);
    
    // Parallel requests
    const [users, posts] = await Promise.all([
      fetch('/api/users').then(r => r.json()),
      fetch('/api/posts').then(r => r.json())
    ]);
  } catch (err) {
    console.error('Error:', err.message);
  }
}`,
        language: 'javascript'
      }
    ]
  },
  // ========== EXPERT TIER ==========
  {
    id: 'day30',
    day: 30,
    tier: 'expert',
    title: 'The Pattern',
    subtitle: 'Design Patterns',
    icon: 'git-network',
    color: '#06B6D4',
    unlocked: true,
    estimatedTime: '90 min',
    sections: [
      {
        title: 'Singleton Pattern',
        content: `Ensure a class has only one instance. Useful for configurations, database connections, loggers.`,
        code: `class Database:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            print("Creating new database connection")
            cls._instance = super().__new__(cls)
            cls._instance.connection = "Connected to DB"
        return cls._instance
    
    def query(self, sql):
        return f"Executing: {sql}"

# Both variables point to the SAME instance
db1 = Database()
db2 = Database()

print(db1 is db2)  # True
print(db1.query("SELECT * FROM users"))`,
        language: 'python'
      },
      {
        title: 'Factory Pattern',
        content: `Create objects without specifying the exact class. Provides flexibility and loose coupling.`,
        code: `from abc import ABC, abstractmethod

class Animal(ABC):
    @abstractmethod
    def speak(self):
        pass

class Dog(Animal):
    def speak(self):
        return "Woof!"

class Cat(Animal):
    def speak(self):
        return "Meow!"

class Bird(Animal):
    def speak(self):
        return "Tweet!"

class AnimalFactory:
    @staticmethod
    def create(animal_type: str) -> Animal:
        animals = {
            "dog": Dog,
            "cat": Cat,
            "bird": Bird
        }
        if animal_type.lower() not in animals:
            raise ValueError(f"Unknown animal: {animal_type}")
        return animals[animal_type.lower()]()

# Usage - no need to know specific classes
pet1 = AnimalFactory.create("dog")
pet2 = AnimalFactory.create("cat")

print(pet1.speak())  # Woof!
print(pet2.speak())  # Meow!`,
        language: 'python'
      },
      {
        title: 'Observer Pattern',
        content: `Objects subscribe to events and get notified when they occur. Foundation of event-driven programming.`,
        code: `class EventEmitter:
    def __init__(self):
        self._listeners = {}
    
    def on(self, event: str, callback):
        if event not in self._listeners:
            self._listeners[event] = []
        self._listeners[event].append(callback)
        return self  # Allow chaining
    
    def off(self, event: str, callback):
        if event in self._listeners:
            self._listeners[event].remove(callback)
    
    def emit(self, event: str, data=None):
        for callback in self._listeners.get(event, []):
            callback(data)

# Usage
emitter = EventEmitter()

def on_login(user):
    print(f"User {user} logged in")

def send_welcome(user):
    print(f"Welcome email sent to {user}")

emitter.on("login", on_login)
emitter.on("login", send_welcome)

emitter.emit("login", "Alice")
# Output:
# User Alice logged in
# Welcome email sent to Alice`,
        language: 'python'
      },
      {
        title: 'Strategy Pattern',
        content: `Define a family of algorithms, encapsulate each one, and make them interchangeable. Great for varying behavior.`,
        code: `from abc import ABC, abstractmethod

class PaymentStrategy(ABC):
    @abstractmethod
    def pay(self, amount: float) -> str:
        pass

class CreditCardPayment(PaymentStrategy):
    def __init__(self, card_number: str):
        self.card_number = card_number
    
    def pay(self, amount: float) -> str:
        return f"Paid ${amount} with card ending in {self.card_number[-4:]}"

class PayPalPayment(PaymentStrategy):
    def __init__(self, email: str):
        self.email = email
    
    def pay(self, amount: float) -> str:
        return f"Paid ${amount} via PayPal ({self.email})"

class ShoppingCart:
    def __init__(self):
        self.items = []
        self.payment_strategy = None
    
    def set_payment_strategy(self, strategy: PaymentStrategy):
        self.payment_strategy = strategy
    
    def checkout(self):
        total = sum(item["price"] for item in self.items)
        return self.payment_strategy.pay(total)

# Usage
cart = ShoppingCart()
cart.items = [{"name": "Book", "price": 20}, {"name": "Pen", "price": 5}]

cart.set_payment_strategy(CreditCardPayment("1234567890123456"))
print(cart.checkout())  # Paid $25 with card ending in 3456`,
        language: 'python'
      }
    ]
  },
  // ========== GODTIER ==========
  {
    id: 'godtier',
    day: 100,
    tier: 'godtier',
    title: 'The Mastery',
    subtitle: 'Principles of Excellence',
    icon: 'trophy',
    color: '#FFD700',
    unlocked: true,
    estimatedTime: '120 min',
    sections: [
      {
        title: 'SOLID Principles',
        content: `The foundation of maintainable, scalable code. These five principles guide object-oriented design.

S - Single Responsibility: One class, one job
O - Open/Closed: Open for extension, closed for modification
L - Liskov Substitution: Subtypes must be substitutable for their base types
I - Interface Segregation: Many specific interfaces are better than one general interface
D - Dependency Inversion: Depend on abstractions, not concretions`,
        tips: ['These take years to master', 'Apply gradually, not all at once', 'Prioritize readability over rigid adherence']
      },
      {
        title: 'Clean Code Commandments',
        content: `The principles that separate good code from great code:

1. Names should reveal intent
2. Functions should do one thing
3. Comments explain WHY, not WHAT
4. Handle errors gracefully
5. Write tests before code (TDD)
6. Refactor continuously
7. Keep it simple (KISS)
8. Do not repeat yourself (DRY)
9. You are not gonna need it (YAGNI)
10. Leave code better than you found it`,
        code: `# BAD - unclear names, does too much
def calc(a, b, t):
    if t == 1:
        return a + b
    elif t == 2:
        return a - b
    elif t == 3:
        r = a + b
        print(r)
        save_to_db(r)
        send_email(r)
        return r

# GOOD - clear names, single responsibility
def add(first_number: int, second_number: int) -> int:
    """Add two numbers and return the result."""
    return first_number + second_number

def subtract(first_number: int, second_number: int) -> int:
    """Subtract second number from first."""
    return first_number - second_number

def process_calculation(result: int) -> None:
    """Handle side effects of a calculation."""
    save_to_db(result)
    send_email(result)`,
        language: 'python'
      },
      {
        title: 'The Godtier Mindset',
        content: `Technical skills get you hired. These principles make you exceptional:

- Read more code than you write
- Teach others to deepen your understanding
- Embrace failure as feedback
- Build projects that solve real problems
- Contribute to open source
- Stay curious - technologies change constantly
- Code is communication - write for humans first
- Premature optimization is the root of all evil
- Simple is better than complex
- Done is better than perfect

"First, solve the problem. Then, write the code." - John Johnson`,
        tips: [
          'The best code is code you do not have to write',
          'Debugging is twice as hard as writing code',
          'If you are not embarrassed by v1, you launched too late'
        ]
      },
      {
        title: 'Your Journey Continues',
        content: `Congratulations on reaching this point. You have learned:

- Fundamentals: Variables, Types, Control Flow
- Functions and Data Structures
- Object-Oriented Programming
- Error Handling and File I/O
- Algorithms and Patterns
- Async Programming
- Design Patterns
- Clean Code Principles

But remember - mastery is a journey, not a destination. The field evolves constantly. Keep building. Keep learning. Keep shipping.

Welcome to Godtier.`,
      }
    ]
  }
];

export const getTierColor = (tier: string): string => {
  const colors: Record<string, string> = {
    beginner: '#22C55E',
    foundation: '#3B82F6',
    intermediate: '#8B5CF6',
    advanced: '#F59E0B',
    expert: '#EC4899',
    godtier: '#FFD700',
  };
  return colors[tier] || '#6366F1';
};

export const getBibleStats = (completedChapters: Record<string, boolean>) => {
  const completedCount = Object.values(completedChapters).filter(Boolean).length;
  const totalChapters = CODING_BIBLE.length;
  const percentage = Math.round((completedCount / totalChapters) * 100);
  return { completedCount, totalChapters, percentage };
};

export default CODING_BIBLE;

// ============================================================================
// CODEDOCK QUANTUM NEXUS - THE COMPLETE CODING BIBLE
// A Year-Long Journey from Zero to Mastery
// 52 Weeks • 12 Months • Infinite Possibilities
// ============================================================================
// "The journey of a thousand miles begins with a single line of code."
// ============================================================================

import { BibleChapter } from '../../types';

// ============================================================================
// YEAR-LONG CURRICULUM STRUCTURE
// ============================================================================
// Month 1-2:   AWAKENING      (Weeks 1-8)   - First Steps & Fundamentals
// Month 3-4:   FOUNDATION     (Weeks 9-16)  - Building Blocks
// Month 5-6:   EXPANSION      (Weeks 17-24) - Growing Your Skills
// Month 7-8:   DEPTH          (Weeks 25-32) - Going Deeper
// Month 9-10:  MASTERY        (Weeks 33-40) - Advanced Concepts
// Month 11-12: TRANSCENDENCE  (Weeks 41-52) - Expert & Beyond
// ============================================================================

export const CODING_BIBLE: BibleChapter[] = [
  // ═══════════════════════════════════════════════════════════════════════════
  // MONTH 1-2: AWAKENING - Your First Steps into Code
  // ═══════════════════════════════════════════════════════════════════════════
  {
    id: 'week1',
    day: 1,
    tier: 'beginner',
    title: 'The Awakening',
    subtitle: 'Your First Line of Code',
    icon: 'sunny',
    color: '#22C55E',
    unlocked: true,
    estimatedTime: '45 min',
    sections: [
      {
        title: 'Welcome to Your Journey',
        content: `Welcome, future developer. Today marks the beginning of something extraordinary.

You are about to learn the language of the future - the ability to create, to build, to bring ideas to life with nothing but your thoughts and a keyboard.

Programming is not about memorizing syntax. It is about learning to think in new ways, to break down problems into smaller pieces, and to express solutions with precision and elegance.

Take a deep breath. You belong here.`,
        tips: ['Every expert was once a complete beginner', 'Progress over perfection', 'Embrace confusion - it means you are learning']
      },
      {
        title: 'What is Programming?',
        content: `At its core, programming is communication. You are learning to speak to computers.

Computers are incredibly powerful but also incredibly literal. They do exactly what you tell them - nothing more, nothing less. This is both their strength and the source of most bugs.

Think of code as a recipe. Each instruction must be clear, precise, and in the right order. The computer follows your recipe step by step, from top to bottom.`,
        code: `# Your first program - a tradition dating back decades
# Every programmer starts here

print("Hello, World!")

# Congratulations! You just gave a computer an instruction
# and it listened.`,
        language: 'python',
        tips: ['print() displays text on the screen', 'Text must be in quotes', 'Python reads top to bottom']
      },
      {
        title: 'Variables: Giving Names to Things',
        content: `Variables are containers for information. Think of them as labeled boxes where you store data for later use.

When you create a variable, you are telling the computer: "Remember this value, and when I use this name, give me the value back."

Choose names that describe what the variable holds. Your future self will thank you.`,
        code: `# Creating variables is like labeling boxes
name = "Ada"           # A box labeled 'name' containing "Ada"
age = 28               # A box labeled 'age' containing 28
is_programmer = True   # A box labeled 'is_programmer' containing True

# Using variables
print(name)            # Opens the 'name' box, shows "Ada"
print(age)             # Shows 28

# Variables can change (that is why they are called variables!)
age = 29               # Birthday! Update the box
print(age)             # Now shows 29`,
        language: 'python'
      },
      {
        title: 'The Four Fundamental Types',
        content: `Data comes in different types, just like in real life. Python automatically recognizes these types:

• Strings (str): Text, always in quotes. "Hello" or 'Hello'
• Integers (int): Whole numbers. 42, -7, 0
• Floats (float): Decimal numbers. 3.14, -0.5, 2.0
• Booleans (bool): True or False. Nothing else.

Understanding types helps you understand what operations are possible.`,
        code: `# Strings - for text
greeting = "Hello, World!"
name = 'Alice'  # Single or double quotes both work

# Integers - whole numbers
count = 42
negative = -7
zero = 0

# Floats - decimal numbers
pi = 3.14159
temperature = -5.5

# Booleans - only True or False
is_learning = True
is_finished = False

# Check the type of anything
print(type(greeting))  # <class 'str'>
print(type(count))     # <class 'int'>
print(type(pi))        # <class 'float'>
print(type(is_learning))  # <class 'bool'>`,
        language: 'python'
      }
    ],
    exercises: [
      {
        id: 'w1-ex1',
        title: 'Your Personal Introduction',
        description: 'Create variables for your name, age, and a fun fact about yourself. Print them all.',
        starterCode: '# Create your variables here\n\n# Print a nice introduction\n',
        language: 'python',
        hints: ['Use descriptive variable names', 'Strings need quotes, numbers do not', 'You can use + to join strings']
      }
    ]
  },
  {
    id: 'week2',
    day: 8,
    tier: 'beginner',
    title: 'The Conversation',
    subtitle: 'Input, Output & Basic Math',
    icon: 'chatbubbles',
    color: '#3B82F6',
    unlocked: true,
    estimatedTime: '50 min',
    sections: [
      {
        title: 'Talking to Your Program',
        content: `Programs become interactive when they can receive input from users. The input() function pauses your program and waits for the user to type something.

This is how you create conversations between humans and computers.`,
        code: `# Getting input from the user
name = input("What is your name? ")
print("Hello, " + name + "!")

# input() always returns a string
age_text = input("How old are you? ")
print(type(age_text))  # <class 'str'> - it is text!

# Convert to number for math
age = int(age_text)
print("Next year you will be", age + 1)`,
        language: 'python',
        tips: ['input() always returns a string', 'Use int() to convert to integer', 'Use float() for decimal numbers']
      },
      {
        title: 'The Art of Arithmetic',
        content: `Python is a powerful calculator. Master these operators:

+ Addition
- Subtraction
* Multiplication
/ Division (always returns float)
// Floor division (rounds down to integer)
% Modulo (remainder after division)
** Exponentiation (power)`,
        code: `# Basic math
print(10 + 3)   # 13
print(10 - 3)   # 7
print(10 * 3)   # 30
print(10 / 3)   # 3.333...

# Special operators
print(10 // 3)  # 3 (floor division)
print(10 % 3)   # 1 (remainder)
print(10 ** 3)  # 1000 (10 cubed)

# Order of operations (PEMDAS)
result = 2 + 3 * 4      # 14, not 20
result = (2 + 3) * 4    # 20, parentheses first

# Compound assignment
count = 10
count += 5   # Same as: count = count + 5
count *= 2   # Same as: count = count * 2
print(count) # 30`,
        language: 'python'
      },
      {
        title: 'String Magic',
        content: `Strings have their own special operations. Learn to manipulate text like a pro.`,
        code: `# Concatenation (joining strings)
first = "Hello"
second = "World"
combined = first + " " + second
print(combined)  # "Hello World"

# Repetition
line = "-" * 20
print(line)  # "--------------------"

# f-strings (formatted strings) - the modern way
name = "Alice"
age = 30
message = f"My name is {name} and I am {age} years old"
print(message)

# You can put any expression in {}
print(f"In 5 years I will be {age + 5}")
print(f"My name in caps: {name.upper()}")`,
        language: 'python'
      }
    ]
  },
  {
    id: 'week3',
    day: 15,
    tier: 'beginner',
    title: 'The Crossroads',
    subtitle: 'Making Decisions with If/Else',
    icon: 'git-branch',
    color: '#8B5CF6',
    unlocked: true,
    estimatedTime: '55 min',
    sections: [
      {
        title: 'The Power of Choice',
        content: `Until now, your programs have been linear - they execute every line from top to bottom. But real programs need to make decisions.

The if statement is your first tool for controlling flow. It lets your program choose different paths based on conditions.`,
        code: `# The basic if statement
temperature = 35

if temperature > 30:
    print("It is hot outside!")
    print("Stay hydrated!")

# The code inside runs ONLY if the condition is True
# Notice the indentation - it defines the code block`,
        language: 'python',
        tips: ['Indentation matters in Python', 'Use 4 spaces (or 1 tab) for each level', 'The colon : is required after the condition']
      },
      {
        title: 'Two Paths: If and Else',
        content: `Often you want to do one thing if a condition is true, and something else if it is false. That is where else comes in.`,
        code: `age = 16

if age >= 18:
    print("You are an adult")
    print("You can vote!")
else:
    print("You are a minor")
    print("You cannot vote yet")

# Only ONE of these blocks will run, never both`,
        language: 'python'
      },
      {
        title: 'Multiple Paths: Elif',
        content: `Sometimes you need more than two options. The elif (else if) lets you check multiple conditions in sequence.`,
        code: `score = 78

if score >= 90:
    grade = "A"
    message = "Excellent!"
elif score >= 80:
    grade = "B"
    message = "Good job!"
elif score >= 70:
    grade = "C"
    message = "Satisfactory"
elif score >= 60:
    grade = "D"
    message = "Needs improvement"
else:
    grade = "F"
    message = "Please see the teacher"

print(f"Grade: {grade}")
print(message)

# Python checks each condition from top to bottom
# It runs the FIRST block whose condition is True
# Then skips all the rest`,
        language: 'python'
      },
      {
        title: 'Comparison Operators',
        content: `To make decisions, you need to compare values. These operators return True or False.

== Equal to (not = which is assignment!)
!= Not equal to
> Greater than
< Less than
>= Greater than or equal
<= Less than or equal`,
        code: `x = 10
y = 5

print(x == y)   # False
print(x != y)   # True
print(x > y)    # True
print(x < y)    # False
print(x >= 10)  # True
print(y <= 5)   # True

# String comparison
name = "Alice"
print(name == "Alice")  # True
print(name == "alice")  # False (case sensitive!)
print(name.lower() == "alice")  # True`,
        language: 'python',
        warning: 'Do not confuse = (assignment) with == (comparison). This is the #1 beginner mistake!'
      }
    ]
  },
  {
    id: 'week4',
    day: 22,
    tier: 'beginner',
    title: 'The Logic',
    subtitle: 'Combining Conditions',
    icon: 'git-merge',
    color: '#EC4899',
    unlocked: true,
    estimatedTime: '45 min',
    sections: [
      {
        title: 'Logical Operators',
        content: `Sometimes one condition is not enough. Logical operators let you combine multiple conditions.

and - Both conditions must be True
or - At least one condition must be True
not - Reverses True to False, and False to True`,
        code: `age = 25
has_license = True
has_car = False

# and - BOTH must be true
if age >= 18 and has_license:
    print("You can legally drive")

# or - AT LEAST ONE must be true
if has_license or has_car:
    print("You have some driving capability")

# not - reverses the boolean
if not has_car:
    print("You need a car")

# Combining them
if age >= 18 and has_license and not has_car:
    print("You can drive, but you need a car first!")`,
        language: 'python'
      },
      {
        title: 'Nested Conditions',
        content: `You can put if statements inside other if statements. This is called nesting.`,
        code: `user_type = "member"
years_member = 3

if user_type == "member":
    print("Welcome back!")
    
    if years_member >= 5:
        print("You are a Gold member!")
        discount = 20
    elif years_member >= 2:
        print("You are a Silver member!")
        discount = 10
    else:
        print("You are a Bronze member!")
        discount = 5
    
    print(f"Your discount: {discount}%")
else:
    print("Please sign up for membership benefits!")`,
        language: 'python',
        tips: ['Keep nesting shallow when possible', 'Deep nesting can be hard to read', 'Consider using functions to simplify']
      },
      {
        title: 'Truthiness',
        content: `In Python, values can be "truthy" or "falsy" - they act like True or False in conditions.

Falsy values: False, None, 0, 0.0, "" (empty string), [] (empty list), {} (empty dict)
Everything else is truthy.`,
        code: `# These are all "falsy"
if not 0:
    print("0 is falsy")

if not "":
    print("Empty string is falsy")

if not []:
    print("Empty list is falsy")

# Practical use
name = input("Enter your name: ")

if name:  # True if name is not empty
    print(f"Hello, {name}!")
else:
    print("You did not enter a name.")

# This is cleaner than: if name != ""`,
        language: 'python'
      }
    ]
  },
  {
    id: 'week5',
    day: 29,
    tier: 'beginner',
    title: 'The Repetition',
    subtitle: 'Loops - Doing Things Over and Over',
    icon: 'repeat',
    color: '#F59E0B',
    unlocked: true,
    estimatedTime: '60 min',
    sections: [
      {
        title: 'Why Loops Matter',
        content: `Imagine you need to print numbers 1 to 100. Without loops, you would write 100 print statements. With loops, you write 2 lines.

Loops are one of programming's most powerful features. They let you automate repetition.`,
        code: `# Without loops (painful!)
print(1)
print(2)
print(3)
# ... 97 more lines ...

# With a loop (elegant!)
for i in range(1, 101):
    print(i)

# Same result, infinitely better code
# This is the power of abstraction`,
        language: 'python'
      },
      {
        title: 'The For Loop',
        content: `Use for loops when you know how many times to repeat, or when iterating over a collection.`,
        code: `# Looping through a range of numbers
for number in range(5):
    print(number)
# Output: 0, 1, 2, 3, 4

# range(start, stop, step)
for number in range(2, 10, 2):
    print(number)
# Output: 2, 4, 6, 8

# Looping through a list
fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
    print(f"I love {fruit}!")

# Looping with index using enumerate
for index, fruit in enumerate(fruits):
    print(f"{index}: {fruit}")`,
        language: 'python',
        tips: ['range(5) gives 0,1,2,3,4 - not including 5!', 'enumerate() gives both index and value', 'The loop variable (fruit, number) is created automatically']
      },
      {
        title: 'The While Loop',
        content: `Use while loops when you do not know how many iterations you need - the loop continues as long as a condition is True.`,
        code: `# Basic while loop
count = 0
while count < 5:
    print(count)
    count += 1  # CRITICAL! Without this, infinite loop!
# Output: 0, 1, 2, 3, 4

# Practical example: User input validation
password = ""
while password != "secret":
    password = input("Enter password: ")
    if password != "secret":
        print("Wrong password, try again.")
print("Access granted!")

# Another example: Game loop
playing = True
while playing:
    action = input("Enter action (quit to exit): ")
    if action == "quit":
        playing = False
    else:
        print(f"You chose: {action}")
print("Thanks for playing!")`,
        language: 'python',
        warning: 'Always ensure your while loop can end! An infinite loop will freeze your program. Make sure the condition eventually becomes False.'
      },
      {
        title: 'Loop Control: Break and Continue',
        content: `Sometimes you need finer control over loops. break exits immediately. continue skips to the next iteration.`,
        code: `# break - exit the loop early
for i in range(10):
    if i == 5:
        print("Found 5, stopping!")
        break
    print(i)
# Output: 0, 1, 2, 3, 4, Found 5, stopping!

# continue - skip this iteration
for i in range(10):
    if i % 2 == 0:  # Skip even numbers
        continue
    print(i)
# Output: 1, 3, 5, 7, 9

# Real example: Search
numbers = [4, 7, 2, 9, 1, 5, 8]
target = 9

for num in numbers:
    if num == target:
        print(f"Found {target}!")
        break
else:  # This else belongs to for, runs if no break
    print(f"{target} not found")`,
        language: 'python'
      }
    ]
  },
  {
    id: 'week6',
    day: 36,
    tier: 'beginner',
    title: 'The Collection',
    subtitle: 'Lists - Your First Data Structure',
    icon: 'list',
    color: '#14B8A6',
    unlocked: true,
    estimatedTime: '55 min',
    sections: [
      {
        title: 'Understanding Lists',
        content: `A list is an ordered collection of items. Think of it as a numbered container where each slot holds a value.

Lists are mutable - you can change them after creation. They can hold any type of data, even mixed types.`,
        code: `# Creating lists
numbers = [1, 2, 3, 4, 5]
fruits = ["apple", "banana", "cherry"]
mixed = [1, "hello", True, 3.14]
empty = []

# Lists are ordered and indexed (starting at 0)
print(fruits[0])   # "apple" (first item)
print(fruits[1])   # "banana" (second item)
print(fruits[-1])  # "cherry" (last item)
print(fruits[-2])  # "banana" (second to last)

# Length of a list
print(len(fruits))  # 3`,
        language: 'python'
      },
      {
        title: 'Modifying Lists',
        content: `Lists are mutable, meaning you can change them in place.`,
        code: `fruits = ["apple", "banana", "cherry"]

# Change an item
fruits[0] = "apricot"
print(fruits)  # ["apricot", "banana", "cherry"]

# Add items
fruits.append("date")       # Add to end
fruits.insert(1, "blueberry")  # Insert at position

# Remove items
fruits.remove("banana")     # Remove by value
del fruits[0]               # Remove by index
last = fruits.pop()         # Remove and return last item
first = fruits.pop(0)       # Remove and return first item

# Combine lists
more_fruits = ["elderberry", "fig"]
all_fruits = fruits + more_fruits  # Creates new list
fruits.extend(more_fruits)         # Modifies in place`,
        language: 'python'
      },
      {
        title: 'List Slicing',
        content: `Slicing lets you extract portions of a list. The syntax is list[start:stop:step].`,
        code: `numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

# Basic slicing [start:stop] - stop is NOT included
print(numbers[2:5])    # [2, 3, 4]
print(numbers[:4])     # [0, 1, 2, 3] (from start)
print(numbers[6:])     # [6, 7, 8, 9] (to end)
print(numbers[:])      # Full copy of list

# With step [start:stop:step]
print(numbers[::2])    # [0, 2, 4, 6, 8] (every 2nd)
print(numbers[1::2])   # [1, 3, 5, 7, 9] (odd indices)
print(numbers[::-1])   # [9, 8, 7, 6, 5, 4, 3, 2, 1, 0] (reversed!)

# Negative indices work too
print(numbers[-3:])    # [7, 8, 9] (last 3)
print(numbers[:-3])    # [0, 1, 2, 3, 4, 5, 6] (all but last 3)`,
        language: 'python'
      },
      {
        title: 'List Comprehensions',
        content: `List comprehensions are a powerful, Pythonic way to create lists. They combine loops and conditions in a single expression.`,
        code: `# Traditional way
squares = []
for x in range(10):
    squares.append(x ** 2)

# List comprehension (same result, one line!)
squares = [x ** 2 for x in range(10)]
print(squares)  # [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]

# With condition (filtering)
evens = [x for x in range(20) if x % 2 == 0]
print(evens)  # [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]

# Transform and filter
words = ["hello", "world", "python", "code"]
long_upper = [w.upper() for w in words if len(w) > 4]
print(long_upper)  # ['HELLO', 'WORLD', 'PYTHON']

# Nested loops
pairs = [(x, y) for x in range(3) for y in range(3)]
print(pairs)  # [(0,0), (0,1), (0,2), (1,0), ...]`,
        language: 'python',
        tips: ['List comprehensions are more Pythonic', 'But do not sacrifice readability', 'Complex logic should use regular loops']
      }
    ]
  },
  {
    id: 'week7',
    day: 43,
    tier: 'beginner',
    title: 'The Dictionary',
    subtitle: 'Key-Value Pairs',
    icon: 'book',
    color: '#6366F1',
    unlocked: true,
    estimatedTime: '50 min',
    sections: [
      {
        title: 'Understanding Dictionaries',
        content: `Dictionaries store data as key-value pairs. Think of them like a real dictionary: you look up a word (key) to find its definition (value).

Unlike lists which use numeric indices, dictionaries use keys of any immutable type.`,
        code: `# Creating a dictionary
person = {
    "name": "Alice",
    "age": 30,
    "city": "New York",
    "is_developer": True
}

# Accessing values by key
print(person["name"])     # "Alice"
print(person["age"])      # 30

# Using .get() - safer, returns None if key missing
print(person.get("name"))      # "Alice"
print(person.get("country"))   # None (no error!)
print(person.get("country", "Unknown"))  # "Unknown" (default)`,
        language: 'python'
      },
      {
        title: 'Modifying Dictionaries',
        content: `Dictionaries are mutable - you can add, change, and remove key-value pairs.`,
        code: `person = {"name": "Alice", "age": 30}

# Add or update
person["email"] = "alice@example.com"  # Add new key
person["age"] = 31                      # Update existing

# Remove
del person["email"]                     # Delete by key
age = person.pop("age")                 # Remove and return value
person.clear()                          # Remove all items

# Useful methods
person = {"name": "Alice", "age": 30, "city": "NYC"}
print(person.keys())    # dict_keys(['name', 'age', 'city'])
print(person.values())  # dict_values(['Alice', 30, 'NYC'])
print(person.items())   # dict_items([('name', 'Alice'), ...])

# Check if key exists
if "name" in person:
    print("Name found!")`,
        language: 'python'
      },
      {
        title: 'Iterating Dictionaries',
        content: `There are several ways to loop through dictionary contents.`,
        code: `person = {"name": "Alice", "age": 30, "city": "NYC"}

# Loop through keys (default)
for key in person:
    print(key)

# Loop through values
for value in person.values():
    print(value)

# Loop through both (most common)
for key, value in person.items():
    print(f"{key}: {value}")

# Dictionary comprehension
numbers = [1, 2, 3, 4, 5]
squares = {n: n**2 for n in numbers}
print(squares)  # {1: 1, 2: 4, 3: 9, 4: 16, 5: 25}`,
        language: 'python'
      },
      {
        title: 'Nested Data Structures',
        content: `Real-world data is often complex. You can nest lists in dictionaries, dictionaries in lists, and so on.`,
        code: `# List of dictionaries
users = [
    {"name": "Alice", "age": 30},
    {"name": "Bob", "age": 25},
    {"name": "Charlie", "age": 35}
]

for user in users:
    print(f"{user['name']} is {user['age']} years old")

# Dictionary with lists
student = {
    "name": "Alice",
    "grades": [85, 90, 78, 92],
    "courses": ["Python", "Math", "Physics"]
}

average = sum(student["grades"]) / len(student["grades"])
print(f"{student['name']}'s average: {average:.1f}")

# Deeply nested
company = {
    "departments": {
        "engineering": {
            "employees": ["Alice", "Bob"],
            "budget": 100000
        },
        "sales": {
            "employees": ["Charlie"],
            "budget": 50000
        }
    }
}

eng_budget = company["departments"]["engineering"]["budget"]`,
        language: 'python'
      }
    ]
  },
  {
    id: 'week8',
    day: 50,
    tier: 'beginner',
    title: 'The Function',
    subtitle: 'Building Reusable Code',
    icon: 'cube',
    color: '#F97316',
    unlocked: true,
    estimatedTime: '65 min',
    sections: [
      {
        title: 'Why Functions?',
        content: `Functions are named blocks of reusable code. They are one of the most important concepts in programming.

Benefits of functions:
• Reusability - write once, use many times
• Organization - break complex problems into pieces
• Abstraction - hide complexity behind simple names
• Testing - easier to test small, focused functions`,
        code: `# Without functions - repetitive!
print("=" * 30)
print("WELCOME")
print("=" * 30)

# ... later in code ...
print("=" * 30)
print("GOODBYE")
print("=" * 30)

# With a function - elegant!
def print_banner(message):
    print("=" * 30)
    print(message)
    print("=" * 30)

print_banner("WELCOME")
print_banner("GOODBYE")
print_banner("ANYTHING YOU WANT")`,
        language: 'python'
      },
      {
        title: 'Defining and Calling Functions',
        content: `Use def to define a function. Call it by using its name followed by parentheses.`,
        code: `# Basic function definition
def greet():
    print("Hello!")
    print("Nice to meet you!")

# Calling the function
greet()  # Runs the code inside

# Function with parameters
def greet_person(name):
    print(f"Hello, {name}!")
    print("Nice to meet you!")

greet_person("Alice")   # Hello, Alice!
greet_person("Bob")     # Hello, Bob!

# Multiple parameters
def introduce(name, age, city):
    print(f"I am {name}, {age} years old, from {city}")

introduce("Alice", 30, "New York")`,
        language: 'python'
      },
      {
        title: 'Return Values',
        content: `Functions can send values back using return. This makes them much more useful.`,
        code: `# Function that returns a value
def add(a, b):
    result = a + b
    return result

# Using the returned value
sum_result = add(5, 3)
print(sum_result)  # 8

# Return ends the function immediately
def divide(a, b):
    if b == 0:
        return None  # Exit early
    return a / b

print(divide(10, 2))  # 5.0
print(divide(10, 0))  # None

# Returning multiple values
def get_stats(numbers):
    return min(numbers), max(numbers), sum(numbers)

low, high, total = get_stats([1, 2, 3, 4, 5])
print(f"Min: {low}, Max: {high}, Sum: {total}")`,
        language: 'python'
      },
      {
        title: 'Default Parameters and Keyword Arguments',
        content: `Make functions more flexible with default values and keyword arguments.`,
        code: `# Default parameter values
def greet(name, greeting="Hello"):
    print(f"{greeting}, {name}!")

greet("Alice")              # Hello, Alice!
greet("Bob", "Hi")          # Hi, Bob!
greet("Charlie", "Hey")     # Hey, Charlie!

# Keyword arguments (specify by name)
def describe_pet(name, animal="dog", age=1):
    print(f"{name} is a {age}-year-old {animal}")

describe_pet("Max")                    # Max is a 1-year-old dog
describe_pet("Whiskers", animal="cat") # Whiskers is a 1-year-old cat
describe_pet("Buddy", age=5)           # Buddy is a 5-year-old dog
describe_pet(animal="bird", name="Tweet", age=2)  # Order does not matter!`,
        language: 'python'
      }
    ]
  },
  // ═══════════════════════════════════════════════════════════════════════════
  // MONTH 3-4: FOUNDATION - Building Your Skills
  // ═══════════════════════════════════════════════════════════════════════════
  {
    id: 'week9',
    day: 57,
    tier: 'foundation',
    title: 'The Scope',
    subtitle: 'Understanding Variable Visibility',
    icon: 'eye',
    color: '#06B6D4',
    unlocked: true,
    estimatedTime: '45 min',
    sections: [
      {
        title: 'Local vs Global Scope',
        content: `Where you define a variable determines where you can use it. This is called scope.

Local scope: Variables inside functions - only visible inside that function.
Global scope: Variables outside functions - visible everywhere.`,
        code: `# Global variable
message = "Hello, Global!"

def my_function():
    # Local variable
    local_msg = "Hello, Local!"
    print(message)      # Can access global
    print(local_msg)    # Can access local

my_function()
print(message)          # Works - global
# print(local_msg)      # ERROR! local_msg does not exist here`,
        language: 'python'
      },
      {
        title: 'The Global Keyword',
        content: `To modify a global variable from inside a function, use the global keyword. But use this sparingly!`,
        code: `counter = 0

def increment():
    global counter  # Tell Python we mean the global one
    counter += 1

def bad_increment():
    counter = counter + 1  # ERROR! Python thinks it is local

increment()
increment()
print(counter)  # 2

# Better approach: pass and return
def better_increment(count):
    return count + 1

counter = 0
counter = better_increment(counter)
counter = better_increment(counter)
print(counter)  # 2`,
        language: 'python',
        tips: ['Avoid global variables when possible', 'Pass values as parameters', 'Return values instead of modifying globals']
      }
    ]
  },
  {
    id: 'week10',
    day: 64,
    tier: 'foundation',
    title: 'The Error',
    subtitle: 'Exception Handling',
    icon: 'bug',
    color: '#EF4444',
    unlocked: true,
    estimatedTime: '55 min',
    sections: [
      {
        title: 'Why Handle Errors?',
        content: `Programs encounter errors. Without handling, they crash. With proper exception handling, they recover gracefully.

Common errors:
• ZeroDivisionError - dividing by zero
• ValueError - wrong value type
• TypeError - wrong data type
• FileNotFoundError - file does not exist
• KeyError - dictionary key not found`,
        code: `# Without handling - program crashes!
# result = 10 / 0  # ZeroDivisionError: division by zero

# With handling - program continues
try:
    result = 10 / 0
except ZeroDivisionError:
    print("Cannot divide by zero!")
    result = 0

print(f"Result: {result}")  # Program continues!`,
        language: 'python'
      },
      {
        title: 'Try-Except-Else-Finally',
        content: `The complete error handling structure:
• try - code that might fail
• except - what to do if it fails
• else - runs only if try succeeded
• finally - always runs, no matter what`,
        code: `def safe_divide(a, b):
    try:
        result = a / b
    except ZeroDivisionError:
        print("Error: Cannot divide by zero!")
        return None
    except TypeError:
        print("Error: Invalid types for division!")
        return None
    else:
        print("Division successful!")
        return result
    finally:
        print("Division attempt complete.")

print(safe_divide(10, 2))   # Success
print(safe_divide(10, 0))   # Zero error
print(safe_divide("a", 2))  # Type error`,
        language: 'python'
      },
      {
        title: 'Raising Exceptions',
        content: `You can raise your own exceptions when something goes wrong in your code.`,
        code: `def set_age(age):
    if not isinstance(age, int):
        raise TypeError("Age must be an integer!")
    if age < 0:
        raise ValueError("Age cannot be negative!")
    if age > 150:
        raise ValueError("Age is unrealistically high!")
    return age

try:
    user_age = set_age(-5)
except ValueError as e:
    print(f"Validation error: {e}")
except TypeError as e:
    print(f"Type error: {e}")

# Creating custom exceptions
class InvalidEmailError(Exception):
    pass

def validate_email(email):
    if "@" not in email:
        raise InvalidEmailError(f"Invalid email: {email}")`,
        language: 'python'
      }
    ]
  },
  // ═══════════════════════════════════════════════════════════════════════════
  // MONTH 5-6: EXPANSION - Growing Your Skills
  // ═══════════════════════════════════════════════════════════════════════════
  {
    id: 'week17',
    day: 113,
    tier: 'intermediate',
    title: 'The Class',
    subtitle: 'Object-Oriented Programming',
    icon: 'construct',
    color: '#8B5CF6',
    unlocked: true,
    estimatedTime: '75 min',
    sections: [
      {
        title: 'What is OOP?',
        content: `Object-Oriented Programming organizes code into "objects" that combine data (attributes) and behavior (methods).

Think of a class as a blueprint. Each object created from that class is an instance.

OOP helps model real-world entities and makes code reusable and maintainable.`,
        code: `# A class is a blueprint
class Dog:
    # Class attribute (shared by all dogs)
    species = "Canis familiaris"
    
    # Constructor - runs when creating a new dog
    def __init__(self, name, breed, age):
        # Instance attributes (unique to each dog)
        self.name = name
        self.breed = breed
        self.age = age
    
    # Method - a function that belongs to the class
    def bark(self):
        return f"{self.name} says Woof!"
    
    def describe(self):
        return f"{self.name} is a {self.age}-year-old {self.breed}"

# Creating objects (instances)
my_dog = Dog("Max", "Labrador", 3)
your_dog = Dog("Bella", "Poodle", 5)

print(my_dog.bark())        # Max says Woof!
print(your_dog.describe())  # Bella is a 5-year-old Poodle
print(Dog.species)          # Canis familiaris`,
        language: 'python'
      },
      {
        title: 'Inheritance',
        content: `Classes can inherit from other classes, gaining their attributes and methods. This promotes code reuse.`,
        code: `class Animal:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def speak(self):
        raise NotImplementedError("Subclass must implement")

class Dog(Animal):  # Inherits from Animal
    def speak(self):
        return f"{self.name} says Woof!"
    
    def fetch(self):
        return f"{self.name} fetches the ball!"

class Cat(Animal):
    def speak(self):
        return f"{self.name} says Meow!"
    
    def purr(self):
        return f"{self.name} purrs contentedly..."

# Usage
dog = Dog("Rex", 3)
cat = Cat("Whiskers", 5)

print(dog.speak())   # Rex says Woof!
print(cat.speak())   # Whiskers says Meow!
print(dog.fetch())   # Rex fetches the ball!
print(dog.age)       # 3 (inherited from Animal)`,
        language: 'python'
      }
    ]
  },
  // ═══════════════════════════════════════════════════════════════════════════
  // MONTH 7-8: DEPTH - Going Deeper
  // ═══════════════════════════════════════════════════════════════════════════
  {
    id: 'week25',
    day: 169,
    tier: 'advanced',
    title: 'The Algorithm',
    subtitle: 'Problem Solving Patterns',
    icon: 'analytics',
    color: '#F59E0B',
    unlocked: true,
    estimatedTime: '90 min',
    sections: [
      {
        title: 'Big O Notation',
        content: `Big O describes how code performance scales with input size. Understanding this helps you write efficient code.

Common complexities (best to worst):
• O(1) - Constant: Same time regardless of input size
• O(log n) - Logarithmic: Halving the problem each step
• O(n) - Linear: Time grows proportionally with input
• O(n log n) - Linearithmic: Good sorting algorithms
• O(n²) - Quadratic: Nested loops over input`,
        code: `# O(1) - Constant time
def get_first(arr):
    return arr[0] if arr else None  # Always one operation

# O(n) - Linear time
def find_max(arr):
    max_val = arr[0]
    for num in arr:  # Visits every element once
        if num > max_val:
            max_val = num
    return max_val

# O(n²) - Quadratic time
def has_duplicate_slow(arr):
    for i in range(len(arr)):
        for j in range(i + 1, len(arr)):  # Nested loop!
            if arr[i] == arr[j]:
                return True
    return False

# O(n) - Better approach with hash set
def has_duplicate_fast(arr):
    seen = set()
    for item in arr:
        if item in seen:  # set lookup is O(1)
            return True
        seen.add(item)
    return False`,
        language: 'python'
      },
      {
        title: 'Two Pointers Pattern',
        content: `Use two pointers moving through data to solve problems efficiently. Common for arrays and strings.`,
        code: `# Palindrome check
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

# Two Sum in sorted array
def two_sum_sorted(nums, target):
    left, right = 0, len(nums) - 1
    
    while left < right:
        current = nums[left] + nums[right]
        if current == target:
            return [left, right]
        elif current < target:
            left += 1
        else:
            right -= 1
    return []`,
        language: 'python'
      }
    ]
  },
  // ═══════════════════════════════════════════════════════════════════════════
  // MONTH 9-10: MASTERY - Advanced Concepts
  // ═══════════════════════════════════════════════════════════════════════════
  {
    id: 'week33',
    day: 225,
    tier: 'advanced',
    title: 'The Async',
    subtitle: 'Concurrent Programming',
    icon: 'flash',
    color: '#EC4899',
    unlocked: true,
    estimatedTime: '80 min',
    sections: [
      {
        title: 'Understanding Asynchronous Code',
        content: `Synchronous code waits for each operation to complete before moving on. Asynchronous code can start an operation and continue with other work while waiting.

This is crucial for I/O operations like network requests, file operations, and database queries.`,
        code: `import asyncio

# Synchronous - blocks while waiting
def sync_task():
    import time
    time.sleep(1)  # Blocks everything for 1 second
    return "Done"

# Asynchronous - does not block
async def async_task():
    await asyncio.sleep(1)  # Yields control while waiting
    return "Done"

# The difference: async lets other code run during the wait`,
        language: 'python'
      },
      {
        title: 'Async/Await in Python',
        content: `Use async def to define coroutines and await to call them.`,
        code: `import asyncio

async def fetch_data(url, delay):
    print(f"Starting fetch from {url}...")
    await asyncio.sleep(delay)  # Simulate network delay
    print(f"Finished fetch from {url}")
    return f"Data from {url}"

async def main():
    # Run concurrently - much faster!
    results = await asyncio.gather(
        fetch_data("api/users", 2),
        fetch_data("api/posts", 2),
        fetch_data("api/comments", 2)
    )
    # Takes ~2 seconds total, not 6!
    
    for result in results:
        print(result)

# Run the async main
# asyncio.run(main())`,
        language: 'python'
      }
    ]
  },
  // ═══════════════════════════════════════════════════════════════════════════
  // MONTH 11-12: TRANSCENDENCE - Expert Level
  // ═══════════════════════════════════════════════════════════════════════════
  {
    id: 'week41',
    day: 281,
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
            print("Creating database connection...")
            cls._instance = super().__new__(cls)
            cls._instance.connection = "Connected"
        return cls._instance

# Both point to the SAME instance
db1 = Database()
db2 = Database()
print(db1 is db2)  # True`,
        language: 'python'
      },
      {
        title: 'Factory Pattern',
        content: `Create objects without specifying exact classes. Provides flexibility and loose coupling.`,
        code: `from abc import ABC, abstractmethod

class Animal(ABC):
    @abstractmethod
    def speak(self): pass

class Dog(Animal):
    def speak(self): return "Woof!"

class Cat(Animal):
    def speak(self): return "Meow!"

class AnimalFactory:
    @staticmethod
    def create(animal_type):
        animals = {"dog": Dog, "cat": Cat}
        return animals.get(animal_type.lower(), Dog)()

# Usage
pet = AnimalFactory.create("cat")
print(pet.speak())  # Meow!`,
        language: 'python'
      }
    ]
  },
  // ═══════════════════════════════════════════════════════════════════════════
  // THE SUMMIT: GODTIER
  // ═══════════════════════════════════════════════════════════════════════════
  {
    id: 'godtier',
    day: 365,
    tier: 'godtier',
    title: 'The Mastery',
    subtitle: 'Principles of Excellence',
    icon: 'trophy',
    color: '#FFD700',
    unlocked: true,
    estimatedTime: '∞',
    sections: [
      {
        title: 'SOLID Principles',
        content: `The foundation of maintainable, scalable code:

S - Single Responsibility: One class, one job
O - Open/Closed: Open for extension, closed for modification
L - Liskov Substitution: Subtypes must be substitutable
I - Interface Segregation: Many specific interfaces over one general
D - Dependency Inversion: Depend on abstractions, not concretions

These principles take years to master. Apply gradually.`,
        tips: ['Start with Single Responsibility', 'Refactor toward these principles', 'Do not over-engineer']
      },
      {
        title: 'The Clean Code Commandments',
        content: `1. Names should reveal intent
2. Functions should do one thing
3. Comments explain WHY, not WHAT
4. Handle errors gracefully
5. Write tests first (TDD)
6. Refactor continuously
7. Keep it simple (KISS)
8. Do not repeat yourself (DRY)
9. You are not gonna need it (YAGNI)
10. Leave code better than you found it`,
        code: `# BAD
def calc(a, b, t):
    if t == 1: return a + b
    elif t == 2: return a - b

# GOOD
def add(first: int, second: int) -> int:
    """Add two numbers."""
    return first + second

def subtract(first: int, second: int) -> int:
    """Subtract second from first."""
    return first - second`,
        language: 'python'
      },
      {
        title: 'The Journey Never Ends',
        content: `Congratulations. You have traveled far.

You have learned:
• The fundamentals of programming
• Data structures and algorithms
• Object-oriented design
• Error handling and best practices
• Asynchronous programming
• Design patterns
• Clean code principles

But mastery is not a destination. It is a lifelong journey.

"First, solve the problem. Then, write the code." - John Johnson

Keep building. Keep learning. Keep growing.

Welcome to Godtier. 🏆`,
        tips: [
          'The best code is code you do not write',
          'Debugging is twice as hard as writing',
          'Teach others to master concepts yourself'
        ]
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

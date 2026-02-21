import React, { useState, useEffect, useRef, useCallback } from 'react';
import {
  View, Text, StyleSheet, TouchableOpacity, ScrollView, TextInput,
  ActivityIndicator, SafeAreaView, StatusBar, Platform, Dimensions,
  KeyboardAvoidingView, Modal, FlatList, Alert, Animated, Vibration,
  TouchableWithoutFeedback, Pressable,
} from 'react-native';
import { WebView } from 'react-native-webview';
import { Ionicons } from '@expo/vector-icons';
import AsyncStorage from '@react-native-async-storage/async-storage';
import axios from 'axios';

const API_URL = process.env.EXPO_PUBLIC_BACKEND_URL || '';
const { width: SCREEN_WIDTH, height: SCREEN_HEIGHT } = Dimensions.get('window');
const VERSION = "4.1.0";
const CODENAME = "Nexus Pro";

// ============================================================================
// CONFIGURATION & CONSTANTS - Refactor-Ready Architecture
// ============================================================================
const CONFIG = {
  API_TIMEOUT: 15000,
  MAX_RETRIES: 3,
  RETRY_DELAY: 1000,
  CACHE_TTL: 5 * 60 * 1000, // 5 minutes
  ANIMATION_DURATION: 300,
  TOAST_DURATION: 3000,
};

// Enhanced error types for better debugging
type ErrorType = 'network' | 'timeout' | 'server' | 'validation' | 'unknown';

interface AppError {
  type: ErrorType;
  message: string;
  code?: number;
  retry?: boolean;
}

// Types
interface Language {
  key: string;
  name: string;
  display_name?: string;
  extension: string;
  icon: string;
  color: string;
  executable: boolean;
  description?: string;
  version?: string;
  type: 'builtin' | 'addon';
  tier?: number;
  status?: string;
  expansion_ready?: boolean;
}

interface Template {
  key: string;
  name: string;
  code: string;
  description?: string;
  complexity?: string;
}

interface TutorialStep {
  key: string;
  order: number;
  title: string;
  description: string;
  content: string;
  tips?: string[];
  highlight_element?: string;
  next_step?: string;
  celebration?: boolean;
}

// ============================================================================
// CODING BIBLE - Day 1 to Godtier Teaching Manual (Offline Ready)
// ============================================================================
interface BibleChapter {
  id: string;
  day: number;
  tier: 'beginner' | 'foundation' | 'intermediate' | 'advanced' | 'expert' | 'godtier';
  title: string;
  subtitle: string;
  icon: string;
  color: string;
  sections: BibleSection[];
  exercises?: BibleExercise[];
  unlocked: boolean;
}

interface BibleSection {
  title: string;
  content: string;
  code?: string;
  language?: string;
  tips?: string[];
  warning?: string;
}

interface BibleExercise {
  title: string;
  description: string;
  starterCode: string;
  language: string;
  hints: string[];
  solution?: string;
}

// THE CODING BIBLE - Complete Offline Manual
const CODING_BIBLE: BibleChapter[] = [
  {
    id: 'day1',
    day: 1,
    tier: 'beginner',
    title: 'The Genesis',
    subtitle: 'Your First Line of Code',
    icon: 'sunny',
    color: '#22C55E',
    unlocked: true,
    sections: [
      {
        title: 'Welcome, Future Developer',
        content: `Today marks the beginning of your coding journey. By the end of this chapter, you'll understand what programming is and write your very first program.

Programming is simply giving instructions to a computer in a language it understands. Think of it like writing a recipe - each step must be clear and precise.`,
        tips: ['Every expert was once a beginner', 'Mistakes are how we learn', 'Take breaks when frustrated']
      },
      {
        title: 'What is Code?',
        content: `Code is text that tells a computer what to do. Just like how English has grammar rules, programming languages have syntax rules.

The computer reads your code line by line, from top to bottom, and executes each instruction in order.`,
        code: `# This is a comment - the computer ignores it
# Below is actual code that runs:
print("Hello, World!")`,
        language: 'python',
        tips: ['Comments help explain your code', 'Indentation matters in Python']
      },
      {
        title: 'Variables: Storing Information',
        content: `Variables are like labeled boxes that store data. You give them a name and put something inside.`,
        code: `# Creating variables
name = "Alex"
age = 25
is_learning = True

# Using variables
print(name)
print("Age:", age)`,
        language: 'python'
      },
      {
        title: 'Data Types',
        content: `Different types of data need different storage:

• Strings: Text in quotes ("Hello")
• Integers: Whole numbers (42)
• Floats: Decimal numbers (3.14)
• Booleans: True or False`,
        code: `text = "I am a string"
number = 42
decimal = 3.14159
is_true = True`,
        language: 'python'
      }
    ],
    exercises: [
      {
        title: 'Hello You!',
        description: 'Create a variable with your name and print a greeting',
        starterCode: '# Store your name in a variable\\n# Then print "Hello, [your name]!"\\n',
        language: 'python',
        hints: ['Use a variable like: my_name = "..."', 'Use print() to display output']
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
    sections: [
      {
        title: 'Conditional Statements',
        content: `Programs need to make decisions. The if statement checks if something is true and acts accordingly.`,
        code: `age = 18

if age >= 18:
    print("You are an adult")
else:
    print("You are a minor")`,
        language: 'python'
      },
      {
        title: 'Multiple Conditions',
        content: `Use elif (else if) to check multiple conditions in sequence.`,
        code: `score = 85

if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
else:
    grade = "F"

print("Grade:", grade)`,
        language: 'python'
      },
      {
        title: 'Comparison Operators',
        content: `These operators compare values and return True or False:

• == Equal to
• != Not equal to
• > Greater than
• < Less than
• >= Greater than or equal
• <= Less than or equal`,
        code: `x = 10
y = 5

print(x == y)  # False
print(x > y)   # True
print(x != y)  # True`,
        language: 'python'
      },
      {
        title: 'Logical Operators',
        content: `Combine conditions with and, or, not:`,
        code: `age = 25
has_license = True

# Both must be true
if age >= 18 and has_license:
    print("Can drive")

# At least one must be true
if age < 18 or not has_license:
    print("Cannot drive")`,
        language: 'python'
      }
    ]
  },
  {
    id: 'day3',
    day: 3,
    tier: 'beginner',
    title: 'The Loop',
    subtitle: 'Repeating Actions',
    icon: 'repeat',
    color: '#8B5CF6',
    unlocked: true,
    sections: [
      {
        title: 'Why Loops?',
        content: `Instead of writing the same code 100 times, loops let you repeat actions automatically.`,
        code: `# Without loops (tedious!)
print(1)
print(2)
print(3)

# With a loop (elegant!)
for i in range(1, 4):
    print(i)`,
        language: 'python'
      },
      {
        title: 'For Loops',
        content: `For loops iterate over a sequence - great when you know how many times to repeat.`,
        code: `# Loop through numbers
for num in range(5):
    print(num)  # 0, 1, 2, 3, 4

# Loop through a list
fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
    print(fruit)`,
        language: 'python'
      },
      {
        title: 'While Loops',
        content: `While loops continue as long as a condition is true - useful when you don't know how many iterations you need.`,
        code: `count = 0

while count < 5:
    print(count)
    count += 1  # Important! Or infinite loop

print("Done!")`,
        language: 'python',
        warning: 'Always ensure your while loop can end! An infinite loop will freeze your program.'
      },
      {
        title: 'Break and Continue',
        content: `Control loop flow with break (exit loop) and continue (skip to next iteration).`,
        code: `for i in range(10):
    if i == 3:
        continue  # Skip 3
    if i == 7:
        break     # Stop at 7
    print(i)
# Output: 0, 1, 2, 4, 5, 6`,
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
    sections: [
      {
        title: 'What are Functions?',
        content: `Functions are reusable blocks of code. Write once, use many times. They help organize code and avoid repetition.`,
        code: `# Defining a function
def greet(name):
    return f"Hello, {name}!"

# Using the function
message = greet("Alice")
print(message)  # Hello, Alice!

print(greet("Bob"))  # Hello, Bob!`,
        language: 'python'
      },
      {
        title: 'Parameters and Arguments',
        content: `Parameters are variables in the function definition. Arguments are actual values you pass in.`,
        code: `def add(a, b):  # a, b are parameters
    return a + b

result = add(5, 3)  # 5, 3 are arguments
print(result)  # 8

# Default parameters
def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"

print(greet("Alice"))           # Hello, Alice!
print(greet("Bob", "Hi"))       # Hi, Bob!`,
        language: 'python'
      },
      {
        title: 'Return Values',
        content: `Functions can return values using the return statement. Without it, they return None.`,
        code: `def square(n):
    return n * n

def print_square(n):
    print(n * n)  # No return

result1 = square(4)       # result1 = 16
result2 = print_square(4) # Prints 16, result2 = None`,
        language: 'python'
      },
      {
        title: 'Scope',
        content: `Variables inside functions are local - they only exist inside that function.`,
        code: `x = 10  # Global variable

def my_func():
    y = 5   # Local variable
    print(x)  # Can access global
    print(y)  # Can access local

my_func()
print(x)  # Works
# print(y)  # Error! y doesn't exist here`,
        language: 'python',
        tips: ['Avoid global variables when possible', 'Pass values as parameters instead']
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
    sections: [
      {
        title: 'Lists',
        content: `Lists store multiple items in order. They can be modified (mutable).`,
        code: `# Creating lists
numbers = [1, 2, 3, 4, 5]
mixed = ["hello", 42, True, 3.14]

# Accessing items (0-indexed)
print(numbers[0])   # 1 (first)
print(numbers[-1])  # 5 (last)

# Modifying
numbers.append(6)    # Add to end
numbers.insert(0, 0) # Insert at position
numbers.remove(3)    # Remove value
del numbers[0]       # Delete by index`,
        language: 'python'
      },
      {
        title: 'List Operations',
        content: `Powerful operations to manipulate lists:`,
        code: `nums = [3, 1, 4, 1, 5, 9, 2, 6]

# Slicing
print(nums[2:5])   # [4, 1, 5]
print(nums[:3])    # [3, 1, 4]
print(nums[5:])    # [9, 2, 6]

# Common methods
nums.sort()         # Sort in place
sorted_nums = sorted(nums)  # Return sorted copy
nums.reverse()      # Reverse in place
print(len(nums))    # Length: 8
print(sum(nums))    # Sum: 31`,
        language: 'python'
      },
      {
        title: 'Dictionaries',
        content: `Dictionaries store key-value pairs. Think of them as real dictionaries: word → definition.`,
        code: `# Creating a dictionary
person = {
    "name": "Alice",
    "age": 30,
    "city": "NYC"
}

# Accessing values
print(person["name"])     # Alice
print(person.get("age"))  # 30

# Modifying
person["email"] = "alice@example.com"  # Add
person["age"] = 31                     # Update
del person["city"]                     # Delete

# Iterating
for key, value in person.items():
    print(f"{key}: {value}")`,
        language: 'python'
      },
      {
        title: 'Sets and Tuples',
        content: `Sets: Unordered, unique items. Tuples: Ordered, immutable lists.`,
        code: `# Sets - unique values only
unique = {1, 2, 2, 3, 3, 3}
print(unique)  # {1, 2, 3}

# Set operations
a = {1, 2, 3}
b = {2, 3, 4}
print(a | b)  # Union: {1, 2, 3, 4}
print(a & b)  # Intersection: {2, 3}

# Tuples - immutable
point = (10, 20)
x, y = point  # Unpacking
# point[0] = 5  # Error! Can't modify`,
        language: 'python'
      }
    ]
  },
  {
    id: 'day7',
    day: 7,
    tier: 'intermediate',
    title: 'The Class',
    subtitle: 'Object-Oriented Programming',
    icon: 'construct',
    color: '#06B6D4',
    unlocked: true,
    sections: [
      {
        title: 'What is OOP?',
        content: `Object-Oriented Programming organizes code into "objects" that contain data (attributes) and behavior (methods). Think of a class as a blueprint for creating objects.`,
        code: `# A class is a blueprint
class Dog:
    # Constructor - runs when creating object
    def __init__(self, name, breed):
        self.name = name    # Instance attribute
        self.breed = breed
    
    # Method - function inside class
    def bark(self):
        return f"{self.name} says Woof!"

# Creating objects (instances)
my_dog = Dog("Max", "Labrador")
print(my_dog.name)    # Max
print(my_dog.bark())  # Max says Woof!`,
        language: 'python'
      },
      {
        title: 'Inheritance',
        content: `Classes can inherit from other classes, gaining their attributes and methods.`,
        code: `class Animal:
    def __init__(self, name):
        self.name = name
    
    def speak(self):
        pass  # To be overridden

class Dog(Animal):  # Inherits from Animal
    def speak(self):
        return f"{self.name} barks!"

class Cat(Animal):
    def speak(self):
        return f"{self.name} meows!"

dog = Dog("Rex")
cat = Cat("Whiskers")
print(dog.speak())  # Rex barks!
print(cat.speak())  # Whiskers meows!`,
        language: 'python'
      },
      {
        title: 'Encapsulation',
        content: `Hide internal details and expose only what's necessary. Use _ prefix for "private" attributes.`,
        code: `class BankAccount:
    def __init__(self, balance):
        self._balance = balance  # "Private"
    
    def deposit(self, amount):
        if amount > 0:
            self._balance += amount
            return True
        return False
    
    def get_balance(self):
        return self._balance

account = BankAccount(100)
account.deposit(50)
print(account.get_balance())  # 150`,
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
    sections: [
      {
        title: 'Why Handle Errors?',
        content: `Programs encounter errors. Without handling, they crash. With handling, they gracefully recover.`,
        code: `# Without handling - CRASH!
# result = 10 / 0  # ZeroDivisionError

# With handling - SAFE
try:
    result = 10 / 0
except ZeroDivisionError:
    print("Cannot divide by zero!")
    result = 0

print(f"Result: {result}")`,
        language: 'python'
      },
      {
        title: 'Try-Except-Finally',
        content: `Full error handling structure:`,
        code: `def safe_divide(a, b):
    try:
        result = a / b
    except ZeroDivisionError:
        print("Division by zero!")
        return None
    except TypeError:
        print("Invalid types!")
        return None
    else:
        print("Success!")  # Runs if no error
        return result
    finally:
        print("Cleanup done")  # Always runs

print(safe_divide(10, 2))   # Success!
print(safe_divide(10, 0))   # Division by zero!`,
        language: 'python'
      },
      {
        title: 'Raising Exceptions',
        content: `Create your own errors when something goes wrong:`,
        code: `def set_age(age):
    if age < 0:
        raise ValueError("Age cannot be negative!")
    if age > 150:
        raise ValueError("Age seems unrealistic!")
    return age

try:
    user_age = set_age(-5)
except ValueError as e:
    print(f"Error: {e}")`,
        language: 'python'
      }
    ]
  },
  {
    id: 'day14',
    day: 14,
    tier: 'advanced',
    title: 'The Algorithm',
    subtitle: 'Problem Solving Patterns',
    icon: 'analytics',
    color: '#8B5CF6',
    unlocked: true,
    sections: [
      {
        title: 'Big O Notation',
        content: `Big O describes how code performance scales with input size.

• O(1) - Constant: Same time regardless of size
• O(n) - Linear: Time grows with size
• O(n²) - Quadratic: Time grows exponentially
• O(log n) - Logarithmic: Time grows slowly`,
        code: `# O(1) - Constant
def get_first(arr):
    return arr[0]

# O(n) - Linear
def find_max(arr):
    max_val = arr[0]
    for num in arr:  # Loops through all
        if num > max_val:
            max_val = num
    return max_val

# O(n²) - Quadratic (nested loops)
def has_duplicate(arr):
    for i in range(len(arr)):
        for j in range(i+1, len(arr)):
            if arr[i] == arr[j]:
                return True
    return False`,
        language: 'python'
      },
      {
        title: 'Common Patterns',
        content: `Master these patterns to solve most problems:`,
        code: `# Two Pointers
def is_palindrome(s):
    left, right = 0, len(s) - 1
    while left < right:
        if s[left] != s[right]:
            return False
        left += 1
        right -= 1
    return True

# Sliding Window
def max_sum_subarray(arr, k):
    window_sum = sum(arr[:k])
    max_sum = window_sum
    for i in range(k, len(arr)):
        window_sum += arr[i] - arr[i-k]
        max_sum = max(max_sum, window_sum)
    return max_sum

# Hash Map for O(1) lookup
def two_sum(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i`,
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
    sections: [
      {
        title: 'Async/Await',
        content: `Asynchronous code doesn't block while waiting. Perfect for I/O operations like API calls.`,
        code: `import asyncio

async def fetch_data(url):
    print(f"Fetching {url}...")
    await asyncio.sleep(1)  # Simulated delay
    return f"Data from {url}"

async def main():
    # Run concurrently - much faster!
    results = await asyncio.gather(
        fetch_data("api/users"),
        fetch_data("api/posts"),
        fetch_data("api/comments")
    )
    for r in results:
        print(r)

# asyncio.run(main())`,
        language: 'python'
      },
      {
        title: 'JavaScript Async',
        content: `JavaScript is built for async with Promises and async/await:`,
        code: `// Async function returns a Promise
async function fetchUser(id) {
    const response = await fetch(\`/api/users/\${id}\`);
    const data = await response.json();
    return data;
}

// Using the async function
fetchUser(1)
    .then(user => console.log(user))
    .catch(err => console.error(err));

// Or with async/await
async function main() {
    try {
        const user = await fetchUser(1);
        console.log(user);
    } catch (err) {
        console.error(err);
    }
}`,
        language: 'javascript'
      }
    ]
  },
  {
    id: 'day30',
    day: 30,
    tier: 'expert',
    title: 'The Pattern',
    subtitle: 'Design Patterns',
    icon: 'git-network',
    color: '#06B6D4',
    unlocked: true,
    sections: [
      {
        title: 'Singleton Pattern',
        content: `Ensure a class has only one instance. Useful for configurations, loggers, etc.`,
        code: `class Database:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.connection = "Connected"
        return cls._instance

# Both variables point to same instance
db1 = Database()
db2 = Database()
print(db1 is db2)  # True`,
        language: 'python'
      },
      {
        title: 'Factory Pattern',
        content: `Create objects without specifying exact class. Great for flexibility.`,
        code: `class Dog:
    def speak(self): return "Woof!"

class Cat:
    def speak(self): return "Meow!"

class AnimalFactory:
    @staticmethod
    def create(animal_type):
        if animal_type == "dog":
            return Dog()
        elif animal_type == "cat":
            return Cat()
        raise ValueError(f"Unknown: {animal_type}")

# Usage - no need to know specific classes
pet = AnimalFactory.create("dog")
print(pet.speak())  # Woof!`,
        language: 'python'
      },
      {
        title: 'Observer Pattern',
        content: `Objects subscribe to events and get notified when they occur.`,
        code: `class EventEmitter:
    def __init__(self):
        self._listeners = {}
    
    def on(self, event, callback):
        if event not in self._listeners:
            self._listeners[event] = []
        self._listeners[event].append(callback)
    
    def emit(self, event, data=None):
        for callback in self._listeners.get(event, []):
            callback(data)

# Usage
emitter = EventEmitter()
emitter.on("login", lambda user: print(f"{user} logged in"))
emitter.on("login", lambda user: print(f"Welcome {user}!"))
emitter.emit("login", "Alice")`,
        language: 'python'
      }
    ]
  },
  {
    id: 'godtier',
    day: 100,
    tier: 'godtier',
    title: 'The Mastery',
    subtitle: 'Principles of Excellence',
    icon: 'trophy',
    color: '#FFD700',
    unlocked: true,
    sections: [
      {
        title: 'SOLID Principles',
        content: `The foundation of maintainable code:

• S - Single Responsibility: One class, one job
• O - Open/Closed: Open for extension, closed for modification
• L - Liskov Substitution: Subtypes must be substitutable
• I - Interface Segregation: Many specific interfaces > one general
• D - Dependency Inversion: Depend on abstractions, not concretions`,
        tips: ['These take years to master', 'Apply gradually, not all at once']
      },
      {
        title: 'Clean Code Commandments',
        content: `1. Names should reveal intent
2. Functions should do one thing
3. Comments explain WHY, not WHAT
4. Handle errors gracefully
5. Write tests before code (TDD)
6. Refactor continuously
7. Keep it simple (KISS)
8. Don't repeat yourself (DRY)
9. You aren't gonna need it (YAGNI)
10. Leave code better than you found it`,
        code: `# BAD
def calc(a, b, t):
    if t == 1:
        return a + b
    elif t == 2:
        return a - b

# GOOD
def add(first_number, second_number):
    return first_number + second_number

def subtract(first_number, second_number):
    return first_number - second_number`,
        language: 'python'
      },
      {
        title: 'The Godtier Mindset',
        content: `Technical skills get you hired. These principles make you exceptional:

• Read more code than you write
• Teach others to deepen understanding
• Embrace failure as feedback
• Build projects that solve real problems
• Contribute to open source
• Stay curious, technologies change
• Code is communication - write for humans
• Premature optimization is the root of evil
• Simple is better than complex
• Done is better than perfect`,
        tips: [
          'The best code is code you don\\'t have to write',
          'Debugging is twice as hard as writing code',
          'If you\\'re not embarrassed by v1, you launched too late'
        ]
      },
      {
        title: 'Your Journey Continues',
        content: `Congratulations on reaching this point. But remember - mastery is a journey, not a destination.

Keep building. Keep learning. Keep shipping.

"First, solve the problem. Then, write the code." - John Johnson

Welcome to Godtier. 🏆`,
      }
    ]
  }
];

interface Tooltip {
  id: string;
  title: string;
  description: string;
  tips?: string[];
  shortcut?: string;
}

interface CodeAnalysis {
  complexity: string;
  cyclomatic_complexity: number;
  lines_of_code: number;
  functions_count: number;
  classes_count: number;
}

interface AIMode {
  key: string;
  name: string;
  description: string;
}

// Themes - 2026 Design
const themes = {
  dark: {
    background: '#09090B',
    surface: '#18181B',
    surfaceAlt: '#27272A',
    surfaceHover: '#3F3F46',
    primary: '#6366F1',
    primaryGlow: 'rgba(99, 102, 241, 0.3)',
    secondary: '#A1A1AA',
    accent: '#22D3EE',
    text: '#FAFAFA',
    textSecondary: '#A1A1AA',
    textMuted: '#71717A',
    border: '#3F3F46',
    borderSubtle: '#27272A',
    success: '#22C55E',
    error: '#EF4444',
    warning: '#F59E0B',
    codeBackground: '#0A0A0B',
    tutorial: '#8B5CF6',
    tutorialGlow: 'rgba(139, 92, 246, 0.3)',
  },
  light: {
    background: '#FAFAFA',
    surface: '#FFFFFF',
    surfaceAlt: '#F4F4F5',
    surfaceHover: '#E4E4E7',
    primary: '#4F46E5',
    primaryGlow: 'rgba(79, 70, 229, 0.15)',
    secondary: '#71717A',
    accent: '#0891B2',
    text: '#18181B',
    textSecondary: '#52525B',
    textMuted: '#A1A1AA',
    border: '#E4E4E7',
    borderSubtle: '#F4F4F5',
    success: '#16A34A',
    error: '#DC2626',
    warning: '#D97706',
    codeBackground: '#FAFAFA',
    tutorial: '#7C3AED',
    tutorialGlow: 'rgba(124, 58, 237, 0.15)',
  },
};

export default function CodeDockQuantumNexus() {
  // Core State
  const [theme, setTheme] = useState<'dark' | 'light'>('dark');
  const [languages, setLanguages] = useState<Language[]>([]);
  const [selectedLanguage, setSelectedLanguage] = useState<Language | null>(null);
  const [code, setCode] = useState('');
  const [output, setOutput] = useState('');
  const [isExecuting, setIsExecuting] = useState(false);
  const [currentFileName, setCurrentFileName] = useState('untitled');
  const [templates, setTemplates] = useState<Template[]>([]);
  const [savedFiles, setSavedFiles] = useState<any[]>([]);
  const [aiModes, setAIModes] = useState<AIMode[]>([]);
  const [codeAnalysis, setCodeAnalysis] = useState<CodeAnalysis | null>(null);
  const [executionTime, setExecutionTime] = useState<number | null>(null);
  const [loading, setLoading] = useState(true);

  // Modal State
  const [showLanguageModal, setShowLanguageModal] = useState(false);
  const [showTemplateModal, setShowTemplateModal] = useState(false);
  const [showFilesModal, setShowFilesModal] = useState(false);
  const [showSettingsModal, setShowSettingsModal] = useState(false);
  const [showAddonModal, setShowAddonModal] = useState(false);
  const [showAIModal, setShowAIModal] = useState(false);
  const [showAnalysisModal, setShowAnalysisModal] = useState(false);
  const [showOutput, setShowOutput] = useState(false);
  const [showWebPreview, setShowWebPreview] = useState(false);
  const [htmlPreview, setHtmlPreview] = useState('');
  
  // ============================================================================
  // CODING BIBLE STATE - Offline Knowledge Base
  // ============================================================================
  const [showBibleModal, setShowBibleModal] = useState(false);
  const [selectedChapter, setSelectedChapter] = useState<BibleChapter | null>(null);
  const [currentSectionIndex, setCurrentSectionIndex] = useState(0);
  const [bibleProgress, setBibleProgress] = useState<Record<string, boolean>>({});
  const [bibleBookmarks, setBibleBookmarks] = useState<string[]>([]);
  
  // Teaching Mode State
  const [showTutorial, setShowTutorial] = useState(false);
  const [tutorialSteps, setTutorialSteps] = useState<TutorialStep[]>([]);
  const [currentTutorialStep, setCurrentTutorialStep] = useState(0);
  const [tutorialCompleted, setTutorialCompleted] = useState(false);
  
  // Tooltip State
  const [tooltips, setTooltips] = useState<Record<string, Tooltip>>({});
  const [activeTooltip, setActiveTooltip] = useState<string | null>(null);
  const [showTooltipModal, setShowTooltipModal] = useState(false);
  
  // Advanced Panel State
  const [showAdvancedPanel, setShowAdvancedPanel] = useState(false);
  const [advancedUnlocked, setAdvancedUnlocked] = useState(false);
  const [versionTapCount, setVersionTapCount] = useState(0);
  const [advancedSettings, setAdvancedSettings] = useState({
    execution_timeout: 10,
    memory_limit_mb: 256,
    security_level: 'standard',
    debug_mode: false,
    experimental_features: false,
  });
  
  // Language Dock State
  const [showDockModal, setShowDockModal] = useState(false);
  const [availableDocks, setAvailableDocks] = useState<Language[]>([]);
  
  // AI State
  const [selectedAIMode, setSelectedAIMode] = useState<AIMode | null>(null);
  const [aiResponse, setAIResponse] = useState('');
  const [isAILoading, setIsAILoading] = useState(false);
  
  // ============================================================================
  // HOTFIX: Enhanced Error & Connection State
  // ============================================================================
  const [connectionStatus, setConnectionStatus] = useState<'connected' | 'disconnected' | 'reconnecting'>('connected');
  const [lastError, setLastError] = useState<AppError | null>(null);
  const [retryCount, setRetryCount] = useState(0);

  // Animation
  const pulseAnim = useRef(new Animated.Value(1)).current;
  const tutorialHighlightAnim = useRef(new Animated.Value(0)).current;
  const fadeAnim = useRef(new Animated.Value(0)).current;
  const slideAnim = useRef(new Animated.Value(50)).current;

  const colors = themes[theme];
  
  // ============================================================================
  // HOTFIX: Retry Utility with Exponential Backoff
  // ============================================================================
  const retryWithBackoff = async <T,>(
    fn: () => Promise<T>,
    maxRetries: number = CONFIG.MAX_RETRIES,
    delay: number = CONFIG.RETRY_DELAY
  ): Promise<T> => {
    let lastError: any;
    for (let i = 0; i < maxRetries; i++) {
      try {
        return await fn();
      } catch (error) {
        lastError = error;
        if (i < maxRetries - 1) {
          await new Promise(r => setTimeout(r, delay * Math.pow(2, i)));
        }
      }
    }
    throw lastError;
  };

  // Parse and classify errors for better UX
  const parseError = (error: any): AppError => {
    if (error.code === 'ECONNABORTED' || error.message?.includes('timeout')) {
      return { type: 'timeout', message: 'Request timed out. Check your connection.', retry: true };
    }
    if (error.response?.status === 500) {
      return { type: 'server', message: 'Server error. Please try again.', code: 500, retry: true };
    }
    if (error.response?.status === 404) {
      return { type: 'validation', message: 'Resource not found.', code: 404, retry: false };
    }
    if (!error.response && error.message?.includes('Network')) {
      return { type: 'network', message: 'Network error. Check your internet connection.', retry: true };
    }
    return { type: 'unknown', message: error.message || 'An unexpected error occurred.', retry: true };
  };

  // Animations
  useEffect(() => {
    Animated.loop(
      Animated.sequence([
        Animated.timing(pulseAnim, { toValue: 1.05, duration: 1500, useNativeDriver: true }),
        Animated.timing(pulseAnim, { toValue: 1, duration: 1500, useNativeDriver: true }),
      ])
    ).start();
  }, []);

  useEffect(() => {
    if (showTutorial) {
      Animated.loop(
        Animated.sequence([
          Animated.timing(tutorialHighlightAnim, { toValue: 1, duration: 1000, useNativeDriver: true }),
          Animated.timing(tutorialHighlightAnim, { toValue: 0, duration: 1000, useNativeDriver: true }),
        ])
      ).start();
    }
  }, [showTutorial]);

  // ============================================================================
  // HOTFIX: Enhanced Data Loading with Retry & Connection Management
  // ============================================================================
  useEffect(() => {
    loadData();
    // Start entrance animation
    Animated.parallel([
      Animated.timing(fadeAnim, { toValue: 1, duration: 500, useNativeDriver: true }),
      Animated.timing(slideAnim, { toValue: 0, duration: 400, useNativeDriver: true }),
    ]).start();
  }, []);

  const loadData = async () => {
    setConnectionStatus('reconnecting');
    try {
      const savedTheme = await AsyncStorage.getItem('codedock_theme');
      if (savedTheme) setTheme(savedTheme as 'dark' | 'light');

      const tutorialDone = await AsyncStorage.getItem('tutorial_completed');
      setTutorialCompleted(tutorialDone === 'true');

      const advUnlocked = await AsyncStorage.getItem('advanced_unlocked');
      setAdvancedUnlocked(advUnlocked === 'true');

      // Load Bible progress (offline)
      const savedBibleProgress = await AsyncStorage.getItem('bible_progress');
      if (savedBibleProgress) setBibleProgress(JSON.parse(savedBibleProgress));

      const savedBookmarks = await AsyncStorage.getItem('bible_bookmarks');
      if (savedBookmarks) setBibleBookmarks(JSON.parse(savedBookmarks));

      // Load languages with retry
      const langResponse = await retryWithBackoff(() => 
        axios.get(`${API_URL}/api/languages`, { timeout: CONFIG.API_TIMEOUT })
      );
      setLanguages(langResponse.data.languages || []);
      
      const defaultLang = langResponse.data.languages?.find((l: Language) => l.key === 'python');
      if (defaultLang) {
        setSelectedLanguage(defaultLang);
        loadTemplates('python');
      }

      // Load AI modes with retry
      const aiResponse = await retryWithBackoff(() => 
        axios.get(`${API_URL}/api/ai/modes`, { timeout: CONFIG.API_TIMEOUT })
      );
      setAIModes(aiResponse.data.modes || []);

      // Load tooltips
      try {
        const tooltipResponse = await axios.get(`${API_URL}/api/tooltips`, { timeout: CONFIG.API_TIMEOUT });
        setTooltips(tooltipResponse.data.tooltips || {});
      } catch { /* Non-critical */ }

      // Load tutorial steps
      try {
        const tutorialResponse = await axios.get(`${API_URL}/api/tutorial/steps`, { timeout: CONFIG.API_TIMEOUT });
        setTutorialSteps(tutorialResponse.data.steps || []);
      } catch { /* Non-critical */ }

      // Load dock info
      try {
        const dockResponse = await axios.get(`${API_URL}/api/dock/available`, { timeout: CONFIG.API_TIMEOUT });
        setAvailableDocks(dockResponse.data.docks || []);
      } catch { /* Non-critical */ }

      // Load files
      loadFiles();

      // Mark as connected
      setConnectionStatus('connected');
      setLastError(null);
      setRetryCount(0);

      // Show tutorial for first-time users
      if (tutorialDone !== 'true') {
        setTimeout(() => setShowTutorial(true), 1000);
      }
    } catch (error: any) {
      console.error('Failed to load:', error);
      const parsedError = parseError(error);
      setLastError(parsedError);
      setConnectionStatus('disconnected');
      setRetryCount(prev => prev + 1);
      
      // Fallback languages
      setLanguages([
        { key: 'python', name: 'Python', display_name: 'Python 3.12+', extension: '.py', icon: 'logo-python', color: '#3776AB', executable: true, type: 'builtin', tier: 1 },
        { key: 'javascript', name: 'JavaScript', display_name: 'JavaScript ES2026', extension: '.js', icon: 'logo-javascript', color: '#F7DF1E', executable: true, type: 'builtin', tier: 1 },
        { key: 'html', name: 'HTML', display_name: 'HTML 5.3', extension: '.html', icon: 'logo-html5', color: '#E34F26', executable: true, type: 'builtin', tier: 1 },
        { key: 'cpp', name: 'C++', display_name: 'C++23', extension: '.cpp', icon: 'code-slash', color: '#00599C', executable: true, type: 'builtin', tier: 1 },
        { key: 'c', name: 'C', display_name: 'C23', extension: '.c', icon: 'code-slash', color: '#A8B9CC', executable: true, type: 'builtin', tier: 1 },
        { key: 'typescript', name: 'TypeScript', display_name: 'TypeScript 5.6+', extension: '.ts', icon: 'logo-javascript', color: '#3178C6', executable: true, type: 'builtin', tier: 1 },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const loadTemplates = async (language: string) => {
    try {
      const response = await axios.get(`${API_URL}/api/templates/${language}`);
      setTemplates(response.data.templates || []);
    } catch (error) {
      setTemplates([]);
    }
  };

  const loadFiles = async () => {
    try {
      const response = await axios.get(`${API_URL}/api/files`);
      setSavedFiles(response.data.files || []);
    } catch (error) {
      console.error('Failed to load files');
    }
  };

  const toggleTheme = async () => {
    const newTheme = theme === 'dark' ? 'light' : 'dark';
    setTheme(newTheme);
    await AsyncStorage.setItem('codedock_theme', newTheme);
    if (Platform.OS !== 'web') Vibration.vibrate(10);
  };

  const selectLanguage = (lang: Language) => {
    setSelectedLanguage(lang);
    setShowLanguageModal(false);
    setCode('');
    setOutput('');
    setShowOutput(false);
    setShowWebPreview(false);
    setCodeAnalysis(null);
    loadTemplates(lang.key);
  };

  const executeCode = async () => {
    if (!code.trim() || !selectedLanguage) return;

    setIsExecuting(true);
    setOutput('');
    setShowOutput(true);
    setShowWebPreview(false);
    setExecutionTime(null);

    try {
      if (selectedLanguage.key === 'html') {
        setHtmlPreview(code);
        setShowWebPreview(true);
        setShowOutput(false);
        return;
      }

      if (selectedLanguage.key === 'javascript' || selectedLanguage.key === 'typescript') {
        const response = await axios.post(`${API_URL}/api/execute`, {
          code, language: selectedLanguage.key,
        });
        
        const wrappedCode = response.data.result.output;
        setHtmlPreview(`
          <html><head><meta name="viewport" content="width=device-width, initial-scale=1">
          <style>body{font-family:monospace;padding:16px;background:${colors.codeBackground};color:${colors.text};font-size:14px;}</style></head>
          <body><pre id="o"></pre><script>try{var r=${wrappedCode};document.getElementById('o').textContent=r.status==='success'?r.output:'Error: '+r.error;}catch(e){document.getElementById('o').textContent='Error: '+e.message;}</script></body></html>
        `);
        setShowWebPreview(true);
        setExecutionTime(response.data.result.metrics?.execution_time_ms || 0);
        return;
      }

      const response = await axios.post(`${API_URL}/api/execute`, {
        code, language: selectedLanguage.key,
        timeout_seconds: advancedSettings.execution_timeout,
        include_analysis: true,
      });

      const result = response.data.result;
      setExecutionTime(result.metrics?.execution_time_ms || 0);
      if (result.analysis) setCodeAnalysis(result.analysis);
      
      if (result.status === 'success') {
        setOutput(result.output || 'Program executed successfully (no output)');
      } else {
        setOutput(`${result.status === 'timeout' ? '⏱' : result.status === 'security_violation' ? '🛡' : '❌'} ${result.error || 'Error'}`);
      }
    } catch (error: any) {
      setOutput(`Execution failed: ${error.response?.data?.detail || error.message}`);
    } finally {
      setIsExecuting(false);
    }
  };

  const analyzeCode = async () => {
    if (!code.trim() || !selectedLanguage) return;
    try {
      const response = await axios.post(`${API_URL}/api/analyze`, { code, language: selectedLanguage.key });
      setCodeAnalysis(response.data.analysis);
      setShowAnalysisModal(true);
    } catch (error) {
      Alert.alert('Error', 'Failed to analyze code');
    }
  };

  const askAI = async (mode: AIMode) => {
    if (!code.trim()) {
      Alert.alert('No Code', 'Please write some code first');
      return;
    }
    setSelectedAIMode(mode);
    setIsAILoading(true);
    setAIResponse('');
    try {
      const response = await axios.post(`${API_URL}/api/ai/assist`, {
        code, language: selectedLanguage?.key || 'python', mode: mode.key,
      });
      setAIResponse(response.data.suggestion);
    } catch (error: any) {
      setAIResponse(`AI Error: ${error.response?.data?.detail || error.message}`);
    } finally {
      setIsAILoading(false);
    }
  };

  const saveFile = async () => {
    if (!code.trim() || !selectedLanguage) return;
    try {
      await axios.post(`${API_URL}/api/files`, {
        name: currentFileName + selectedLanguage.extension,
        language: selectedLanguage.key, code,
      });
      Alert.alert('Saved', 'File saved successfully');
      loadFiles();
    } catch (error) {
      Alert.alert('Error', 'Failed to save file');
    }
  };

  const loadFile = (file: any) => {
    const lang = languages.find(l => l.key === file.language);
    if (lang) {
      setSelectedLanguage(lang);
      setCode(file.code);
      setCurrentFileName(file.name.replace(/\.[^/.]+$/, ''));
      setShowFilesModal(false);
      setShowOutput(false);
      loadTemplates(lang.key);
    }
  };

  const applyTemplate = (template: Template) => {
    setCode(template.code);
    setShowTemplateModal(false);
    setShowOutput(false);
    setCodeAnalysis(null);
  };

  const clearCode = () => {
    setCode('');
    setOutput('');
    setShowOutput(false);
    setShowWebPreview(false);
    setCodeAnalysis(null);
    setExecutionTime(null);
  };

  // Tutorial functions
  const nextTutorialStep = () => {
    if (currentTutorialStep < tutorialSteps.length - 1) {
      setCurrentTutorialStep(prev => prev + 1);
    } else {
      completeTutorial();
    }
  };

  const prevTutorialStep = () => {
    if (currentTutorialStep > 0) {
      setCurrentTutorialStep(prev => prev - 1);
    }
  };

  const completeTutorial = async () => {
    setShowTutorial(false);
    setTutorialCompleted(true);
    await AsyncStorage.setItem('tutorial_completed', 'true');
    Alert.alert('🎉 Congratulations!', 'You\'ve completed the tutorial. Start coding!');
  };

  const skipTutorial = async () => {
    setShowTutorial(false);
    setTutorialCompleted(true);
    await AsyncStorage.setItem('tutorial_completed', 'true');
  };

  const restartTutorial = () => {
    setCurrentTutorialStep(0);
    setShowTutorial(true);
  };

  // Advanced Panel unlock
  const handleVersionTap = async () => {
    const newCount = versionTapCount + 1;
    setVersionTapCount(newCount);
    
    if (newCount >= 3) {
      setAdvancedUnlocked(true);
      setShowAdvancedPanel(true);
      setVersionTapCount(0);
      await AsyncStorage.setItem('advanced_unlocked', 'true');
      if (Platform.OS !== 'web') Vibration.vibrate([50, 100, 50]);
      Alert.alert('🔓 Unlocked!', 'Advanced Panel is now available');
    }
    
    setTimeout(() => setVersionTapCount(0), 2000);
  };

  // Tooltip functions
  const showTooltip = (tooltipId: string) => {
    setActiveTooltip(tooltipId);
    setShowTooltipModal(true);
  };

  const getIconName = (icon: string): keyof typeof Ionicons.glyphMap => {
    const iconMap: Record<string, keyof typeof Ionicons.glyphMap> = {
      'logo-python': 'logo-python', 'logo-html5': 'logo-html5', 'logo-javascript': 'logo-javascript',
      'logo-css3': 'logo-css3', 'code-slash': 'code-slash', 'code-working': 'code-working',
      'document-text': 'document-text', 'server': 'server', 'hardware-chip': 'hardware-chip',
      'terminal': 'terminal', 'diamond': 'diamond', 'cafe': 'cafe', 'logo-apple': 'logo-apple',
    };
    return iconMap[icon] || 'code-slash';
  };

  const getComplexityColor = (complexity: string) => {
    switch (complexity) {
      case 'trivial': return colors.success;
      case 'simple': return colors.accent;
      case 'moderate': return colors.warning;
      case 'complex': return colors.error;
      default: return colors.secondary;
    }
  };

  if (loading) {
    return (
      <View style={[styles.loadingContainer, { backgroundColor: colors.background }]}>
        <ActivityIndicator size="large" color={colors.primary} />
        <Text style={[styles.loadingTitle, { color: colors.text }]}>CodeDock Quantum</Text>
        <Text style={[styles.loadingSubtitle, { color: colors.textMuted }]}>{CODENAME} Edition</Text>
      </View>
    );
  }

  const currentStep = tutorialSteps[currentTutorialStep];

  return (
    <SafeAreaView style={[styles.container, { backgroundColor: colors.background }]}>
      <StatusBar barStyle={theme === 'dark' ? 'light-content' : 'dark-content'} />
      
      {/* Header */}
      <View style={[styles.header, { backgroundColor: colors.surface, borderBottomColor: colors.border }]}>
        <Pressable style={styles.languageSelector} onPress={() => setShowLanguageModal(true)}
          onLongPress={() => showTooltip('language_selector')}>
          {selectedLanguage && (
            <>
              <View style={[styles.langIconBg, { backgroundColor: selectedLanguage.color + '20' }]}>
                <Ionicons name={getIconName(selectedLanguage.icon)} size={18} color={selectedLanguage.color} />
              </View>
              <View>
                <Text style={[styles.languageName, { color: colors.text }]}>{selectedLanguage.name}</Text>
                <Text style={[styles.languageVersion, { color: colors.textMuted }]}>
                  {selectedLanguage.display_name || selectedLanguage.version || selectedLanguage.extension}
                </Text>
              </View>
              <Ionicons name="chevron-down" size={16} color={colors.secondary} />
            </>
          )}
        </Pressable>
        
        <View style={styles.headerActions}>
          {/* HOTFIX: Connection Status Indicator */}
          {connectionStatus !== 'connected' && (
            <TouchableOpacity 
              style={[styles.headerButton, { backgroundColor: connectionStatus === 'disconnected' ? colors.error + '20' : colors.warning + '20' }]} 
              onPress={loadData}>
              <Ionicons 
                name={connectionStatus === 'disconnected' ? 'cloud-offline' : 'cloud-upload'} 
                size={18} 
                color={connectionStatus === 'disconnected' ? colors.error : colors.warning} 
              />
            </TouchableOpacity>
          )}
          {!tutorialCompleted && (
            <TouchableOpacity style={[styles.headerButton, { backgroundColor: colors.tutorial + '20' }]} 
              onPress={() => setShowTutorial(true)}>
              <Ionicons name="school" size={18} color={colors.tutorial} />
            </TouchableOpacity>
          )}
          <TouchableOpacity style={styles.headerButton} onPress={toggleTheme}>
            <Ionicons name={theme === 'dark' ? 'sunny' : 'moon'} size={20} color={colors.secondary} />
          </TouchableOpacity>
          <TouchableOpacity style={styles.headerButton} onPress={() => setShowSettingsModal(true)}>
            <Ionicons name="settings-outline" size={20} color={colors.secondary} />
          </TouchableOpacity>
        </View>
      </View>

      {/* HOTFIX: Error Banner */}
      {lastError && (
        <Animated.View style={[styles.errorBanner, { backgroundColor: colors.error + '15', borderColor: colors.error }]}>
          <View style={styles.errorBannerContent}>
            <Ionicons name="alert-circle" size={18} color={colors.error} />
            <Text style={[styles.errorBannerText, { color: colors.error }]}>{lastError.message}</Text>
          </View>
          {lastError.retry && (
            <TouchableOpacity style={[styles.errorBannerRetry, { backgroundColor: colors.error }]} onPress={loadData}>
              <Ionicons name="refresh" size={14} color="#FFF" />
              <Text style={styles.errorBannerRetryText}>Retry</Text>
            </TouchableOpacity>
          )}
        </Animated.View>
      )}

      {/* Toolbar */}
      <View style={[styles.toolbar, { backgroundColor: colors.surfaceAlt }]}>
        <ScrollView horizontal showsHorizontalScrollIndicator={false} contentContainerStyle={styles.toolbarContent}>
          <Pressable style={[styles.toolButton, { backgroundColor: colors.surface }]} 
            onPress={() => setShowTemplateModal(true)} onLongPress={() => showTooltip('templates_button')}>
            <Ionicons name="flash" size={15} color={colors.warning} />
            <Text style={[styles.toolButtonText, { color: colors.text }]}>Templates</Text>
          </Pressable>
          
          <Pressable style={[styles.toolButton, { backgroundColor: colors.surface }]} 
            onPress={() => setShowFilesModal(true)} onLongPress={() => showTooltip('files_button')}>
            <Ionicons name="folder" size={15} color={colors.accent} />
            <Text style={[styles.toolButtonText, { color: colors.text }]}>Files</Text>
          </Pressable>
          
          <Pressable style={[styles.toolButton, { backgroundColor: colors.surface }]} 
            onPress={saveFile} onLongPress={() => showTooltip('save_button')}>
            <Ionicons name="save" size={15} color={colors.success} />
            <Text style={[styles.toolButtonText, { color: colors.text }]}>Save</Text>
          </Pressable>
          
          <Pressable style={[styles.toolButton, { backgroundColor: colors.surface }]} 
            onPress={analyzeCode} onLongPress={() => showTooltip('analyze_button')}>
            <Ionicons name="analytics" size={15} color={colors.primary} />
            <Text style={[styles.toolButtonText, { color: colors.text }]}>Analyze</Text>
          </Pressable>
          
          <TouchableOpacity style={[styles.toolButton, { backgroundColor: colors.surface }]} onPress={clearCode}>
            <Ionicons name="trash" size={15} color={colors.error} />
            <Text style={[styles.toolButtonText, { color: colors.text }]}>Clear</Text>
          </TouchableOpacity>
        </ScrollView>
      </View>

      {/* AI Bar */}
      <Animated.View style={[styles.aiBar, { backgroundColor: colors.surface, borderBottomColor: colors.border, transform: [{ scale: pulseAnim }] }]}>
        <Pressable style={[styles.aiButton, { backgroundColor: colors.primary + '15', borderColor: colors.primary + '40' }]}
          onPress={() => setShowAIModal(true)} onLongPress={() => showTooltip('ai_assist_button')}>
          <Ionicons name="sparkles" size={18} color={colors.primary} />
          <Text style={[styles.aiButtonText, { color: colors.primary }]}>AI Assist</Text>
          <View style={[styles.aiBadge, { backgroundColor: colors.primary }]}>
            <Text style={styles.aiBadgeText}>GPT-4o</Text>
          </View>
        </Pressable>
        
        {codeAnalysis && (
          <TouchableOpacity style={[styles.analysisChip, { backgroundColor: getComplexityColor(codeAnalysis.complexity) + '20' }]}
            onPress={() => setShowAnalysisModal(true)}>
            <Text style={[styles.analysisChipText, { color: getComplexityColor(codeAnalysis.complexity) }]}>
              {codeAnalysis.complexity.toUpperCase()}
            </Text>
          </TouchableOpacity>
        )}
        
        <TouchableOpacity style={[styles.dockChip, { backgroundColor: colors.surfaceAlt }]} onPress={() => setShowDockModal(true)}>
          <Ionicons name="grid" size={14} color={colors.accent} />
          <Text style={[styles.dockChipText, { color: colors.accent }]}>Dock</Text>
        </TouchableOpacity>
      </Animated.View>

      {/* Code Editor */}
      <KeyboardAvoidingView style={styles.mainContent} behavior={Platform.OS === 'ios' ? 'padding' : 'height'}>
        <View style={[styles.editorContainer, { backgroundColor: colors.codeBackground }]}>
          <View style={[styles.editorHeader, { borderBottomColor: colors.borderSubtle }]}>
            <View style={[styles.editorTab, { backgroundColor: colors.primary + '20', borderBottomColor: colors.primary }]}>
              <TextInput style={[styles.fileNameInput, { color: colors.text }]} value={currentFileName}
                onChangeText={setCurrentFileName} placeholder="filename" placeholderTextColor={colors.textMuted} />
              <Text style={[styles.extensionText, { color: colors.textMuted }]}>{selectedLanguage?.extension || ''}</Text>
            </View>
            {executionTime !== null && (
              <Text style={[styles.execTimeText, { color: colors.success }]}>{executionTime.toFixed(1)}ms</Text>
            )}
          </View>
          
          <ScrollView style={styles.editorScroll} keyboardShouldPersistTaps="handled">
            <View style={styles.editorContent}>
              <View style={[styles.lineNumbers, { backgroundColor: colors.surface + '50' }]}>
                {(code || ' ').split('\n').map((_, i) => (
                  <Text key={i} style={[styles.lineNumber, { color: colors.textMuted }]}>{i + 1}</Text>
                ))}
              </View>
              <TextInput style={[styles.codeInput, { color: colors.text }]} value={code} onChangeText={setCode}
                multiline autoCapitalize="none" autoCorrect={false} spellCheck={false}
                placeholder="// Start coding here..." placeholderTextColor={colors.textMuted} textAlignVertical="top" />
            </View>
          </ScrollView>
        </View>

        {/* Output */}
        {(showOutput || showWebPreview) && (
          <View style={[styles.outputContainer, { backgroundColor: colors.surface, borderTopColor: colors.border }]}>
            <View style={[styles.outputHeader, { borderBottomColor: colors.borderSubtle }]}>
              <View style={styles.outputTitleRow}>
                <Ionicons name={showWebPreview ? "globe" : "terminal"} size={16} color={colors.accent} />
                <Text style={[styles.outputTitle, { color: colors.text }]}>{showWebPreview ? 'Preview' : 'Output'}</Text>
              </View>
              <TouchableOpacity onPress={() => { setShowOutput(false); setShowWebPreview(false); }}>
                <Ionicons name="close" size={20} color={colors.secondary} />
              </TouchableOpacity>
            </View>
            {showWebPreview ? (
              <WebView style={styles.webPreview} source={{ html: htmlPreview }} originWhitelist={['*']} javaScriptEnabled />
            ) : (
              <ScrollView style={styles.outputScroll}>
                <Text style={[styles.outputText, { color: colors.text }]}>{output || 'No output'}</Text>
              </ScrollView>
            )}
          </View>
        )}
      </KeyboardAvoidingView>

      {/* Run Button */}
      <View style={[styles.bottomBar, { backgroundColor: colors.surface, borderTopColor: colors.border }]}>
        <Pressable style={[styles.runButton, { backgroundColor: selectedLanguage?.executable ? colors.success : colors.surfaceAlt }]}
          onPress={executeCode} onLongPress={() => showTooltip('run_button')} disabled={isExecuting || !selectedLanguage?.executable}>
          {isExecuting ? <ActivityIndicator size="small" color="#FFF" /> : (
            <>
              <Ionicons name={selectedLanguage?.key === 'html' ? 'eye' : 'play'} size={22} color="#FFF" />
              <Text style={styles.runButtonText}>{selectedLanguage?.key === 'html' ? 'Preview' : 'Run'}</Text>
            </>
          )}
        </Pressable>
      </View>

      {/* TEACHING MODE MODAL */}
      <Modal visible={showTutorial} transparent animationType="fade" onRequestClose={skipTutorial}>
        <View style={styles.tutorialOverlay}>
          <View style={[styles.tutorialCard, { backgroundColor: colors.surface }]}>
            <View style={[styles.tutorialHeader, { borderBottomColor: colors.border }]}>
              <View style={styles.tutorialProgress}>
                <Text style={[styles.tutorialStep, { color: colors.tutorial }]}>
                  Step {currentTutorialStep + 1} of {tutorialSteps.length}
                </Text>
                <View style={[styles.progressBar, { backgroundColor: colors.surfaceAlt }]}>
                  <View style={[styles.progressFill, { 
                    backgroundColor: colors.tutorial, 
                    width: `${((currentTutorialStep + 1) / tutorialSteps.length) * 100}%` 
                  }]} />
                </View>
              </View>
              <TouchableOpacity onPress={skipTutorial}>
                <Text style={[styles.skipText, { color: colors.textMuted }]}>Skip</Text>
              </TouchableOpacity>
            </View>
            
            {currentStep && (
              <ScrollView style={styles.tutorialContent}>
                <View style={[styles.tutorialIcon, { backgroundColor: colors.tutorial + '20' }]}>
                  <Ionicons name={
                    currentStep.key === 'welcome' ? 'rocket' :
                    currentStep.key === 'select_language' ? 'code-slash' :
                    currentStep.key === 'use_templates' ? 'flash' :
                    currentStep.key === 'write_code' ? 'create' :
                    currentStep.key === 'run_code' ? 'play' :
                    currentStep.key === 'view_output' ? 'terminal' :
                    currentStep.key === 'use_ai' ? 'sparkles' :
                    currentStep.key === 'analyze_code' ? 'analytics' :
                    currentStep.key === 'save_file' ? 'save' :
                    currentStep.key === 'complete' ? 'trophy' : 'bulb'
                  } size={40} color={colors.tutorial} />
                </View>
                
                <Text style={[styles.tutorialTitle, { color: colors.text }]}>{currentStep.title}</Text>
                <Text style={[styles.tutorialDesc, { color: colors.textSecondary }]}>{currentStep.description}</Text>
                <Text style={[styles.tutorialContentText, { color: colors.text }]}>{currentStep.content}</Text>
                
                {currentStep.tips && (
                  <View style={[styles.tutorialTips, { backgroundColor: colors.surfaceAlt }]}>
                    <Text style={[styles.tipsTitle, { color: colors.tutorial }]}>💡 Tips</Text>
                    {currentStep.tips.map((tip, i) => (
                      <Text key={i} style={[styles.tipText, { color: colors.textSecondary }]}>• {tip}</Text>
                    ))}
                  </View>
                )}
                
                {currentStep.celebration && (
                  <Text style={[styles.celebration, { color: colors.tutorial }]}>🎉 🚀 ⭐</Text>
                )}
              </ScrollView>
            )}
            
            <View style={[styles.tutorialNav, { borderTopColor: colors.border }]}>
              {currentTutorialStep > 0 ? (
                <TouchableOpacity style={[styles.tutorialNavBtn, { backgroundColor: colors.surfaceAlt }]} onPress={prevTutorialStep}>
                  <Ionicons name="arrow-back" size={18} color={colors.text} />
                  <Text style={[styles.tutorialNavText, { color: colors.text }]}>Back</Text>
                </TouchableOpacity>
              ) : <View style={styles.tutorialNavBtn} />}
              
              <TouchableOpacity style={[styles.tutorialNavBtn, styles.tutorialNavPrimary, { backgroundColor: colors.tutorial }]} 
                onPress={nextTutorialStep}>
                <Text style={styles.tutorialNavTextPrimary}>
                  {currentTutorialStep === tutorialSteps.length - 1 ? 'Finish' : 'Next'}
                </Text>
                <Ionicons name={currentTutorialStep === tutorialSteps.length - 1 ? 'checkmark' : 'arrow-forward'} size={18} color="#FFF" />
              </TouchableOpacity>
            </View>
          </View>
        </View>
      </Modal>

      {/* TOOLTIP MODAL */}
      <Modal visible={showTooltipModal} transparent animationType="fade" onRequestClose={() => setShowTooltipModal(false)}>
        <TouchableWithoutFeedback onPress={() => setShowTooltipModal(false)}>
          <View style={styles.tooltipOverlay}>
            <TouchableWithoutFeedback>
              <View style={[styles.tooltipCard, { backgroundColor: colors.surface }]}>
                {activeTooltip && tooltips[activeTooltip] && (
                  <>
                    <View style={styles.tooltipHeader}>
                      <Ionicons name="information-circle" size={24} color={colors.primary} />
                      <Text style={[styles.tooltipTitle, { color: colors.text }]}>{tooltips[activeTooltip].title}</Text>
                    </View>
                    <Text style={[styles.tooltipDesc, { color: colors.textSecondary }]}>{tooltips[activeTooltip].description}</Text>
                    {tooltips[activeTooltip].tips && (
                      <View style={styles.tooltipTips}>
                        {tooltips[activeTooltip].tips?.map((tip, i) => (
                          <Text key={i} style={[styles.tooltipTip, { color: colors.textMuted }]}>• {tip}</Text>
                        ))}
                      </View>
                    )}
                    {tooltips[activeTooltip].shortcut && (
                      <View style={[styles.shortcutBadge, { backgroundColor: colors.surfaceAlt }]}>
                        <Ionicons name="keypad" size={14} color={colors.accent} />
                        <Text style={[styles.shortcutText, { color: colors.accent }]}>{tooltips[activeTooltip].shortcut}</Text>
                      </View>
                    )}
                  </>
                )}
                <TouchableOpacity style={[styles.tooltipCloseBtn, { backgroundColor: colors.primary }]} 
                  onPress={() => setShowTooltipModal(false)}>
                  <Text style={styles.tooltipCloseBtnText}>Got it</Text>
                </TouchableOpacity>
              </View>
            </TouchableWithoutFeedback>
          </View>
        </TouchableWithoutFeedback>
      </Modal>

      {/* LANGUAGE DOCK MODAL */}
      <Modal visible={showDockModal} transparent animationType="slide" onRequestClose={() => setShowDockModal(false)}>
        <View style={styles.modalOverlay}>
          <View style={[styles.modalContent, styles.dockModalContent, { backgroundColor: colors.surface }]}>
            <View style={[styles.modalHeader, { borderBottomColor: colors.border }]}>
              <View style={styles.modalTitleRow}>
                <Ionicons name="grid" size={22} color={colors.accent} />
                <Text style={[styles.modalTitle, { color: colors.text }]}>Language Dock</Text>
              </View>
              <TouchableOpacity onPress={() => setShowDockModal(false)}>
                <Ionicons name="close" size={24} color={colors.secondary} />
              </TouchableOpacity>
            </View>
            
            <ScrollView>
              <Text style={[styles.dockSectionTitle, { color: colors.textMuted }]}>TIER 1 - INSTALLED</Text>
              {availableDocks.filter(d => d.tier === 1).map(dock => (
                <TouchableOpacity key={dock.key} style={[styles.dockItem, { borderBottomColor: colors.borderSubtle }]}
                  onPress={() => { selectLanguage(dock as any); setShowDockModal(false); }}>
                  <View style={[styles.dockIcon, { backgroundColor: dock.color + '20' }]}>
                    <Ionicons name={getIconName(dock.icon || 'code-slash')} size={22} color={dock.color} />
                  </View>
                  <View style={styles.dockInfo}>
                    <Text style={[styles.dockName, { color: colors.text }]}>{dock.display_name || dock.name}</Text>
                    <Text style={[styles.dockDesc, { color: colors.textMuted }]} numberOfLines={1}>{dock.description}</Text>
                  </View>
                  {dock.executable && (
                    <View style={[styles.statusBadge, { backgroundColor: colors.success + '20' }]}>
                      <Text style={[styles.statusText, { color: colors.success }]}>Active</Text>
                    </View>
                  )}
                </TouchableOpacity>
              ))}
              
              <Text style={[styles.dockSectionTitle, { color: colors.textMuted, marginTop: 20 }]}>TIER 2 - COMING SOON</Text>
              {availableDocks.filter(d => d.tier === 2).map(dock => (
                <View key={dock.key} style={[styles.dockItem, styles.dockItemDisabled, { borderBottomColor: colors.borderSubtle }]}>
                  <View style={[styles.dockIcon, { backgroundColor: dock.color + '10' }]}>
                    <Ionicons name={getIconName(dock.icon || 'code-slash')} size={22} color={dock.color + '80'} />
                  </View>
                  <View style={styles.dockInfo}>
                    <Text style={[styles.dockName, { color: colors.textMuted }]}>{dock.display_name || dock.name}</Text>
                    <Text style={[styles.dockDesc, { color: colors.textMuted }]} numberOfLines={1}>{dock.description}</Text>
                  </View>
                  <View style={[styles.statusBadge, { backgroundColor: colors.warning + '20' }]}>
                    <Text style={[styles.statusText, { color: colors.warning }]}>Soon</Text>
                  </View>
                </View>
              ))}
              
              <Text style={[styles.dockSectionTitle, { color: colors.textMuted, marginTop: 20 }]}>TIER 3 - EXPANSION SLOTS</Text>
              <View style={styles.dockGrid}>
                {availableDocks.filter(d => d.tier === 3).map(dock => (
                  <View key={dock.key} style={[styles.dockGridItem, { backgroundColor: colors.surfaceAlt }]}>
                    <Ionicons name={getIconName(dock.icon || 'code-slash')} size={24} color={dock.color + '60'} />
                    <Text style={[styles.dockGridName, { color: colors.textMuted }]}>{dock.name}</Text>
                  </View>
                ))}
              </View>
              
              <Text style={[styles.dockFooter, { color: colors.textMuted }]}>
                {availableDocks.length} languages • {availableDocks.filter(d => d.expansion_ready).length} expansion ready
              </Text>
            </ScrollView>
          </View>
        </View>
      </Modal>

      {/* SETTINGS MODAL */}
      <Modal visible={showSettingsModal} transparent animationType="slide" onRequestClose={() => setShowSettingsModal(false)}>
        <View style={styles.modalOverlay}>
          <View style={[styles.modalContent, { backgroundColor: colors.surface }]}>
            <View style={[styles.modalHeader, { borderBottomColor: colors.border }]}>
              <Text style={[styles.modalTitle, { color: colors.text }]}>Settings</Text>
              <TouchableOpacity onPress={() => setShowSettingsModal(false)}>
                <Ionicons name="close" size={24} color={colors.secondary} />
              </TouchableOpacity>
            </View>
            
            <ScrollView style={styles.settingsContent}>
              <TouchableOpacity style={[styles.settingItem, { borderBottomColor: colors.borderSubtle }]} onPress={toggleTheme}>
                <View style={styles.settingItemLeft}>
                  <View style={[styles.settingIcon, { backgroundColor: colors.warning + '20' }]}>
                    <Ionicons name={theme === 'dark' ? 'moon' : 'sunny'} size={20} color={colors.warning} />
                  </View>
                  <Text style={[styles.settingItemText, { color: colors.text }]}>Theme</Text>
                </View>
                <Text style={[styles.settingItemValue, { color: colors.textSecondary }]}>{theme === 'dark' ? 'Dark' : 'Light'}</Text>
              </TouchableOpacity>
              
              <TouchableOpacity style={[styles.settingItem, { borderBottomColor: colors.borderSubtle }]} 
                onPress={() => { setShowSettingsModal(false); setShowAddonModal(true); }}>
                <View style={styles.settingItemLeft}>
                  <View style={[styles.settingIcon, { backgroundColor: colors.primary + '20' }]}>
                    <Ionicons name="extension-puzzle" size={20} color={colors.primary} />
                  </View>
                  <Text style={[styles.settingItemText, { color: colors.text }]}>Language Addons</Text>
                </View>
                <Ionicons name="chevron-forward" size={20} color={colors.secondary} />
              </TouchableOpacity>
              
              <TouchableOpacity style={[styles.settingItem, { borderBottomColor: colors.borderSubtle }]} 
                onPress={restartTutorial}>
                <View style={styles.settingItemLeft}>
                  <View style={[styles.settingIcon, { backgroundColor: colors.tutorial + '20' }]}>
                    <Ionicons name="school" size={20} color={colors.tutorial} />
                  </View>
                  <Text style={[styles.settingItemText, { color: colors.text }]}>Restart Tutorial</Text>
                </View>
                <Ionicons name="refresh" size={20} color={colors.secondary} />
              </TouchableOpacity>
              
              {advancedUnlocked && (
                <TouchableOpacity style={[styles.settingItem, { borderBottomColor: colors.borderSubtle }]} 
                  onPress={() => { setShowSettingsModal(false); setShowAdvancedPanel(true); }}>
                  <View style={styles.settingItemLeft}>
                    <View style={[styles.settingIcon, { backgroundColor: colors.error + '20' }]}>
                      <Ionicons name="flask" size={20} color={colors.error} />
                    </View>
                    <Text style={[styles.settingItemText, { color: colors.text }]}>Advanced Panel</Text>
                  </View>
                  <View style={[styles.unlockBadge, { backgroundColor: colors.success + '20' }]}>
                    <Text style={[styles.unlockBadgeText, { color: colors.success }]}>UNLOCKED</Text>
                  </View>
                </TouchableOpacity>
              )}
              
              <Pressable style={[styles.settingItem, { borderBottomColor: colors.borderSubtle }]} onPress={handleVersionTap}>
                <View style={styles.settingItemLeft}>
                  <View style={[styles.settingIcon, { backgroundColor: colors.accent + '20' }]}>
                    <Ionicons name="information-circle" size={20} color={colors.accent} />
                  </View>
                  <Text style={[styles.settingItemText, { color: colors.text }]}>Version</Text>
                </View>
                <Text style={[styles.settingItemValue, { color: colors.textSecondary }]}>{VERSION} {CODENAME}</Text>
              </Pressable>
              
              {!advancedUnlocked && versionTapCount > 0 && (
                <Text style={[styles.unlockHint, { color: colors.textMuted }]}>
                  {3 - versionTapCount} more taps to unlock advanced features...
                </Text>
              )}
            </ScrollView>
          </View>
        </View>
      </Modal>

      {/* ADVANCED PANEL MODAL */}
      <Modal visible={showAdvancedPanel} transparent animationType="slide" onRequestClose={() => setShowAdvancedPanel(false)}>
        <View style={styles.modalOverlay}>
          <View style={[styles.modalContent, { backgroundColor: colors.surface }]}>
            <View style={[styles.modalHeader, { borderBottomColor: colors.border }]}>
              <View style={styles.modalTitleRow}>
                <Ionicons name="flask" size={22} color={colors.error} />
                <Text style={[styles.modalTitle, { color: colors.text }]}>Advanced Panel</Text>
              </View>
              <TouchableOpacity onPress={() => setShowAdvancedPanel(false)}>
                <Ionicons name="close" size={24} color={colors.secondary} />
              </TouchableOpacity>
            </View>
            
            <ScrollView style={styles.advancedContent}>
              <View style={[styles.advancedWarning, { backgroundColor: colors.warning + '20' }]}>
                <Ionicons name="warning" size={20} color={colors.warning} />
                <Text style={[styles.advancedWarningText, { color: colors.warning }]}>
                  These settings are for power users. Incorrect values may cause issues.
                </Text>
              </View>
              
              <View style={styles.advancedSection}>
                <Text style={[styles.advancedLabel, { color: colors.text }]}>Execution Timeout (seconds)</Text>
                <View style={styles.advancedSlider}>
                  {[5, 10, 15, 30, 60].map(val => (
                    <TouchableOpacity key={val} 
                      style={[styles.sliderOption, advancedSettings.execution_timeout === val && { backgroundColor: colors.primary }]}
                      onPress={() => setAdvancedSettings(s => ({ ...s, execution_timeout: val }))}>
                      <Text style={[styles.sliderText, { color: advancedSettings.execution_timeout === val ? '#FFF' : colors.text }]}>{val}s</Text>
                    </TouchableOpacity>
                  ))}
                </View>
              </View>
              
              <View style={styles.advancedSection}>
                <Text style={[styles.advancedLabel, { color: colors.text }]}>Memory Limit (MB)</Text>
                <View style={styles.advancedSlider}>
                  {[128, 256, 512, 1024].map(val => (
                    <TouchableOpacity key={val}
                      style={[styles.sliderOption, advancedSettings.memory_limit_mb === val && { backgroundColor: colors.primary }]}
                      onPress={() => setAdvancedSettings(s => ({ ...s, memory_limit_mb: val }))}>
                      <Text style={[styles.sliderText, { color: advancedSettings.memory_limit_mb === val ? '#FFF' : colors.text }]}>{val}</Text>
                    </TouchableOpacity>
                  ))}
                </View>
              </View>
              
              <View style={styles.advancedSection}>
                <Text style={[styles.advancedLabel, { color: colors.text }]}>Security Level</Text>
                <View style={styles.advancedSlider}>
                  {['strict', 'standard', 'permissive'].map(val => (
                    <TouchableOpacity key={val}
                      style={[styles.sliderOption, styles.sliderOptionWide, advancedSettings.security_level === val && { backgroundColor: colors.primary }]}
                      onPress={() => setAdvancedSettings(s => ({ ...s, security_level: val }))}>
                      <Text style={[styles.sliderText, { color: advancedSettings.security_level === val ? '#FFF' : colors.text }]}>{val}</Text>
                    </TouchableOpacity>
                  ))}
                </View>
              </View>
              
              <TouchableOpacity style={[styles.advancedToggle, { borderBottomColor: colors.borderSubtle }]}
                onPress={() => setAdvancedSettings(s => ({ ...s, debug_mode: !s.debug_mode }))}>
                <Text style={[styles.advancedToggleText, { color: colors.text }]}>Debug Mode</Text>
                <Ionicons name={advancedSettings.debug_mode ? 'checkbox' : 'square-outline'} size={24} 
                  color={advancedSettings.debug_mode ? colors.success : colors.textMuted} />
              </TouchableOpacity>
              
              <TouchableOpacity style={[styles.advancedToggle, { borderBottomColor: colors.borderSubtle }]}
                onPress={() => setAdvancedSettings(s => ({ ...s, experimental_features: !s.experimental_features }))}>
                <Text style={[styles.advancedToggleText, { color: colors.text }]}>Experimental Features</Text>
                <Ionicons name={advancedSettings.experimental_features ? 'checkbox' : 'square-outline'} size={24}
                  color={advancedSettings.experimental_features ? colors.success : colors.textMuted} />
              </TouchableOpacity>
            </ScrollView>
          </View>
        </View>
      </Modal>

      {/* LANGUAGE MODAL */}
      <Modal visible={showLanguageModal} transparent animationType="slide" onRequestClose={() => setShowLanguageModal(false)}>
        <View style={styles.modalOverlay}>
          <View style={[styles.modalContent, { backgroundColor: colors.surface }]}>
            <View style={[styles.modalHeader, { borderBottomColor: colors.border }]}>
              <Text style={[styles.modalTitle, { color: colors.text }]}>Select Language</Text>
              <TouchableOpacity onPress={() => setShowLanguageModal(false)}>
                <Ionicons name="close" size={24} color={colors.secondary} />
              </TouchableOpacity>
            </View>
            <FlatList data={languages.filter(l => l.executable || l.type === 'addon')} keyExtractor={item => item.key}
              renderItem={({ item }) => (
                <TouchableOpacity style={[styles.languageItem, { borderBottomColor: colors.borderSubtle }, 
                  selectedLanguage?.key === item.key && { backgroundColor: colors.primary + '10' }]}
                  onPress={() => selectLanguage(item)}>
                  <View style={[styles.langItemIcon, { backgroundColor: item.color + '20' }]}>
                    <Ionicons name={getIconName(item.icon)} size={22} color={item.color} />
                  </View>
                  <View style={styles.languageItemInfo}>
                    <Text style={[styles.languageItemName, { color: colors.text }]}>{item.name}</Text>
                    <Text style={[styles.languageItemVersion, { color: colors.textMuted }]}>
                      {item.display_name || item.version || item.extension}
                    </Text>
                  </View>
                  {item.executable && (
                    <View style={[styles.executableBadge, { backgroundColor: colors.success + '20' }]}>
                      <Ionicons name="checkmark-circle" size={12} color={colors.success} />
                    </View>
                  )}
                </TouchableOpacity>
              )}
            />
          </View>
        </View>
      </Modal>

      {/* TEMPLATES MODAL */}
      <Modal visible={showTemplateModal} transparent animationType="slide" onRequestClose={() => setShowTemplateModal(false)}>
        <View style={styles.modalOverlay}>
          <View style={[styles.modalContent, { backgroundColor: colors.surface }]}>
            <View style={[styles.modalHeader, { borderBottomColor: colors.border }]}>
              <Text style={[styles.modalTitle, { color: colors.text }]}>{selectedLanguage?.name} Templates</Text>
              <TouchableOpacity onPress={() => setShowTemplateModal(false)}>
                <Ionicons name="close" size={24} color={colors.secondary} />
              </TouchableOpacity>
            </View>
            <FlatList data={templates} keyExtractor={item => item.key}
              renderItem={({ item }) => (
                <TouchableOpacity style={[styles.templateItem, { borderBottomColor: colors.borderSubtle }]}
                  onPress={() => applyTemplate(item)}>
                  <Ionicons name="document-text" size={20} color={colors.primary} />
                  <View style={styles.templateInfo}>
                    <Text style={[styles.templateName, { color: colors.text }]}>{item.name}</Text>
                    {item.description && (
                      <Text style={[styles.templateDesc, { color: colors.textMuted }]} numberOfLines={1}>{item.description}</Text>
                    )}
                  </View>
                  {item.complexity && (
                    <View style={[styles.complexityBadge, { backgroundColor: getComplexityColor(item.complexity) + '20' }]}>
                      <Text style={[styles.complexityText, { color: getComplexityColor(item.complexity) }]}>{item.complexity}</Text>
                    </View>
                  )}
                </TouchableOpacity>
              )}
              ListEmptyComponent={<Text style={[styles.emptyText, { color: colors.textMuted }]}>No templates available</Text>}
            />
          </View>
        </View>
      </Modal>

      {/* FILES MODAL */}
      <Modal visible={showFilesModal} transparent animationType="slide" onRequestClose={() => setShowFilesModal(false)}>
        <View style={styles.modalOverlay}>
          <View style={[styles.modalContent, { backgroundColor: colors.surface }]}>
            <View style={[styles.modalHeader, { borderBottomColor: colors.border }]}>
              <Text style={[styles.modalTitle, { color: colors.text }]}>Saved Files</Text>
              <TouchableOpacity onPress={() => setShowFilesModal(false)}>
                <Ionicons name="close" size={24} color={colors.secondary} />
              </TouchableOpacity>
            </View>
            <FlatList data={savedFiles} keyExtractor={item => item.id}
              renderItem={({ item }) => (
                <TouchableOpacity style={[styles.fileItem, { borderBottomColor: colors.borderSubtle }]} onPress={() => loadFile(item)}>
                  <Ionicons name="document" size={20} color={colors.accent} />
                  <View style={styles.fileItemInfo}>
                    <Text style={[styles.fileName, { color: colors.text }]}>{item.name}</Text>
                    <Text style={[styles.fileDate, { color: colors.textMuted }]}>{new Date(item.updated_at).toLocaleDateString()}</Text>
                  </View>
                </TouchableOpacity>
              )}
              ListEmptyComponent={<Text style={[styles.emptyText, { color: colors.textMuted }]}>No saved files</Text>}
            />
          </View>
        </View>
      </Modal>

      {/* AI MODAL */}
      <Modal visible={showAIModal} transparent animationType="slide" onRequestClose={() => setShowAIModal(false)}>
        <View style={styles.modalOverlay}>
          <View style={[styles.modalContent, styles.aiModalContent, { backgroundColor: colors.surface }]}>
            <View style={[styles.modalHeader, { borderBottomColor: colors.border }]}>
              <View style={styles.modalTitleRow}>
                <Ionicons name="sparkles" size={22} color={colors.primary} />
                <Text style={[styles.modalTitle, { color: colors.text }]}>AI Assistant</Text>
              </View>
              <TouchableOpacity onPress={() => { setShowAIModal(false); setSelectedAIMode(null); setAIResponse(''); }}>
                <Ionicons name="close" size={24} color={colors.secondary} />
              </TouchableOpacity>
            </View>
            
            {!selectedAIMode ? (
              <FlatList data={aiModes} keyExtractor={item => item.key} numColumns={2} contentContainerStyle={styles.aiModeGrid}
                renderItem={({ item }) => (
                  <TouchableOpacity style={[styles.aiModeCard, { backgroundColor: colors.surfaceAlt, borderColor: colors.border }]}
                    onPress={() => askAI(item)}>
                    <Ionicons name={
                      item.key === 'explain' ? 'bulb' : item.key === 'debug' ? 'bug' : item.key === 'optimize' ? 'rocket' :
                      item.key === 'complete' ? 'create' : item.key === 'refactor' ? 'construct' : item.key === 'document' ? 'document-text' :
                      item.key === 'test_gen' ? 'flask' : item.key === 'security_audit' ? 'shield-checkmark' :
                      item.key === 'teach' ? 'school' : item.key === 'review' ? 'eye' : item.key === 'architecture' ? 'git-branch' : 'swap-horizontal'
                    } size={28} color={colors.primary} />
                    <Text style={[styles.aiModeName, { color: colors.text }]}>{item.name}</Text>
                    <Text style={[styles.aiModeDesc, { color: colors.textMuted }]} numberOfLines={2}>{item.description}</Text>
                  </TouchableOpacity>
                )}
              />
            ) : (
              <View style={styles.aiResponseContainer}>
                <TouchableOpacity style={styles.aiBackButton} onPress={() => { setSelectedAIMode(null); setAIResponse(''); }}>
                  <Ionicons name="arrow-back" size={20} color={colors.primary} />
                  <Text style={[styles.aiBackText, { color: colors.primary }]}>Back</Text>
                </TouchableOpacity>
                {isAILoading ? (
                  <View style={styles.aiLoadingContainer}>
                    <ActivityIndicator size="large" color={colors.primary} />
                    <Text style={[styles.aiLoadingText, { color: colors.textSecondary }]}>Analyzing with GPT-4o...</Text>
                  </View>
                ) : (
                  <ScrollView style={styles.aiResponseScroll}>
                    <Text style={[styles.aiResponseText, { color: colors.text }]}>{aiResponse}</Text>
                  </ScrollView>
                )}
              </View>
            )}
          </View>
        </View>
      </Modal>

      {/* ANALYSIS MODAL */}
      <Modal visible={showAnalysisModal} transparent animationType="slide" onRequestClose={() => setShowAnalysisModal(false)}>
        <View style={styles.modalOverlay}>
          <View style={[styles.modalContent, styles.analysisModalContent, { backgroundColor: colors.surface }]}>
            <View style={[styles.modalHeader, { borderBottomColor: colors.border }]}>
              <Text style={[styles.modalTitle, { color: colors.text }]}>Code Analysis</Text>
              <TouchableOpacity onPress={() => setShowAnalysisModal(false)}>
                <Ionicons name="close" size={24} color={colors.secondary} />
              </TouchableOpacity>
            </View>
            {codeAnalysis && (
              <ScrollView style={styles.analysisContent}>
                <View style={[styles.analysisCard, { backgroundColor: colors.surfaceAlt }]}>
                  <Text style={[styles.analysisLabel, { color: colors.textSecondary }]}>Complexity</Text>
                  <View style={[styles.complexityDisplay, { backgroundColor: getComplexityColor(codeAnalysis.complexity) + '20' }]}>
                    <Text style={[styles.complexityValue, { color: getComplexityColor(codeAnalysis.complexity) }]}>
                      {codeAnalysis.complexity.toUpperCase()}
                    </Text>
                  </View>
                </View>
                <View style={styles.analysisGrid}>
                  {[
                    { label: 'Lines', value: codeAnalysis.lines_of_code },
                    { label: 'Cyclomatic', value: codeAnalysis.cyclomatic_complexity },
                    { label: 'Functions', value: codeAnalysis.functions_count },
                    { label: 'Classes', value: codeAnalysis.classes_count },
                  ].map((item, i) => (
                    <View key={i} style={[styles.analysisGridItem, { backgroundColor: colors.surfaceAlt }]}>
                      <Text style={[styles.analysisGridValue, { color: colors.text }]}>{item.value}</Text>
                      <Text style={[styles.analysisGridLabel, { color: colors.textMuted }]}>{item.label}</Text>
                    </View>
                  ))}
                </View>
              </ScrollView>
            )}
          </View>
        </View>
      </Modal>

      {/* ADDON MODAL */}
      <Modal visible={showAddonModal} transparent animationType="slide" onRequestClose={() => setShowAddonModal(false)}>
        <View style={styles.modalOverlay}>
          <View style={[styles.modalContent, { backgroundColor: colors.surface }]}>
            <View style={[styles.modalHeader, { borderBottomColor: colors.border }]}>
              <Text style={[styles.modalTitle, { color: colors.text }]}>Add Language Addon</Text>
              <TouchableOpacity onPress={() => setShowAddonModal(false)}>
                <Ionicons name="close" size={24} color={colors.secondary} />
              </TouchableOpacity>
            </View>
            <AddAddonForm colors={colors} onClose={() => setShowAddonModal(false)} onAdded={loadData} />
          </View>
        </View>
      </Modal>
    </SafeAreaView>
  );
}

// Add Addon Form Component
function AddAddonForm({ colors, onClose, onAdded }: { colors: any; onClose: () => void; onAdded: () => void }) {
  const [name, setName] = useState('');
  const [extension, setExtension] = useState('');
  const [description, setDescription] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    if (!name.trim() || !extension.trim()) {
      Alert.alert('Error', 'Name and extension are required');
      return;
    }
    setLoading(true);
    try {
      await axios.post(`${API_URL}/api/addons`, {
        language_key: name.toLowerCase().replace(/[^a-z0-9]/g, '_'),
        name: name.trim(),
        extension: extension.startsWith('.') ? extension : `.${extension}`,
        description: description.trim(),
        icon: 'code-slash', color: '#6B7280', executable: false,
      });
      Alert.alert('Success', 'Addon added');
      onAdded();
      onClose();
    } catch (error: any) {
      Alert.alert('Error', error.response?.data?.detail || 'Failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <ScrollView style={{ padding: 20 }}>
      <Text style={[styles.inputLabel, { color: colors.text }]}>Language Name *</Text>
      <TextInput style={[styles.textInput, { backgroundColor: colors.surfaceAlt, color: colors.text, borderColor: colors.border }]}
        value={name} onChangeText={setName} placeholder="e.g., Rust" placeholderTextColor={colors.textMuted} />
      <Text style={[styles.inputLabel, { color: colors.text }]}>Extension *</Text>
      <TextInput style={[styles.textInput, { backgroundColor: colors.surfaceAlt, color: colors.text, borderColor: colors.border }]}
        value={extension} onChangeText={setExtension} placeholder="e.g., .rs" placeholderTextColor={colors.textMuted} />
      <Text style={[styles.inputLabel, { color: colors.text }]}>Description</Text>
      <TextInput style={[styles.textInput, styles.textArea, { backgroundColor: colors.surfaceAlt, color: colors.text, borderColor: colors.border }]}
        value={description} onChangeText={setDescription} placeholder="Brief description" placeholderTextColor={colors.textMuted} multiline />
      <TouchableOpacity style={[styles.submitButton, { backgroundColor: colors.primary }]} onPress={handleSubmit} disabled={loading}>
        {loading ? <ActivityIndicator size="small" color="#FFF" /> : <Text style={styles.submitButtonText}>Add Language</Text>}
      </TouchableOpacity>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1 },
  loadingContainer: { flex: 1, justifyContent: 'center', alignItems: 'center' },
  loadingTitle: { marginTop: 20, fontSize: 24, fontWeight: '700' },
  loadingSubtitle: { marginTop: 4, fontSize: 14 },
  header: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', paddingHorizontal: 16, paddingVertical: 12, borderBottomWidth: 1 },
  languageSelector: { flexDirection: 'row', alignItems: 'center', gap: 10 },
  langIconBg: { width: 36, height: 36, borderRadius: 8, alignItems: 'center', justifyContent: 'center' },
  languageName: { fontSize: 16, fontWeight: '600' },
  languageVersion: { fontSize: 11 },
  headerActions: { flexDirection: 'row', gap: 4 },
  headerButton: { padding: 8, borderRadius: 8 },
  // HOTFIX: Error Banner Styles
  errorBanner: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', paddingHorizontal: 12, paddingVertical: 8, borderWidth: 1, borderRadius: 0 },
  errorBannerContent: { flexDirection: 'row', alignItems: 'center', gap: 8, flex: 1 },
  errorBannerText: { fontSize: 13, fontWeight: '500' },
  errorBannerRetry: { flexDirection: 'row', alignItems: 'center', paddingHorizontal: 12, paddingVertical: 6, borderRadius: 6, gap: 4 },
  errorBannerRetryText: { color: '#FFF', fontSize: 12, fontWeight: '600' },
  toolbar: { paddingVertical: 8 },
  toolbarContent: { paddingHorizontal: 12, gap: 8 },
  toolButton: { flexDirection: 'row', alignItems: 'center', paddingHorizontal: 12, paddingVertical: 8, borderRadius: 8, gap: 6 },
  toolButtonText: { fontSize: 13, fontWeight: '500' },
  aiBar: { flexDirection: 'row', alignItems: 'center', paddingHorizontal: 12, paddingVertical: 10, gap: 10, borderBottomWidth: 1 },
  aiButton: { flexDirection: 'row', alignItems: 'center', paddingHorizontal: 14, paddingVertical: 8, borderRadius: 20, gap: 8, borderWidth: 1 },
  aiButtonText: { fontSize: 14, fontWeight: '600' },
  aiBadge: { paddingHorizontal: 8, paddingVertical: 2, borderRadius: 10 },
  aiBadgeText: { color: '#FFF', fontSize: 10, fontWeight: '700' },
  analysisChip: { paddingHorizontal: 10, paddingVertical: 4, borderRadius: 12 },
  analysisChipText: { fontSize: 11, fontWeight: '700' },
  dockChip: { flexDirection: 'row', alignItems: 'center', paddingHorizontal: 10, paddingVertical: 6, borderRadius: 12, gap: 4 },
  dockChipText: { fontSize: 12, fontWeight: '600' },
  mainContent: { flex: 1 },
  editorContainer: { flex: 1 },
  editorHeader: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', paddingHorizontal: 12, paddingVertical: 8, borderBottomWidth: 1 },
  editorTab: { flexDirection: 'row', alignItems: 'center', paddingHorizontal: 12, paddingVertical: 6, borderRadius: 6, borderBottomWidth: 2 },
  fileNameInput: { fontSize: 13, fontFamily: Platform.OS === 'ios' ? 'Menlo' : 'monospace' },
  extensionText: { fontSize: 13, fontFamily: Platform.OS === 'ios' ? 'Menlo' : 'monospace' },
  execTimeText: { fontSize: 12, fontWeight: '600' },
  editorScroll: { flex: 1 },
  editorContent: { flexDirection: 'row', paddingVertical: 8 },
  lineNumbers: { paddingHorizontal: 10, paddingRight: 8, alignItems: 'flex-end', minWidth: 44 },
  lineNumber: { fontSize: 13, lineHeight: 22, fontFamily: Platform.OS === 'ios' ? 'Menlo' : 'monospace' },
  codeInput: { flex: 1, fontSize: 13, lineHeight: 22, fontFamily: Platform.OS === 'ios' ? 'Menlo' : 'monospace', paddingHorizontal: 12, textAlignVertical: 'top' },
  outputContainer: { height: SCREEN_HEIGHT * 0.28, borderTopWidth: 1 },
  outputHeader: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', paddingHorizontal: 14, paddingVertical: 10, borderBottomWidth: 1 },
  outputTitleRow: { flexDirection: 'row', alignItems: 'center', gap: 8 },
  outputTitle: { fontSize: 14, fontWeight: '600' },
  outputScroll: { flex: 1, padding: 14 },
  outputText: { fontSize: 13, fontFamily: Platform.OS === 'ios' ? 'Menlo' : 'monospace', lineHeight: 20 },
  webPreview: { flex: 1 },
  bottomBar: { paddingHorizontal: 16, paddingVertical: 12, borderTopWidth: 1 },
  runButton: { flexDirection: 'row', alignItems: 'center', justifyContent: 'center', paddingVertical: 14, borderRadius: 12, gap: 10 },
  runButtonText: { color: '#FFF', fontSize: 17, fontWeight: '700' },
  
  // Tutorial styles
  tutorialOverlay: { flex: 1, backgroundColor: 'rgba(0,0,0,0.8)', justifyContent: 'center', alignItems: 'center', padding: 20 },
  tutorialCard: { width: '100%', maxWidth: 400, borderRadius: 20, overflow: 'hidden' },
  tutorialHeader: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', padding: 16, borderBottomWidth: 1 },
  tutorialProgress: { flex: 1, marginRight: 16 },
  tutorialStep: { fontSize: 12, fontWeight: '600', marginBottom: 8 },
  progressBar: { height: 4, borderRadius: 2, overflow: 'hidden' },
  progressFill: { height: '100%', borderRadius: 2 },
  skipText: { fontSize: 14 },
  tutorialContent: { padding: 20, maxHeight: SCREEN_HEIGHT * 0.5 },
  tutorialIcon: { width: 80, height: 80, borderRadius: 40, alignItems: 'center', justifyContent: 'center', alignSelf: 'center', marginBottom: 20 },
  tutorialTitle: { fontSize: 22, fontWeight: '700', textAlign: 'center', marginBottom: 8 },
  tutorialDesc: { fontSize: 14, textAlign: 'center', marginBottom: 16 },
  tutorialContentText: { fontSize: 15, lineHeight: 24, textAlign: 'center', marginBottom: 16 },
  tutorialTips: { padding: 16, borderRadius: 12, marginTop: 8 },
  tipsTitle: { fontSize: 14, fontWeight: '600', marginBottom: 8 },
  tipText: { fontSize: 13, lineHeight: 20, marginBottom: 4 },
  celebration: { fontSize: 40, textAlign: 'center', marginTop: 16 },
  tutorialNav: { flexDirection: 'row', justifyContent: 'space-between', padding: 16, borderTopWidth: 1 },
  tutorialNavBtn: { flexDirection: 'row', alignItems: 'center', paddingHorizontal: 20, paddingVertical: 12, borderRadius: 10, gap: 8 },
  tutorialNavPrimary: { backgroundColor: '#8B5CF6' },
  tutorialNavText: { fontSize: 15, fontWeight: '500' },
  tutorialNavTextPrimary: { color: '#FFF', fontSize: 15, fontWeight: '600' },
  
  // Tooltip styles
  tooltipOverlay: { flex: 1, backgroundColor: 'rgba(0,0,0,0.5)', justifyContent: 'center', alignItems: 'center', padding: 20 },
  tooltipCard: { width: '100%', maxWidth: 340, borderRadius: 16, padding: 20 },
  tooltipHeader: { flexDirection: 'row', alignItems: 'center', gap: 12, marginBottom: 12 },
  tooltipTitle: { fontSize: 18, fontWeight: '700' },
  tooltipDesc: { fontSize: 15, lineHeight: 22, marginBottom: 12 },
  tooltipTips: { marginTop: 8 },
  tooltipTip: { fontSize: 13, lineHeight: 20, marginBottom: 4 },
  shortcutBadge: { flexDirection: 'row', alignItems: 'center', alignSelf: 'flex-start', paddingHorizontal: 12, paddingVertical: 6, borderRadius: 8, gap: 6, marginTop: 12 },
  shortcutText: { fontSize: 12, fontWeight: '600' },
  tooltipCloseBtn: { alignItems: 'center', paddingVertical: 12, borderRadius: 10, marginTop: 16 },
  tooltipCloseBtnText: { color: '#FFF', fontSize: 15, fontWeight: '600' },
  
  // Modal styles
  modalOverlay: { flex: 1, backgroundColor: 'rgba(0,0,0,0.6)', justifyContent: 'flex-end' },
  modalContent: { maxHeight: SCREEN_HEIGHT * 0.75, borderTopLeftRadius: 24, borderTopRightRadius: 24 },
  aiModalContent: { maxHeight: SCREEN_HEIGHT * 0.85 },
  analysisModalContent: { maxHeight: SCREEN_HEIGHT * 0.5 },
  dockModalContent: { maxHeight: SCREEN_HEIGHT * 0.85 },
  modalHeader: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', paddingHorizontal: 20, paddingVertical: 16, borderBottomWidth: 1 },
  modalTitle: { fontSize: 18, fontWeight: '700' },
  modalTitleRow: { flexDirection: 'row', alignItems: 'center', gap: 10 },
  
  // Language & Template items
  languageItem: { flexDirection: 'row', alignItems: 'center', paddingHorizontal: 20, paddingVertical: 14, borderBottomWidth: 1 },
  langItemIcon: { width: 44, height: 44, borderRadius: 10, alignItems: 'center', justifyContent: 'center', marginRight: 12 },
  languageItemInfo: { flex: 1 },
  languageItemName: { fontSize: 16, fontWeight: '600' },
  languageItemVersion: { fontSize: 12, marginTop: 2 },
  executableBadge: { width: 28, height: 28, borderRadius: 14, alignItems: 'center', justifyContent: 'center' },
  templateItem: { flexDirection: 'row', alignItems: 'center', paddingHorizontal: 20, paddingVertical: 14, borderBottomWidth: 1, gap: 12 },
  templateInfo: { flex: 1 },
  templateName: { fontSize: 15, fontWeight: '500' },
  templateDesc: { fontSize: 12, marginTop: 2 },
  complexityBadge: { paddingHorizontal: 10, paddingVertical: 4, borderRadius: 10 },
  complexityText: { fontSize: 10, fontWeight: '700', textTransform: 'uppercase' },
  fileItem: { flexDirection: 'row', alignItems: 'center', paddingHorizontal: 20, paddingVertical: 14, borderBottomWidth: 1, gap: 12 },
  fileItemInfo: { flex: 1 },
  fileName: { fontSize: 15, fontWeight: '500' },
  fileDate: { fontSize: 12, marginTop: 2 },
  emptyText: { textAlign: 'center', paddingVertical: 40, fontSize: 14 },
  
  // Dock styles
  dockSectionTitle: { fontSize: 12, fontWeight: '700', paddingHorizontal: 20, paddingTop: 16, paddingBottom: 8 },
  dockItem: { flexDirection: 'row', alignItems: 'center', paddingHorizontal: 20, paddingVertical: 12, borderBottomWidth: 1 },
  dockItemDisabled: { opacity: 0.6 },
  dockIcon: { width: 44, height: 44, borderRadius: 10, alignItems: 'center', justifyContent: 'center', marginRight: 12 },
  dockInfo: { flex: 1 },
  dockName: { fontSize: 15, fontWeight: '600' },
  dockDesc: { fontSize: 12, marginTop: 2 },
  statusBadge: { paddingHorizontal: 10, paddingVertical: 4, borderRadius: 10 },
  statusText: { fontSize: 10, fontWeight: '700' },
  dockGrid: { flexDirection: 'row', flexWrap: 'wrap', paddingHorizontal: 16, gap: 8, paddingVertical: 8 },
  dockGridItem: { width: (SCREEN_WIDTH - 56) / 4, alignItems: 'center', paddingVertical: 12, borderRadius: 10 },
  dockGridName: { fontSize: 10, marginTop: 4, textAlign: 'center' },
  dockFooter: { textAlign: 'center', paddingVertical: 16, fontSize: 12 },
  
  // Settings styles
  settingsContent: { paddingBottom: 20 },
  settingItem: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', paddingHorizontal: 20, paddingVertical: 16, borderBottomWidth: 1 },
  settingItemLeft: { flexDirection: 'row', alignItems: 'center', gap: 14 },
  settingIcon: { width: 40, height: 40, borderRadius: 10, alignItems: 'center', justifyContent: 'center' },
  settingItemText: { fontSize: 16 },
  settingItemValue: { fontSize: 14 },
  unlockBadge: { paddingHorizontal: 10, paddingVertical: 4, borderRadius: 10 },
  unlockBadgeText: { fontSize: 10, fontWeight: '700' },
  unlockHint: { textAlign: 'center', fontSize: 12, paddingVertical: 12 },
  
  // Advanced panel styles
  advancedContent: { padding: 20 },
  advancedWarning: { flexDirection: 'row', alignItems: 'center', padding: 12, borderRadius: 10, gap: 10, marginBottom: 20 },
  advancedWarningText: { flex: 1, fontSize: 13 },
  advancedSection: { marginBottom: 24 },
  advancedLabel: { fontSize: 14, fontWeight: '600', marginBottom: 12 },
  advancedSlider: { flexDirection: 'row', gap: 8 },
  sliderOption: { flex: 1, paddingVertical: 10, borderRadius: 8, alignItems: 'center' },
  sliderOptionWide: { flex: 1 },
  sliderText: { fontSize: 13, fontWeight: '500' },
  advancedToggle: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', paddingVertical: 16, borderBottomWidth: 1 },
  advancedToggleText: { fontSize: 15 },
  
  // AI modal styles
  aiModeGrid: { padding: 16 },
  aiModeCard: { flex: 1, margin: 6, padding: 16, borderRadius: 14, borderWidth: 1, alignItems: 'center', minHeight: 130 },
  aiModeName: { fontSize: 14, fontWeight: '600', marginTop: 10 },
  aiModeDesc: { fontSize: 11, textAlign: 'center', marginTop: 4, lineHeight: 15 },
  aiResponseContainer: { flex: 1 },
  aiBackButton: { flexDirection: 'row', alignItems: 'center', gap: 4, padding: 16 },
  aiBackText: { fontSize: 14, fontWeight: '500' },
  aiLoadingContainer: { flex: 1, justifyContent: 'center', alignItems: 'center', padding: 40 },
  aiLoadingText: { marginTop: 16, fontSize: 14 },
  aiResponseScroll: { flex: 1, padding: 16 },
  aiResponseText: { fontSize: 14, lineHeight: 22 },
  
  // Analysis styles
  analysisContent: { padding: 16 },
  analysisCard: { padding: 16, borderRadius: 12, marginBottom: 16, alignItems: 'center' },
  analysisLabel: { fontSize: 12, marginBottom: 8 },
  complexityDisplay: { paddingHorizontal: 20, paddingVertical: 8, borderRadius: 20 },
  complexityValue: { fontSize: 16, fontWeight: '700' },
  analysisGrid: { flexDirection: 'row', flexWrap: 'wrap', gap: 12 },
  analysisGridItem: { width: '47%', padding: 16, borderRadius: 12, alignItems: 'center' },
  analysisGridValue: { fontSize: 28, fontWeight: '700' },
  analysisGridLabel: { fontSize: 12, marginTop: 4 },
  
  // Form styles
  inputLabel: { fontSize: 14, fontWeight: '600', marginBottom: 8, marginTop: 16 },
  textInput: { borderWidth: 1, borderRadius: 10, paddingHorizontal: 14, paddingVertical: 12, fontSize: 15 },
  textArea: { minHeight: 80, textAlignVertical: 'top' },
  submitButton: { alignItems: 'center', justifyContent: 'center', paddingVertical: 14, borderRadius: 12, marginTop: 24, marginBottom: 20 },
  submitButtonText: { color: '#FFF', fontSize: 16, fontWeight: '700' },
});

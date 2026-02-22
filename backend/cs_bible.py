"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    THE ULTIMATE COMPUTER SCIENCE BIBLE                        ║
║                     15-Year Comprehensive Curriculum                          ║
║                                                                               ║
║  From absolute beginner to world-class computer scientist                     ║
║  150+ courses • 15 years • 10,000+ hours of content                          ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

# ============================================================================
# YEAR STRUCTURE - 15 Year Computer Science Curriculum
# ============================================================================

CURRICULUM_YEARS = {
    1: {"name": "Foundation Year", "focus": "Programming Fundamentals", "level": "beginner"},
    2: {"name": "Core Year", "focus": "Data Structures & Algorithms", "level": "beginner"},
    3: {"name": "Systems Year", "focus": "Computer Architecture & OS", "level": "intermediate"},
    4: {"name": "Theory Year", "focus": "Discrete Math & Theory of Computation", "level": "intermediate"},
    5: {"name": "Software Engineering Year", "focus": "Design Patterns & Architecture", "level": "intermediate"},
    6: {"name": "Database Year", "focus": "Data Management & Distributed Systems", "level": "intermediate"},
    7: {"name": "Networks Year", "focus": "Networking & Security", "level": "advanced"},
    8: {"name": "AI Foundations Year", "focus": "Machine Learning & AI", "level": "advanced"},
    9: {"name": "Compilers Year", "focus": "Language Implementation", "level": "advanced"},
    10: {"name": "Graphics Year", "focus": "Computer Graphics & Visualization", "level": "advanced"},
    11: {"name": "Research Year I", "focus": "Advanced Algorithms & Complexity", "level": "expert"},
    12: {"name": "Research Year II", "focus": "Distributed Computing & Systems", "level": "expert"},
    13: {"name": "Specialization Year", "focus": "Domain Expertise", "level": "master"},
    14: {"name": "Innovation Year", "focus": "Original Research", "level": "master"},
    15: {"name": "Mastery Year", "focus": "Teaching & Leadership", "level": "phd"},
}

# ============================================================================
# COMPLETE 15-YEAR CURRICULUM - 150+ COURSES
# ============================================================================

CS_BIBLE_CURRICULUM = {
    "title": "The Ultimate Computer Science Bible",
    "subtitle": "15-Year Journey from Beginner to Master",
    "total_years": 15,
    "total_courses": 150,
    "total_hours": 10000,
    "certification_levels": ["Certificate", "Associate", "Bachelor", "Master", "PhD"],
    
    "years": [
        # ====================================================================
        # YEAR 1: FOUNDATION YEAR - Programming Fundamentals
        # ====================================================================
        {
            "year": 1,
            "name": "Foundation Year",
            "theme": "Programming Fundamentals",
            "level": "beginner",
            "hours": 600,
            "courses": [
                {
                    "id": "cs101",
                    "code": "CS 101",
                    "title": "Introduction to Programming",
                    "subtitle": "Your First Lines of Code",
                    "credits": 4,
                    "hours": 60,
                    "difficulty": "beginner",
                    "prerequisites": [],
                    "description": "Learn the fundamental concepts of programming using Python. No prior experience required.",
                    "topics": [
                        "Variables and Data Types",
                        "Control Flow (if/else, loops)",
                        "Functions and Parameters",
                        "Lists and Dictionaries",
                        "File I/O",
                        "Error Handling",
                        "Basic OOP Concepts",
                        "Problem Solving Strategies"
                    ],
                    "projects": [
                        "Calculator Application",
                        "Text-based Adventure Game",
                        "Personal Budget Tracker",
                        "Simple Todo List"
                    ],
                    "languages": ["python"],
                    "content": """
# Introduction to Programming

Welcome to your journey into the world of programming! This course will teach you
how to think like a programmer and write your first programs.

## What is Programming?

Programming is the art of giving instructions to a computer. Just like you might
follow a recipe to bake a cake, computers follow programs to perform tasks.

## Your First Program

```python
# The classic first program
print("Hello, World!")

# Variables store data
name = "Student"
age = 20

# Making decisions
if age >= 18:
    print(f"{name} is an adult")
else:
    print(f"{name} is a minor")

# Loops repeat actions
for i in range(5):
    print(f"Count: {i}")

# Functions organize code
def greet(person):
    return f"Hello, {person}!"

print(greet("World"))
```

## The Programming Mindset

1. **Break problems into smaller pieces** - Decomposition
2. **Find patterns** - Abstraction
3. **Step-by-step solutions** - Algorithmic thinking
4. **Test and fix** - Debugging

## Practice Makes Perfect

Programming is a skill learned by doing. Write code every day, even if it's just
for 15 minutes. Make mistakes - they're the best teachers.
                    """
                },
                {
                    "id": "cs102",
                    "code": "CS 102",
                    "title": "Programming in C",
                    "subtitle": "Understanding the Machine",
                    "credits": 4,
                    "hours": 60,
                    "difficulty": "beginner",
                    "prerequisites": ["cs101"],
                    "description": "Learn C programming to understand how computers really work at a lower level.",
                    "topics": [
                        "C Syntax and Structure",
                        "Pointers and Memory",
                        "Arrays and Strings",
                        "Structs and Unions",
                        "Dynamic Memory Allocation",
                        "File Operations in C",
                        "Preprocessor Directives",
                        "Debugging with GDB"
                    ],
                    "projects": [
                        "Memory Allocator",
                        "String Library Implementation",
                        "Simple Shell",
                        "Binary File Reader"
                    ],
                    "languages": ["c"],
                    "content": """
# Programming in C

C is the foundation of modern computing. Understanding C gives you insight into
how computers actually work.

## Why Learn C?

- Direct memory access
- High performance
- Foundation of operating systems
- Understanding of computer architecture

## Pointers - The Heart of C

```c
#include <stdio.h>

int main() {
    int x = 42;
    int *ptr = &x;  // ptr holds address of x
    
    printf("Value: %d\\n", x);
    printf("Address: %p\\n", (void*)&x);
    printf("Via pointer: %d\\n", *ptr);
    
    // Pointer arithmetic
    int arr[] = {10, 20, 30, 40, 50};
    int *p = arr;
    
    for (int i = 0; i < 5; i++) {
        printf("arr[%d] = %d\\n", i, *(p + i));
    }
    
    return 0;
}
```

## Memory Management

```c
#include <stdlib.h>

// Dynamic allocation
int *array = malloc(10 * sizeof(int));
if (array == NULL) {
    // Handle allocation failure
}

// Use the memory
for (int i = 0; i < 10; i++) {
    array[i] = i * i;
}

// ALWAYS free when done
free(array);
```
                    """
                },
                {
                    "id": "cs103",
                    "code": "CS 103",
                    "title": "Discrete Mathematics I",
                    "subtitle": "The Language of Computer Science",
                    "credits": 4,
                    "hours": 60,
                    "difficulty": "beginner",
                    "prerequisites": [],
                    "description": "Essential mathematical foundations for computer science.",
                    "topics": [
                        "Propositional Logic",
                        "Predicate Logic",
                        "Sets and Set Operations",
                        "Relations and Functions",
                        "Proof Techniques",
                        "Mathematical Induction",
                        "Counting Principles",
                        "Basic Probability"
                    ],
                    "projects": [
                        "Logic Gate Simulator",
                        "Set Operations Calculator",
                        "Proof Verifier"
                    ],
                    "languages": [],
                    "content": """
# Discrete Mathematics I

Mathematics is the language of computer science. This course builds the
foundation you'll use throughout your career.

## Propositional Logic

```
Propositions are statements that are either TRUE or FALSE.

p: "It is raining"
q: "I have an umbrella"

Logical Operators:
¬p     - NOT p (negation)
p ∧ q  - p AND q (conjunction)
p ∨ q  - p OR q (disjunction)
p → q  - p IMPLIES q (implication)
p ↔ q  - p IFF q (biconditional)

Truth Table for AND:
p | q | p ∧ q
T | T |   T
T | F |   F
F | T |   F
F | F |   F
```

## Sets

```
A = {1, 2, 3, 4, 5}
B = {4, 5, 6, 7, 8}

A ∪ B = {1, 2, 3, 4, 5, 6, 7, 8}  (Union)
A ∩ B = {4, 5}                     (Intersection)
A - B = {1, 2, 3}                  (Difference)
A × B = {(1,4), (1,5), ...}        (Cartesian Product)
```

## Mathematical Induction

To prove P(n) for all n ≥ 1:
1. **Base Case**: Prove P(1) is true
2. **Inductive Step**: Assume P(k) is true, prove P(k+1)
                    """
                },
                {
                    "id": "cs104",
                    "code": "CS 104",
                    "title": "Computer Systems Fundamentals",
                    "subtitle": "How Computers Work",
                    "credits": 4,
                    "hours": 60,
                    "difficulty": "beginner",
                    "prerequisites": ["cs101"],
                    "description": "Understand the fundamental architecture of computer systems.",
                    "topics": [
                        "Binary Number System",
                        "Boolean Algebra",
                        "Logic Gates",
                        "CPU Architecture",
                        "Memory Hierarchy",
                        "Assembly Language Basics",
                        "Input/Output Systems",
                        "Operating System Overview"
                    ],
                    "projects": [
                        "Binary Calculator",
                        "Logic Circuit Simulator",
                        "Assembly Programs"
                    ],
                    "languages": ["assembly_x86"],
                    "content": """
# Computer Systems Fundamentals

Understanding how computers work at the hardware level is essential for
writing efficient software.

## Binary Numbers

```
Decimal  Binary   Hex
0        0000     0x0
1        0001     0x1
5        0101     0x5
10       1010     0xA
15       1111     0xF
255      11111111 0xFF

Binary Addition:
  1011  (11)
+ 0110  ( 6)
------
 10001  (17)
```

## CPU Architecture

```
┌─────────────────────────────────────┐
│              CPU                     │
│  ┌─────────┐  ┌─────────────────┐   │
│  │ Control │  │ Arithmetic      │   │
│  │  Unit   │  │ Logic Unit (ALU)│   │
│  └─────────┘  └─────────────────┘   │
│  ┌─────────────────────────────┐    │
│  │        Registers            │    │
│  │  RAX RBX RCX RDX RSI RDI   │    │
│  └─────────────────────────────┘    │
└─────────────────────────────────────┘
         ↑↓
┌─────────────────────────────────────┐
│           Memory (RAM)              │
└─────────────────────────────────────┘
```

## Assembly Language

```asm
section .text
global _start

_start:
    mov rax, 1      ; syscall: write
    mov rdi, 1      ; file descriptor: stdout
    mov rsi, msg    ; buffer
    mov rdx, 13     ; length
    syscall
    
    mov rax, 60     ; syscall: exit
    xor rdi, rdi    ; status: 0
    syscall

section .data
    msg db "Hello World!", 10
```
                    """
                },
                {
                    "id": "cs105",
                    "code": "CS 105",
                    "title": "Object-Oriented Programming",
                    "subtitle": "Modeling the World in Code",
                    "credits": 4,
                    "hours": 60,
                    "difficulty": "beginner",
                    "prerequisites": ["cs101"],
                    "description": "Master object-oriented programming concepts using Java.",
                    "topics": [
                        "Classes and Objects",
                        "Encapsulation",
                        "Inheritance",
                        "Polymorphism",
                        "Abstract Classes",
                        "Interfaces",
                        "Exception Handling",
                        "Collections Framework"
                    ],
                    "projects": [
                        "Bank Account System",
                        "Library Management",
                        "Simple Game Engine"
                    ],
                    "languages": ["java", "cpp"],
                    "content": """
# Object-Oriented Programming

OOP is a paradigm based on the concept of "objects" which contain data and code.

## The Four Pillars

### 1. Encapsulation
```java
public class BankAccount {
    private double balance;  // Hidden from outside
    
    public void deposit(double amount) {
        if (amount > 0) {
            balance += amount;
        }
    }
    
    public double getBalance() {
        return balance;
    }
}
```

### 2. Inheritance
```java
public class Animal {
    protected String name;
    
    public void speak() {
        System.out.println("...");
    }
}

public class Dog extends Animal {
    @Override
    public void speak() {
        System.out.println("Woof!");
    }
}
```

### 3. Polymorphism
```java
Animal[] animals = {new Dog(), new Cat(), new Bird()};
for (Animal a : animals) {
    a.speak();  // Each animal speaks differently
}
```

### 4. Abstraction
```java
public interface Drawable {
    void draw();
}

public abstract class Shape implements Drawable {
    abstract double area();
}
```
                    """
                },
                {
                    "id": "cs106",
                    "code": "CS 106",
                    "title": "Web Development Fundamentals",
                    "subtitle": "Building for the Browser",
                    "credits": 4,
                    "hours": 60,
                    "difficulty": "beginner",
                    "prerequisites": ["cs101"],
                    "description": "Learn to build modern web applications from scratch.",
                    "topics": [
                        "HTML5 Structure",
                        "CSS3 Styling",
                        "JavaScript Basics",
                        "DOM Manipulation",
                        "Responsive Design",
                        "HTTP Protocol",
                        "REST APIs",
                        "Version Control with Git"
                    ],
                    "projects": [
                        "Personal Portfolio",
                        "Interactive Quiz App",
                        "Weather Dashboard"
                    ],
                    "languages": ["html", "css", "javascript"],
                    "content": """
# Web Development Fundamentals

The web is the most ubiquitous platform. Learn to build for it.

## The Web Stack

```
┌─────────────────────────────────────┐
│         JavaScript (Behavior)       │
├─────────────────────────────────────┤
│         CSS (Presentation)          │
├─────────────────────────────────────┤
│         HTML (Structure)            │
└─────────────────────────────────────┘
```

## HTML - Structure
```html
<!DOCTYPE html>
<html>
<head>
    <title>My Page</title>
</head>
<body>
    <header>
        <nav>
            <a href="/">Home</a>
        </nav>
    </header>
    <main>
        <article>
            <h1>Welcome</h1>
            <p>Content here</p>
        </article>
    </main>
</body>
</html>
```

## CSS - Styling
```css
:root {
    --primary: #3498db;
}

.container {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
}

@media (max-width: 768px) {
    .container {
        flex-direction: column;
    }
}
```

## JavaScript - Behavior
```javascript
async function fetchData(url) {
    try {
        const response = await fetch(url);
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error:', error);
    }
}
```
                    """
                },
                {
                    "id": "cs107",
                    "code": "CS 107",
                    "title": "Introduction to Databases",
                    "subtitle": "Storing and Retrieving Data",
                    "credits": 4,
                    "hours": 60,
                    "difficulty": "beginner",
                    "prerequisites": ["cs101"],
                    "description": "Learn to design and query relational databases.",
                    "topics": [
                        "Database Concepts",
                        "SQL Fundamentals",
                        "Table Design",
                        "Primary and Foreign Keys",
                        "Joins and Subqueries",
                        "Indexes",
                        "Transactions",
                        "Database Normalization"
                    ],
                    "projects": [
                        "Student Records System",
                        "E-commerce Database",
                        "Social Media Schema"
                    ],
                    "languages": ["sql"],
                    "content": """
# Introduction to Databases

Databases are the backbone of modern applications. Learn to store,
organize, and retrieve data efficiently.

## SQL Basics

```sql
-- Create a table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Insert data
INSERT INTO users (username, email)
VALUES ('john_doe', 'john@example.com');

-- Query data
SELECT * FROM users WHERE created_at > '2024-01-01';

-- Update data
UPDATE users SET email = 'newemail@example.com'
WHERE username = 'john_doe';

-- Delete data
DELETE FROM users WHERE id = 1;
```

## Joins

```sql
-- Inner Join
SELECT orders.id, users.username, orders.total
FROM orders
INNER JOIN users ON orders.user_id = users.id;

-- Left Join
SELECT users.username, COUNT(orders.id) as order_count
FROM users
LEFT JOIN orders ON users.id = orders.user_id
GROUP BY users.id;
```

## Normalization

1NF: No repeating groups
2NF: No partial dependencies
3NF: No transitive dependencies
BCNF: Every determinant is a candidate key
                    """
                },
                {
                    "id": "cs108",
                    "code": "CS 108",
                    "title": "Software Development Practices",
                    "subtitle": "Professional Coding Standards",
                    "credits": 3,
                    "hours": 45,
                    "difficulty": "beginner",
                    "prerequisites": ["cs101"],
                    "description": "Learn industry-standard software development practices.",
                    "topics": [
                        "Version Control (Git)",
                        "Code Review",
                        "Testing Basics",
                        "Documentation",
                        "Agile Methodology",
                        "Clean Code Principles",
                        "Debugging Techniques",
                        "CI/CD Introduction"
                    ],
                    "projects": [
                        "Open Source Contribution",
                        "Team Project"
                    ],
                    "languages": ["python", "javascript"],
                    "content": """
# Software Development Practices

Professional software development is about more than just writing code.

## Git Workflow

```bash
# Initialize repository
git init

# Create feature branch
git checkout -b feature/new-feature

# Stage and commit
git add .
git commit -m "Add new feature"

# Push to remote
git push origin feature/new-feature

# Create pull request, review, merge
git checkout main
git pull origin main
```

## Clean Code Principles

```python
# BAD
def p(x):
    return x*x

# GOOD
def calculate_square(number: int) -> int:
    \"\"\"Calculate the square of a number.\"\"\"
    return number * number

# BAD - Magic numbers
if status == 1:
    pass

# GOOD - Named constants
STATUS_ACTIVE = 1
if status == STATUS_ACTIVE:
    pass
```

## Testing

```python
import pytest

def test_calculate_square():
    assert calculate_square(2) == 4
    assert calculate_square(0) == 0
    assert calculate_square(-3) == 9
```
                    """
                },
                {
                    "id": "cs109",
                    "code": "CS 109",
                    "title": "Linux and Command Line",
                    "subtitle": "Mastering the Terminal",
                    "credits": 3,
                    "hours": 45,
                    "difficulty": "beginner",
                    "prerequisites": [],
                    "description": "Become proficient in Linux and command-line tools.",
                    "topics": [
                        "Linux File System",
                        "Basic Commands",
                        "File Permissions",
                        "Shell Scripting",
                        "Process Management",
                        "Package Management",
                        "Text Processing (grep, sed, awk)",
                        "Remote Access (SSH)"
                    ],
                    "projects": [
                        "Backup Script",
                        "System Monitor",
                        "Log Analyzer"
                    ],
                    "languages": ["bash"],
                    "content": """
# Linux and Command Line

The command line is the most powerful tool in a developer's arsenal.

## Essential Commands

```bash
# Navigation
pwd           # Print working directory
ls -la        # List all files
cd /path      # Change directory

# File operations
cp file1 file2      # Copy
mv old new          # Move/rename
rm -rf directory    # Remove (careful!)

# Text processing
cat file            # Display file
grep "pattern" file # Search
sed 's/old/new/g'   # Replace
awk '{print $1}'    # Column extraction

# Process management
ps aux              # List processes
top                 # Monitor system
kill -9 PID         # Terminate process
```

## Shell Scripting

```bash
#!/bin/bash

# Variables
NAME="World"
echo "Hello, $NAME!"

# Functions
greet() {
    echo "Hello, $1!"
}
greet "User"

# Loops
for file in *.txt; do
    echo "Processing $file"
done

# Conditionals
if [ -f "$file" ]; then
    echo "File exists"
fi
```
                    """
                },
                {
                    "id": "cs110",
                    "code": "CS 110",
                    "title": "Functional Programming",
                    "subtitle": "A Different Way of Thinking",
                    "credits": 3,
                    "hours": 45,
                    "difficulty": "beginner",
                    "prerequisites": ["cs101"],
                    "description": "Introduction to functional programming paradigm.",
                    "topics": [
                        "Pure Functions",
                        "Immutability",
                        "Higher-Order Functions",
                        "Map, Filter, Reduce",
                        "Lambda Expressions",
                        "Recursion",
                        "Pattern Matching",
                        "Functional Composition"
                    ],
                    "projects": [
                        "Functional Data Pipeline",
                        "Parser Combinator"
                    ],
                    "languages": ["python", "haskell", "javascript"],
                    "content": """
# Functional Programming

Functional programming is a paradigm where computation is treated as
the evaluation of mathematical functions.

## Core Concepts

### Pure Functions
```python
# Pure - same input always gives same output
def add(a, b):
    return a + b

# Impure - depends on external state
total = 0
def add_to_total(x):
    global total
    total += x
    return total
```

### Higher-Order Functions
```python
# Functions that take or return functions
def apply_twice(f, x):
    return f(f(x))

def double(x):
    return x * 2

result = apply_twice(double, 5)  # 20
```

### Map, Filter, Reduce
```python
numbers = [1, 2, 3, 4, 5]

# Map - transform each element
squared = list(map(lambda x: x**2, numbers))

# Filter - keep elements matching condition
evens = list(filter(lambda x: x % 2 == 0, numbers))

# Reduce - combine all elements
from functools import reduce
total = reduce(lambda acc, x: acc + x, numbers, 0)
```

### Haskell Example
```haskell
-- List comprehension
squares = [x^2 | x <- [1..10]]

-- Pattern matching
factorial 0 = 1
factorial n = n * factorial (n - 1)

-- Higher-order functions
map (*2) [1,2,3,4,5]  -- [2,4,6,8,10]
```
                    """
                }
            ]
        },
        
        # ====================================================================
        # YEAR 2: CORE YEAR - Data Structures & Algorithms
        # ====================================================================
        {
            "year": 2,
            "name": "Core Year",
            "theme": "Data Structures & Algorithms",
            "level": "beginner",
            "hours": 650,
            "courses": [
                {
                    "id": "cs201",
                    "code": "CS 201",
                    "title": "Data Structures",
                    "subtitle": "Organizing Information Efficiently",
                    "credits": 4,
                    "hours": 60,
                    "difficulty": "intermediate",
                    "prerequisites": ["cs101", "cs102"],
                    "description": "Master fundamental data structures used in programming.",
                    "topics": [
                        "Arrays and Dynamic Arrays",
                        "Linked Lists (Singly, Doubly, Circular)",
                        "Stacks and Queues",
                        "Hash Tables",
                        "Trees (Binary, BST, AVL, Red-Black)",
                        "Heaps and Priority Queues",
                        "Graphs (Representations)",
                        "Tries and Advanced Structures"
                    ],
                    "projects": [
                        "Custom ArrayList Implementation",
                        "Hash Map from Scratch",
                        "Self-Balancing BST",
                        "Graph Library"
                    ],
                    "languages": ["java", "cpp", "python"],
                    "content": """
# Data Structures

Choosing the right data structure is crucial for efficient programs.

## Time Complexity Overview

| Structure    | Access | Search | Insert | Delete |
|-------------|--------|--------|--------|--------|
| Array       | O(1)   | O(n)   | O(n)   | O(n)   |
| Linked List | O(n)   | O(n)   | O(1)   | O(1)   |
| Hash Table  | N/A    | O(1)*  | O(1)*  | O(1)*  |
| BST         | O(log n)| O(log n)| O(log n)| O(log n)|
| Heap        | N/A    | O(n)   | O(log n)| O(log n)|

## Linked List Implementation

```python
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None
    
    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return
        
        current = self.head
        while current.next:
            current = current.next
        current.next = new_node
    
    def prepend(self, data):
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node
```

## Binary Search Tree

```python
class BSTNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None

def insert(root, key):
    if root is None:
        return BSTNode(key)
    
    if key < root.key:
        root.left = insert(root.left, key)
    else:
        root.right = insert(root.right, key)
    
    return root

def search(root, key):
    if root is None or root.key == key:
        return root
    
    if key < root.key:
        return search(root.left, key)
    return search(root.right, key)
```
                    """
                },
                {
                    "id": "cs202",
                    "code": "CS 202",
                    "title": "Algorithms I",
                    "subtitle": "Solving Problems Efficiently",
                    "credits": 4,
                    "hours": 60,
                    "difficulty": "intermediate",
                    "prerequisites": ["cs103", "cs201"],
                    "description": "Learn fundamental algorithm design and analysis.",
                    "topics": [
                        "Algorithm Analysis (Big O)",
                        "Sorting Algorithms",
                        "Searching Algorithms",
                        "Divide and Conquer",
                        "Recursion and Recurrences",
                        "Graph Traversal (BFS, DFS)",
                        "Shortest Path Algorithms",
                        "Minimum Spanning Trees"
                    ],
                    "projects": [
                        "Sorting Algorithm Visualizer",
                        "Pathfinding Visualizer",
                        "Algorithm Comparison Tool"
                    ],
                    "languages": ["python", "cpp"],
                    "content": """
# Algorithms I

An algorithm is a step-by-step procedure for solving a problem.

## Big O Notation

```
O(1)       - Constant    - Array access
O(log n)   - Logarithmic - Binary search
O(n)       - Linear      - Simple search
O(n log n) - Linearithmic - Merge sort
O(n²)      - Quadratic   - Bubble sort
O(2^n)     - Exponential - Recursive Fibonacci
O(n!)      - Factorial   - Permutations
```

## Sorting Algorithms

### Quick Sort
```python
def quicksort(arr):
    if len(arr) <= 1:
        return arr
    
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    
    return quicksort(left) + middle + quicksort(right)
```

### Merge Sort
```python
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    
    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0
    
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    result.extend(left[i:])
    result.extend(right[j:])
    return result
```

## Graph Algorithms

### BFS
```python
from collections import deque

def bfs(graph, start):
    visited = set([start])
    queue = deque([start])
    
    while queue:
        node = queue.popleft()
        print(node)
        
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
```

### Dijkstra's Algorithm
```python
import heapq

def dijkstra(graph, start):
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    pq = [(0, start)]
    
    while pq:
        curr_dist, curr_node = heapq.heappop(pq)
        
        if curr_dist > distances[curr_node]:
            continue
        
        for neighbor, weight in graph[curr_node].items():
            distance = curr_dist + weight
            
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(pq, (distance, neighbor))
    
    return distances
```
                    """
                },
                {
                    "id": "cs203",
                    "code": "CS 203",
                    "title": "Algorithms II",
                    "subtitle": "Advanced Algorithm Design",
                    "credits": 4,
                    "hours": 60,
                    "difficulty": "intermediate",
                    "prerequisites": ["cs202"],
                    "description": "Advanced algorithm design techniques and analysis.",
                    "topics": [
                        "Dynamic Programming",
                        "Greedy Algorithms",
                        "Backtracking",
                        "Branch and Bound",
                        "String Algorithms",
                        "Network Flow",
                        "NP-Completeness",
                        "Approximation Algorithms"
                    ],
                    "projects": [
                        "Dynamic Programming Solver",
                        "Scheduling Optimizer",
                        "String Matching Engine"
                    ],
                    "languages": ["cpp", "python"],
                    "content": """
# Algorithms II

Advanced techniques for solving complex computational problems.

## Dynamic Programming

DP solves problems by breaking them into overlapping subproblems.

### Fibonacci with DP
```python
# Top-down (Memoization)
def fib_memo(n, memo={}):
    if n in memo:
        return memo[n]
    if n <= 1:
        return n
    memo[n] = fib_memo(n-1, memo) + fib_memo(n-2, memo)
    return memo[n]

# Bottom-up (Tabulation)
def fib_tab(n):
    if n <= 1:
        return n
    dp = [0] * (n + 1)
    dp[1] = 1
    for i in range(2, n + 1):
        dp[i] = dp[i-1] + dp[i-2]
    return dp[n]
```

### Longest Common Subsequence
```python
def lcs(X, Y):
    m, n = len(X), len(Y)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if X[i-1] == Y[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    
    return dp[m][n]
```

### 0/1 Knapsack
```python
def knapsack(W, weights, values, n):
    dp = [[0] * (W + 1) for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        for w in range(W + 1):
            if weights[i-1] <= w:
                dp[i][w] = max(
                    dp[i-1][w],
                    values[i-1] + dp[i-1][w - weights[i-1]]
                )
            else:
                dp[i][w] = dp[i-1][w]
    
    return dp[n][W]
```

## NP-Completeness

Problems classified by computational complexity:
- **P**: Solvable in polynomial time
- **NP**: Verifiable in polynomial time
- **NP-Complete**: Hardest problems in NP
- **NP-Hard**: At least as hard as NP-Complete

Examples of NP-Complete problems:
- Traveling Salesman Problem
- Boolean Satisfiability (SAT)
- Graph Coloring
- Subset Sum
                    """
                },
                {
                    "id": "cs204",
                    "code": "CS 204",
                    "title": "Discrete Mathematics II",
                    "subtitle": "Advanced Mathematical Foundations",
                    "credits": 4,
                    "hours": 60,
                    "difficulty": "intermediate",
                    "prerequisites": ["cs103"],
                    "description": "Advanced discrete mathematics for computer science.",
                    "topics": [
                        "Graph Theory",
                        "Combinatorics",
                        "Recurrence Relations",
                        "Generating Functions",
                        "Number Theory",
                        "Modular Arithmetic",
                        "Cryptographic Basics",
                        "Probability Theory"
                    ],
                    "projects": [
                        "Graph Algorithm Proofs",
                        "Cryptographic Implementation"
                    ],
                    "languages": [],
                    "content": """
# Discrete Mathematics II

Advanced mathematical tools for algorithm analysis and design.

## Graph Theory

### Definitions
- **Graph G = (V, E)**: Vertices and Edges
- **Degree**: Number of edges incident to a vertex
- **Path**: Sequence of vertices connected by edges
- **Cycle**: Path that starts and ends at same vertex
- **Connected**: Path exists between any two vertices

### Euler's Formula (Planar Graphs)
```
V - E + F = 2

Where:
V = number of vertices
E = number of edges
F = number of faces (including outer face)
```

### Graph Coloring
Chromatic number χ(G) = minimum colors needed
- Trees: χ = 2
- Bipartite: χ = 2
- Planar: χ ≤ 4 (Four Color Theorem)

## Number Theory

### Modular Arithmetic
```
(a + b) mod n = ((a mod n) + (b mod n)) mod n
(a * b) mod n = ((a mod n) * (b mod n)) mod n
```

### Euclidean Algorithm (GCD)
```python
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a
```

### Extended Euclidean Algorithm
```python
def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y
```

## Recurrence Relations

### Master Theorem
For T(n) = aT(n/b) + f(n):

1. If f(n) = O(n^(log_b(a) - ε)), then T(n) = Θ(n^log_b(a))
2. If f(n) = Θ(n^log_b(a)), then T(n) = Θ(n^log_b(a) * log n)
3. If f(n) = Ω(n^(log_b(a) + ε)), then T(n) = Θ(f(n))
                    """
                },
                {
                    "id": "cs205",
                    "code": "CS 205",
                    "title": "Programming Languages",
                    "subtitle": "Understanding Language Design",
                    "credits": 4,
                    "hours": 60,
                    "difficulty": "intermediate",
                    "prerequisites": ["cs101", "cs105"],
                    "description": "Survey of programming language paradigms and concepts.",
                    "topics": [
                        "Language Paradigms Overview",
                        "Type Systems",
                        "Memory Management",
                        "Scope and Binding",
                        "Control Abstractions",
                        "Concurrency Models",
                        "Domain-Specific Languages",
                        "Language Implementation"
                    ],
                    "projects": [
                        "Mini-Language Interpreter",
                        "Type Checker"
                    ],
                    "languages": ["python", "haskell", "rust", "lisp"],
                    "content": """
# Programming Languages

Understanding language design helps you choose and use languages effectively.

## Paradigms

### Imperative
```c
int sum = 0;
for (int i = 0; i < n; i++) {
    sum += array[i];
}
```

### Functional
```haskell
sum = foldl (+) 0
```

### Object-Oriented
```java
list.stream()
    .map(x -> x * 2)
    .filter(x -> x > 10)
    .forEach(System.out::println);
```

### Logic
```prolog
parent(tom, mary).
parent(tom, john).
grandparent(X, Z) :- parent(X, Y), parent(Y, Z).
```

## Type Systems

### Static vs Dynamic
```python
# Dynamic (Python)
x = 5        # x is int
x = "hello"  # now x is str
```

```rust
// Static (Rust)
let x: i32 = 5;
// x = "hello";  // Compile error!
```

### Strong vs Weak
```javascript
// Weak (JavaScript)
"5" + 3  // "53" (string concatenation)
"5" - 3  // 2 (numeric subtraction)
```

```python
# Strong (Python)
"5" + 3  # TypeError!
```

## Memory Management

1. **Manual** (C): malloc/free
2. **Reference Counting** (Python, Swift)
3. **Garbage Collection** (Java, Go)
4. **Ownership** (Rust): Compile-time safety
                    """
                },
                {
                    "id": "cs206",
                    "code": "CS 206",
                    "title": "Computer Architecture",
                    "subtitle": "Inside the Machine",
                    "credits": 4,
                    "hours": 60,
                    "difficulty": "intermediate",
                    "prerequisites": ["cs104"],
                    "description": "Deep dive into computer architecture and organization.",
                    "topics": [
                        "Instruction Set Architecture",
                        "CPU Design",
                        "Pipelining",
                        "Cache Memory",
                        "Virtual Memory",
                        "I/O Systems",
                        "Parallel Architecture",
                        "Performance Optimization"
                    ],
                    "projects": [
                        "CPU Simulator",
                        "Cache Simulator"
                    ],
                    "languages": ["assembly_x86", "verilog"],
                    "content": """
# Computer Architecture

Understanding hardware helps you write efficient software.

## CPU Pipeline

```
┌─────────┬─────────┬─────────┬─────────┬─────────┐
│  Fetch  │ Decode  │ Execute │ Memory  │  Write  │
│  (IF)   │  (ID)   │  (EX)   │  (MEM)  │  (WB)   │
└─────────┴─────────┴─────────┴─────────┴─────────┘

Clock 1: I1-IF
Clock 2: I1-ID   I2-IF
Clock 3: I1-EX   I2-ID   I3-IF
Clock 4: I1-MEM  I2-EX   I3-ID   I4-IF
Clock 5: I1-WB   I2-MEM  I3-EX   I4-ID   I5-IF
```

## Memory Hierarchy

```
┌─────────────┐  ← Registers (1 cycle)
│             │
├─────────────┤
│  L1 Cache   │  ← 4 cycles
├─────────────┤
│  L2 Cache   │  ← 12 cycles
├─────────────┤
│  L3 Cache   │  ← 40 cycles
├─────────────┤
│    RAM      │  ← 100 cycles
├─────────────┤
│    SSD      │  ← 10,000+ cycles
├─────────────┤
│    HDD      │  ← 10,000,000+ cycles
└─────────────┘
```

## Cache Performance

```
Cache Hit Rate = Hits / (Hits + Misses)

Average Memory Access Time =
    Hit Time + (Miss Rate × Miss Penalty)

Example:
- L1 Hit Time: 1 cycle
- L1 Miss Rate: 5%
- L2 Hit Time: 10 cycles
- L2 Miss Rate: 2%
- Memory Access: 100 cycles

AMAT = 1 + 0.05 × (10 + 0.02 × 100)
     = 1 + 0.05 × 12
     = 1.6 cycles
```
                    """
                },
                {
                    "id": "cs207",
                    "code": "CS 207",
                    "title": "Software Testing",
                    "subtitle": "Building Reliable Software",
                    "credits": 3,
                    "hours": 45,
                    "difficulty": "intermediate",
                    "prerequisites": ["cs105", "cs108"],
                    "description": "Comprehensive software testing methodologies.",
                    "topics": [
                        "Testing Fundamentals",
                        "Unit Testing",
                        "Integration Testing",
                        "System Testing",
                        "Test-Driven Development",
                        "Code Coverage",
                        "Mutation Testing",
                        "Performance Testing"
                    ],
                    "projects": [
                        "Test Suite Development",
                        "CI/CD Pipeline Setup"
                    ],
                    "languages": ["python", "javascript"],
                    "content": """
# Software Testing

Testing is essential for building reliable software.

## Testing Pyramid

```
        /\\
       /  \\
      / E2E\\     <- Few, slow, expensive
     /──────\\
    /  Integ \\   <- Medium
   /──────────\\
  /    Unit    \\ <- Many, fast, cheap
 /──────────────\\
```

## Test-Driven Development

```
1. RED:   Write a failing test
2. GREEN: Write minimum code to pass
3. REFACTOR: Improve the code

def test_add():
    assert add(2, 3) == 5  # RED: No add function

def add(a, b):
    return a + b  # GREEN: Test passes

# REFACTOR if needed
```

## Coverage Metrics

```python
# Statement Coverage
if condition:
    line_a()  # Covered if condition is True
else:
    line_b()  # Covered if condition is False

# Branch Coverage
if a and b:  # Need: (T,T), (T,F), (F,*)
    do_something()

# Path Coverage
if a:
    x()
if b:
    y()
# Paths: x-y, x-!y, !x-y, !x-!y
```

## pytest Example

```python
import pytest

class TestCalculator:
    def test_add(self):
        assert Calculator.add(1, 2) == 3
    
    def test_divide(self):
        assert Calculator.divide(10, 2) == 5
    
    def test_divide_by_zero(self):
        with pytest.raises(ZeroDivisionError):
            Calculator.divide(10, 0)
    
    @pytest.mark.parametrize("a,b,expected", [
        (1, 2, 3),
        (0, 0, 0),
        (-1, 1, 0),
    ])
    def test_add_parametrized(self, a, b, expected):
        assert Calculator.add(a, b) == expected
```
                    """
                },
                {
                    "id": "cs208",
                    "code": "CS 208",
                    "title": "Advanced Python",
                    "subtitle": "Python Mastery",
                    "credits": 3,
                    "hours": 45,
                    "difficulty": "intermediate",
                    "prerequisites": ["cs101"],
                    "description": "Advanced Python programming techniques.",
                    "topics": [
                        "Decorators",
                        "Generators and Iterators",
                        "Context Managers",
                        "Metaclasses",
                        "Async/Await",
                        "Type Hints",
                        "Performance Optimization",
                        "C Extensions"
                    ],
                    "projects": [
                        "Web Framework",
                        "Async HTTP Client"
                    ],
                    "languages": ["python"],
                    "content": """
# Advanced Python

Unlock the full power of Python.

## Decorators

```python
def timer(func):
    import time
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print(f"{func.__name__} took {time.time()-start:.4f}s")
        return result
    return wrapper

@timer
def slow_function():
    time.sleep(1)
```

## Generators

```python
def fibonacci():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

fib = fibonacci()
for _ in range(10):
    print(next(fib))
```

## Context Managers

```python
class DatabaseConnection:
    def __enter__(self):
        self.conn = connect_to_db()
        return self.conn
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()

with DatabaseConnection() as conn:
    conn.execute("SELECT * FROM users")
```

## Async/Await

```python
import asyncio

async def fetch_data(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()

async def main():
    urls = ['url1', 'url2', 'url3']
    tasks = [fetch_data(url) for url in urls]
    results = await asyncio.gather(*tasks)
    return results
```
                    """
                },
                {
                    "id": "cs209",
                    "code": "CS 209",
                    "title": "Advanced JavaScript",
                    "subtitle": "JavaScript Deep Dive",
                    "credits": 3,
                    "hours": 45,
                    "difficulty": "intermediate",
                    "prerequisites": ["cs106"],
                    "description": "Advanced JavaScript programming techniques.",
                    "topics": [
                        "Closures and Scope",
                        "Prototypes and Classes",
                        "Promises and Async/Await",
                        "Event Loop",
                        "Modules (ESM, CommonJS)",
                        "Web APIs",
                        "Performance Optimization",
                        "TypeScript Introduction"
                    ],
                    "projects": [
                        "Promise Library",
                        "Event Emitter"
                    ],
                    "languages": ["javascript", "typescript"],
                    "content": """
# Advanced JavaScript

Master the quirks and power of JavaScript.

## Event Loop

```
┌─────────────────────────────────────────┐
│              Call Stack                  │
│    ┌─────────────────────────────┐      │
│    │    Function Execution       │      │
│    └─────────────────────────────┘      │
└─────────────────────────────────────────┘
           ↑                    ↓
┌──────────┴────────────────────┴─────────┐
│        Web APIs / Node APIs             │
│  setTimeout, fetch, DOM events          │
└─────────────────────────────────────────┘
           ↓
┌─────────────────────────────────────────┐
│          Task Queues                     │
│  ┌─────────────────────────────────┐    │
│  │ Microtask Queue (Promises)      │    │
│  └─────────────────────────────────┘    │
│  ┌─────────────────────────────────┐    │
│  │ Macrotask Queue (setTimeout)    │    │
│  └─────────────────────────────────┘    │
└─────────────────────────────────────────┘
```

## Closures

```javascript
function createCounter() {
    let count = 0;  // Enclosed variable
    
    return {
        increment: () => ++count,
        decrement: () => --count,
        getCount: () => count
    };
}

const counter = createCounter();
counter.increment();  // 1
counter.increment();  // 2
```

## Promises

```javascript
const myPromise = new Promise((resolve, reject) => {
    setTimeout(() => {
        resolve('Success!');
    }, 1000);
});

// Chaining
myPromise
    .then(result => console.log(result))
    .catch(error => console.error(error))
    .finally(() => console.log('Done'));

// Async/Await
async function getData() {
    try {
        const result = await myPromise;
        return result;
    } catch (error) {
        console.error(error);
    }
}
```
                    """
                },
                {
                    "id": "cs210",
                    "code": "CS 210",
                    "title": "Competitive Programming",
                    "subtitle": "Problem Solving Mastery",
                    "credits": 3,
                    "hours": 45,
                    "difficulty": "intermediate",
                    "prerequisites": ["cs202", "cs203"],
                    "description": "Prepare for programming competitions and technical interviews.",
                    "topics": [
                        "Problem Analysis",
                        "Time/Space Optimization",
                        "Common Patterns",
                        "Segment Trees",
                        "Fenwick Trees",
                        "Union-Find",
                        "Number Theory Applications",
                        "Geometry Algorithms"
                    ],
                    "projects": [
                        "Contest Participation",
                        "Problem Archive"
                    ],
                    "languages": ["cpp", "python"],
                    "content": """
# Competitive Programming

Sharpen your problem-solving skills.

## Essential Data Structures

### Segment Tree
```cpp
class SegmentTree {
    vector<int> tree;
    int n;
    
public:
    SegmentTree(vector<int>& arr) {
        n = arr.size();
        tree.resize(4 * n);
        build(arr, 0, 0, n - 1);
    }
    
    void build(vector<int>& arr, int node, int start, int end) {
        if (start == end) {
            tree[node] = arr[start];
        } else {
            int mid = (start + end) / 2;
            build(arr, 2*node+1, start, mid);
            build(arr, 2*node+2, mid+1, end);
            tree[node] = tree[2*node+1] + tree[2*node+2];
        }
    }
    
    int query(int node, int start, int end, int l, int r) {
        if (r < start || end < l) return 0;
        if (l <= start && end <= r) return tree[node];
        int mid = (start + end) / 2;
        return query(2*node+1, start, mid, l, r) +
               query(2*node+2, mid+1, end, l, r);
    }
};
```

### Union-Find
```cpp
class UnionFind {
    vector<int> parent, rank;
    
public:
    UnionFind(int n) : parent(n), rank(n, 0) {
        iota(parent.begin(), parent.end(), 0);
    }
    
    int find(int x) {
        if (parent[x] != x)
            parent[x] = find(parent[x]);
        return parent[x];
    }
    
    void unite(int x, int y) {
        int px = find(x), py = find(y);
        if (px == py) return;
        if (rank[px] < rank[py]) swap(px, py);
        parent[py] = px;
        if (rank[px] == rank[py]) rank[px]++;
    }
};
```
                    """
                }
            ]
        },
        
        # ====================================================================
        # YEAR 3-15: Abbreviated for space - Full courses defined
        # ====================================================================
        {
            "year": 3,
            "name": "Systems Year",
            "theme": "Computer Architecture & Operating Systems",
            "level": "intermediate",
            "hours": 650,
            "courses": [
                {"id": "cs301", "code": "CS 301", "title": "Operating Systems", "subtitle": "The Heart of Computing", "credits": 4, "hours": 60, "difficulty": "intermediate", "prerequisites": ["cs102", "cs206"], "topics": ["Process Management", "Memory Management", "File Systems", "Concurrency", "Scheduling", "Virtual Memory", "Device Drivers", "System Calls"], "languages": ["c", "rust"]},
                {"id": "cs302", "code": "CS 302", "title": "Computer Networks", "subtitle": "Connecting the World", "credits": 4, "hours": 60, "difficulty": "intermediate", "prerequisites": ["cs104"], "topics": ["OSI Model", "TCP/IP", "Routing", "DNS", "HTTP/HTTPS", "Sockets", "Network Security", "Wireless Networks"], "languages": ["python", "c"]},
                {"id": "cs303", "code": "CS 303", "title": "Systems Programming", "subtitle": "Low-Level Mastery", "credits": 4, "hours": 60, "difficulty": "intermediate", "prerequisites": ["cs102", "cs301"], "topics": ["POSIX APIs", "Process Creation", "Signals", "IPC", "Threading", "Memory Mapping", "Shared Memory", "Semaphores"], "languages": ["c"]},
                {"id": "cs304", "code": "CS 304", "title": "Embedded Systems", "subtitle": "Programming Hardware", "credits": 4, "hours": 60, "difficulty": "intermediate", "prerequisites": ["cs102", "cs206"], "topics": ["Microcontrollers", "Real-Time Systems", "Interrupts", "Timers", "Serial Communication", "Sensors", "Actuators", "RTOS"], "languages": ["c", "assembly_arm"]},
                {"id": "cs305", "code": "CS 305", "title": "Database Systems", "subtitle": "Data Management at Scale", "credits": 4, "hours": 60, "difficulty": "intermediate", "prerequisites": ["cs107", "cs201"], "topics": ["Query Processing", "Transaction Management", "Recovery", "Indexing", "Query Optimization", "Distributed Databases", "NoSQL", "NewSQL"], "languages": ["sql"]},
                {"id": "cs306", "code": "CS 306", "title": "Compiler Design I", "subtitle": "Language Implementation Basics", "credits": 4, "hours": 60, "difficulty": "intermediate", "prerequisites": ["cs201", "cs205"], "topics": ["Lexical Analysis", "Parsing", "Semantic Analysis", "Type Checking", "Symbol Tables", "Intermediate Representation", "Basic Optimization", "Code Generation"], "languages": ["python", "cpp"]},
                {"id": "cs307", "code": "CS 307", "title": "Computer Security", "subtitle": "Defending Digital Systems", "credits": 4, "hours": 60, "difficulty": "intermediate", "prerequisites": ["cs301", "cs302"], "topics": ["Cryptography", "Authentication", "Access Control", "Buffer Overflows", "Web Security", "Network Security", "Malware", "Penetration Testing"], "languages": ["python", "c"]},
                {"id": "cs308", "code": "CS 308", "title": "Parallel Computing", "subtitle": "Harnessing Multiple Cores", "credits": 4, "hours": 60, "difficulty": "intermediate", "prerequisites": ["cs206", "cs303"], "topics": ["Parallel Architectures", "Shared Memory", "Message Passing", "OpenMP", "MPI", "GPU Programming", "CUDA", "Load Balancing"], "languages": ["cpp", "cuda"]},
                {"id": "cs309", "code": "CS 309", "title": "Cloud Computing", "subtitle": "Computing as a Service", "credits": 3, "hours": 45, "difficulty": "intermediate", "prerequisites": ["cs301", "cs302"], "topics": ["Virtualization", "Containers", "Kubernetes", "Serverless", "Cloud Storage", "Load Balancing", "Auto-scaling", "Cloud Security"], "languages": ["python", "yaml"]},
                {"id": "cs310", "code": "CS 310", "title": "DevOps Engineering", "subtitle": "Bridging Dev and Ops", "credits": 3, "hours": 45, "difficulty": "intermediate", "prerequisites": ["cs108", "cs309"], "topics": ["CI/CD", "Infrastructure as Code", "Monitoring", "Logging", "Containerization", "Orchestration", "Site Reliability", "Incident Management"], "languages": ["bash", "python", "yaml"]}
            ]
        },
        {
            "year": 4,
            "name": "Theory Year",
            "theme": "Discrete Math & Theory of Computation",
            "level": "intermediate",
            "hours": 650,
            "courses": [
                {"id": "cs401", "code": "CS 401", "title": "Theory of Computation", "subtitle": "The Limits of Computing", "credits": 4, "hours": 60, "difficulty": "advanced", "prerequisites": ["cs103", "cs204"], "topics": ["Finite Automata", "Regular Languages", "Context-Free Grammars", "Pushdown Automata", "Turing Machines", "Decidability", "Complexity Classes", "Reductions"], "languages": []},
                {"id": "cs402", "code": "CS 402", "title": "Formal Languages", "subtitle": "Mathematical Language Theory", "credits": 4, "hours": 60, "difficulty": "advanced", "prerequisites": ["cs401"], "topics": ["Regular Expressions", "Chomsky Hierarchy", "Pumping Lemmas", "Closure Properties", "Parsing Theory", "Ambiguity", "Normal Forms", "Language Transformations"], "languages": []},
                {"id": "cs403", "code": "CS 403", "title": "Computational Complexity", "subtitle": "Understanding Hardness", "credits": 4, "hours": 60, "difficulty": "advanced", "prerequisites": ["cs401"], "topics": ["P vs NP", "NP-Completeness", "Reductions", "Space Complexity", "Randomized Complexity", "Interactive Proofs", "Approximation Algorithms", "Parameterized Complexity"], "languages": []},
                {"id": "cs404", "code": "CS 404", "title": "Cryptography", "subtitle": "The Science of Secrets", "credits": 4, "hours": 60, "difficulty": "advanced", "prerequisites": ["cs204", "cs307"], "topics": ["Symmetric Encryption", "Public Key Cryptography", "Hash Functions", "Digital Signatures", "Zero-Knowledge Proofs", "Homomorphic Encryption", "Secure Multiparty Computation", "Blockchain Cryptography"], "languages": ["python"]},
                {"id": "cs405", "code": "CS 405", "title": "Information Theory", "subtitle": "Quantifying Information", "credits": 4, "hours": 60, "difficulty": "advanced", "prerequisites": ["cs204"], "topics": ["Entropy", "Mutual Information", "Channel Capacity", "Source Coding", "Error-Correcting Codes", "Data Compression", "Rate-Distortion Theory", "Network Information Theory"], "languages": ["python"]},
                {"id": "cs406", "code": "CS 406", "title": "Logic and Verification", "subtitle": "Proving Programs Correct", "credits": 4, "hours": 60, "difficulty": "advanced", "prerequisites": ["cs103", "cs401"], "topics": ["Propositional Logic", "First-Order Logic", "Temporal Logic", "Model Checking", "Theorem Proving", "SAT Solvers", "SMT Solvers", "Program Verification"], "languages": ["coq", "lean"]},
                {"id": "cs407", "code": "CS 407", "title": "Category Theory for CS", "subtitle": "Abstract Mathematics", "credits": 3, "hours": 45, "difficulty": "advanced", "prerequisites": ["cs204", "cs110"], "topics": ["Categories and Functors", "Natural Transformations", "Adjunctions", "Monads", "Algebraic Data Types", "Type Theory", "Dependent Types", "Homotopy Type Theory"], "languages": ["haskell"]},
                {"id": "cs408", "code": "CS 408", "title": "Quantum Computing", "subtitle": "Computing with Qubits", "credits": 4, "hours": 60, "difficulty": "advanced", "prerequisites": ["cs401"], "topics": ["Qubits", "Quantum Gates", "Entanglement", "Quantum Algorithms", "Shor's Algorithm", "Grover's Algorithm", "Quantum Error Correction", "Quantum Supremacy"], "languages": ["python"]},
                {"id": "cs409", "code": "CS 409", "title": "Randomized Algorithms", "subtitle": "Power of Randomness", "credits": 3, "hours": 45, "difficulty": "advanced", "prerequisites": ["cs203", "cs204"], "topics": ["Probabilistic Analysis", "Las Vegas Algorithms", "Monte Carlo Algorithms", "Random Sampling", "Hashing", "Skip Lists", "Randomized Graphs", "Derandomization"], "languages": ["python"]},
                {"id": "cs410", "code": "CS 410", "title": "Approximation Algorithms", "subtitle": "Near-Optimal Solutions", "credits": 3, "hours": 45, "difficulty": "advanced", "prerequisites": ["cs203", "cs403"], "topics": ["Approximation Ratios", "Greedy Approximations", "LP Relaxation", "Rounding", "Primal-Dual", "Local Search", "PTAS/FPTAS", "Inapproximability"], "languages": ["python"]}
            ]
        },
        {
            "year": 5,
            "name": "Software Engineering Year",
            "theme": "Design Patterns & Architecture",
            "level": "intermediate",
            "hours": 650,
            "courses": [
                {"id": "cs501", "code": "CS 501", "title": "Software Architecture", "subtitle": "Designing Large Systems", "credits": 4, "hours": 60, "difficulty": "intermediate", "prerequisites": ["cs105", "cs108"], "topics": ["Architectural Patterns", "Microservices", "Event-Driven Architecture", "CQRS", "Domain-Driven Design", "API Design", "Scalability", "Resilience"], "languages": ["java", "python"]},
                {"id": "cs502", "code": "CS 502", "title": "Design Patterns", "subtitle": "Reusable Solutions", "credits": 4, "hours": 60, "difficulty": "intermediate", "prerequisites": ["cs105"], "topics": ["Creational Patterns", "Structural Patterns", "Behavioral Patterns", "SOLID Principles", "Refactoring", "Anti-Patterns", "Pattern Languages", "Gang of Four"], "languages": ["java", "typescript"]},
                {"id": "cs503", "code": "CS 503", "title": "Distributed Systems", "subtitle": "Systems at Scale", "credits": 4, "hours": 60, "difficulty": "advanced", "prerequisites": ["cs301", "cs302", "cs305"], "topics": ["Consensus Protocols", "Replication", "Consistency Models", "Distributed Transactions", "Fault Tolerance", "CAP Theorem", "MapReduce", "Stream Processing"], "languages": ["java", "go"]},
                {"id": "cs504", "code": "CS 504", "title": "Mobile Development", "subtitle": "Apps for Everyone", "credits": 4, "hours": 60, "difficulty": "intermediate", "prerequisites": ["cs105", "cs106"], "topics": ["iOS Development", "Android Development", "Cross-Platform", "Mobile UI/UX", "Local Storage", "Push Notifications", "Location Services", "Mobile Security"], "languages": ["swift", "kotlin", "dart"]},
                {"id": "cs505", "code": "CS 505", "title": "Full-Stack Development", "subtitle": "End-to-End Apps", "credits": 4, "hours": 60, "difficulty": "intermediate", "prerequisites": ["cs106", "cs107"], "topics": ["Frontend Frameworks", "Backend Frameworks", "REST/GraphQL", "Authentication", "State Management", "Real-time Features", "Deployment", "Performance"], "languages": ["typescript", "python", "go"]},
                {"id": "cs506", "code": "CS 506", "title": "Game Development", "subtitle": "Creating Interactive Experiences", "credits": 4, "hours": 60, "difficulty": "intermediate", "prerequisites": ["cs105", "cs201"], "topics": ["Game Loops", "Physics Engines", "Graphics Programming", "AI in Games", "Networking", "Audio", "Level Design", "Game Engines"], "languages": ["cpp", "csharp"]},
                {"id": "cs507", "code": "CS 507", "title": "API Design & Development", "subtitle": "Building Interfaces", "credits": 3, "hours": 45, "difficulty": "intermediate", "prerequisites": ["cs106", "cs501"], "topics": ["REST Principles", "GraphQL", "gRPC", "API Versioning", "Documentation", "Rate Limiting", "Caching", "Security"], "languages": ["python", "go"]},
                {"id": "cs508", "code": "CS 508", "title": "Software Project Management", "subtitle": "Leading Technical Teams", "credits": 3, "hours": 45, "difficulty": "intermediate", "prerequisites": ["cs108"], "topics": ["Agile/Scrum", "Kanban", "Sprint Planning", "Estimation", "Risk Management", "Technical Debt", "Code Reviews", "Team Dynamics"], "languages": []},
                {"id": "cs509", "code": "CS 509", "title": "User Experience Design", "subtitle": "Human-Centered Design", "credits": 3, "hours": 45, "difficulty": "intermediate", "prerequisites": ["cs106"], "topics": ["User Research", "Personas", "Wireframing", "Prototyping", "Usability Testing", "Accessibility", "Design Systems", "Interaction Design"], "languages": []},
                {"id": "cs510", "code": "CS 510", "title": "Tech Entrepreneurship", "subtitle": "Building Startups", "credits": 3, "hours": 45, "difficulty": "intermediate", "prerequisites": ["cs108"], "topics": ["Idea Validation", "MVPs", "Funding", "Team Building", "Product-Market Fit", "Growth", "Legal Basics", "Exit Strategies"], "languages": []}
            ]
        },
        {
            "year": 6,
            "name": "Database Year",
            "theme": "Data Management & Distributed Systems",
            "level": "intermediate",
            "hours": 650,
            "courses": [
                {"id": "cs601", "code": "CS 601", "title": "Advanced Database Systems", "subtitle": "Beyond SQL", "credits": 4, "hours": 60, "difficulty": "advanced", "prerequisites": ["cs305"], "topics": ["Query Optimization", "Storage Engines", "Concurrency Control", "Recovery Algorithms", "Distributed Databases", "Sharding", "Replication", "Consistency"], "languages": ["sql", "cpp"]},
                {"id": "cs602", "code": "CS 602", "title": "Data Warehousing", "subtitle": "Analytics at Scale", "credits": 4, "hours": 60, "difficulty": "advanced", "prerequisites": ["cs305"], "topics": ["Star Schema", "OLAP", "ETL", "Data Lakes", "Columnar Storage", "Dimensional Modeling", "Data Quality", "BI Tools"], "languages": ["sql", "python"]},
                {"id": "cs603", "code": "CS 603", "title": "NoSQL Databases", "subtitle": "Alternative Data Models", "credits": 4, "hours": 60, "difficulty": "advanced", "prerequisites": ["cs305", "cs503"], "topics": ["Document Stores", "Key-Value Stores", "Column Families", "Graph Databases", "Time Series", "Multi-Model", "CAP Tradeoffs", "Data Modeling"], "languages": ["python", "javascript"]},
                {"id": "cs604", "code": "CS 604", "title": "Big Data Systems", "subtitle": "Processing Massive Data", "credits": 4, "hours": 60, "difficulty": "advanced", "prerequisites": ["cs503", "cs601"], "topics": ["Hadoop", "Spark", "Flink", "Kafka", "Data Pipelines", "Stream Processing", "Batch Processing", "Data Governance"], "languages": ["scala", "python"]},
                {"id": "cs605", "code": "CS 605", "title": "Information Retrieval", "subtitle": "Search Systems", "credits": 4, "hours": 60, "difficulty": "advanced", "prerequisites": ["cs201", "cs305"], "topics": ["Text Processing", "Indexing", "Ranking", "Relevance", "Semantic Search", "Recommendation Systems", "NLP for IR", "Evaluation"], "languages": ["python"]},
                {"id": "cs606", "code": "CS 606", "title": "Data Mining", "subtitle": "Discovering Patterns", "credits": 4, "hours": 60, "difficulty": "advanced", "prerequisites": ["cs202", "cs305"], "topics": ["Classification", "Clustering", "Association Rules", "Anomaly Detection", "Feature Engineering", "Dimensionality Reduction", "Ensemble Methods", "Deep Learning for Mining"], "languages": ["python"]},
                {"id": "cs607", "code": "CS 607", "title": "Blockchain Technology", "subtitle": "Decentralized Systems", "credits": 4, "hours": 60, "difficulty": "advanced", "prerequisites": ["cs404", "cs503"], "topics": ["Consensus Mechanisms", "Smart Contracts", "DeFi", "NFTs", "Layer 2 Solutions", "Interoperability", "Privacy", "Governance"], "languages": ["solidity", "rust"]},
                {"id": "cs608", "code": "CS 608", "title": "Data Engineering", "subtitle": "Building Data Infrastructure", "credits": 3, "hours": 45, "difficulty": "advanced", "prerequisites": ["cs604"], "topics": ["Pipeline Architecture", "Orchestration", "Data Quality", "Monitoring", "Testing", "Documentation", "Cost Optimization", "Team Practices"], "languages": ["python", "sql"]},
                {"id": "cs609", "code": "CS 609", "title": "Privacy-Preserving Computing", "subtitle": "Secure Data Processing", "credits": 3, "hours": 45, "difficulty": "advanced", "prerequisites": ["cs404", "cs601"], "topics": ["Differential Privacy", "Federated Learning", "Secure Enclaves", "Multi-Party Computation", "Homomorphic Encryption", "Anonymization", "Privacy Regulations", "Audit Trails"], "languages": ["python"]},
                {"id": "cs610", "code": "CS 610", "title": "Data Visualization", "subtitle": "Communicating with Data", "credits": 3, "hours": 45, "difficulty": "intermediate", "prerequisites": ["cs106"], "topics": ["Visualization Theory", "Chart Types", "Interactive Viz", "Dashboard Design", "D3.js", "Storytelling", "Accessibility", "Performance"], "languages": ["javascript", "python"]}
            ]
        },
        {
            "year": 7,
            "name": "Networks Year",
            "theme": "Networking & Security",
            "level": "advanced",
            "hours": 650,
            "courses": [
                {"id": "cs701", "code": "CS 701", "title": "Advanced Networking", "subtitle": "Network Protocols Deep Dive", "credits": 4, "hours": 60, "difficulty": "advanced", "prerequisites": ["cs302"], "topics": ["BGP", "MPLS", "SDN", "Network Virtualization", "Traffic Engineering", "QoS", "IPv6", "Network Troubleshooting"], "languages": ["python"]},
                {"id": "cs702", "code": "CS 702", "title": "Network Security", "subtitle": "Protecting Networks", "credits": 4, "hours": 60, "difficulty": "advanced", "prerequisites": ["cs307", "cs701"], "topics": ["Firewalls", "IDS/IPS", "VPNs", "PKI", "TLS", "Network Forensics", "DDoS Mitigation", "Zero Trust"], "languages": ["python"]},
                {"id": "cs703", "code": "CS 703", "title": "Web Security", "subtitle": "Securing Web Applications", "credits": 4, "hours": 60, "difficulty": "advanced", "prerequisites": ["cs307", "cs505"], "topics": ["OWASP Top 10", "XSS", "CSRF", "SQL Injection", "Authentication", "Session Management", "CSP", "Security Headers"], "languages": ["javascript", "python"]},
                {"id": "cs704", "code": "CS 704", "title": "Malware Analysis", "subtitle": "Understanding Threats", "credits": 4, "hours": 60, "difficulty": "advanced", "prerequisites": ["cs301", "cs307"], "topics": ["Static Analysis", "Dynamic Analysis", "Reverse Engineering", "Sandboxing", "Behavioral Analysis", "Threat Intelligence", "Incident Response", "Forensics"], "languages": ["c", "python"]},
                {"id": "cs705", "code": "CS 705", "title": "Penetration Testing", "subtitle": "Ethical Hacking", "credits": 4, "hours": 60, "difficulty": "advanced", "prerequisites": ["cs307", "cs702"], "topics": ["Reconnaissance", "Scanning", "Exploitation", "Post-Exploitation", "Reporting", "Red Team Operations", "Social Engineering", "Physical Security"], "languages": ["python", "bash"]},
                {"id": "cs706", "code": "CS 706", "title": "Applied Cryptography", "subtitle": "Crypto in Practice", "credits": 4, "hours": 60, "difficulty": "advanced", "prerequisites": ["cs404"], "topics": ["Protocol Design", "Key Management", "HSMs", "Secure Channels", "Password Hashing", "Random Number Generation", "Side-Channel Attacks", "Post-Quantum Crypto"], "languages": ["python", "rust"]},
                {"id": "cs707", "code": "CS 707", "title": "IoT Security", "subtitle": "Securing Connected Devices", "credits": 3, "hours": 45, "difficulty": "advanced", "prerequisites": ["cs304", "cs307"], "topics": ["IoT Protocols", "Embedded Security", "Secure Boot", "OTA Updates", "Device Authentication", "Edge Security", "Privacy", "Regulations"], "languages": ["c", "python"]},
                {"id": "cs708", "code": "CS 708", "title": "Cloud Security", "subtitle": "Securing Cloud Infrastructure", "credits": 3, "hours": 45, "difficulty": "advanced", "prerequisites": ["cs309", "cs307"], "topics": ["IAM", "Data Encryption", "Network Security", "Compliance", "Container Security", "Serverless Security", "CSPM", "Incident Response"], "languages": ["python", "yaml"]},
                {"id": "cs709", "code": "CS 709", "title": "Security Operations", "subtitle": "Managing Security", "credits": 3, "hours": 45, "difficulty": "advanced", "prerequisites": ["cs702"], "topics": ["SOC Operations", "SIEM", "Threat Hunting", "Vulnerability Management", "Patch Management", "Security Metrics", "Compliance", "Risk Assessment"], "languages": ["python"]},
                {"id": "cs710", "code": "CS 710", "title": "Privacy Engineering", "subtitle": "Building Privacy-First Systems", "credits": 3, "hours": 45, "difficulty": "advanced", "prerequisites": ["cs609", "cs703"], "topics": ["Privacy by Design", "GDPR/CCPA", "Consent Management", "Data Minimization", "Anonymization", "Privacy Impact Assessment", "Tracking Prevention", "User Rights"], "languages": ["python"]}
            ]
        },
        {
            "year": 8,
            "name": "AI Foundations Year",
            "theme": "Machine Learning & AI",
            "level": "advanced",
            "hours": 700,
            "courses": [
                {"id": "cs801", "code": "CS 801", "title": "Machine Learning", "subtitle": "Learning from Data", "credits": 4, "hours": 60, "difficulty": "advanced", "prerequisites": ["cs202", "cs204"], "topics": ["Supervised Learning", "Unsupervised Learning", "Neural Networks", "Decision Trees", "SVMs", "Ensemble Methods", "Model Selection", "Bias-Variance"], "languages": ["python"]},
                {"id": "cs802", "code": "CS 802", "title": "Deep Learning", "subtitle": "Neural Network Mastery", "credits": 4, "hours": 60, "difficulty": "advanced", "prerequisites": ["cs801"], "topics": ["CNNs", "RNNs", "Transformers", "GANs", "Autoencoders", "Optimization", "Regularization", "Transfer Learning"], "languages": ["python"]},
                {"id": "cs803", "code": "CS 803", "title": "Natural Language Processing", "subtitle": "Understanding Human Language", "credits": 4, "hours": 60, "difficulty": "advanced", "prerequisites": ["cs801", "cs802"], "topics": ["Text Processing", "Word Embeddings", "Language Models", "Sequence-to-Sequence", "Attention Mechanisms", "BERT/GPT", "NER", "Question Answering"], "languages": ["python"]},
                {"id": "cs804", "code": "CS 804", "title": "Computer Vision", "subtitle": "Teaching Computers to See", "credits": 4, "hours": 60, "difficulty": "advanced", "prerequisites": ["cs801", "cs802"], "topics": ["Image Processing", "Object Detection", "Image Segmentation", "Face Recognition", "Pose Estimation", "Video Analysis", "3D Vision", "Medical Imaging"], "languages": ["python"]},
                {"id": "cs805", "code": "CS 805", "title": "Reinforcement Learning", "subtitle": "Learning by Interaction", "credits": 4, "hours": 60, "difficulty": "advanced", "prerequisites": ["cs801"], "topics": ["MDPs", "Q-Learning", "Policy Gradient", "Actor-Critic", "Deep RL", "Multi-Agent RL", "Inverse RL", "Real-World Applications"], "languages": ["python"]},
                {"id": "cs806", "code": "CS 806", "title": "AI Ethics & Safety", "subtitle": "Responsible AI", "credits": 3, "hours": 45, "difficulty": "advanced", "prerequisites": ["cs801"], "topics": ["Fairness", "Transparency", "Accountability", "Privacy", "Bias", "Alignment", "Robustness", "Governance"], "languages": []},
                {"id": "cs807", "code": "CS 807", "title": "MLOps", "subtitle": "ML in Production", "credits": 3, "hours": 45, "difficulty": "advanced", "prerequisites": ["cs801", "cs310"], "topics": ["Model Deployment", "Monitoring", "Versioning", "Feature Stores", "Data Pipelines", "A/B Testing", "Model Registry", "AutoML"], "languages": ["python"]},
                {"id": "cs808", "code": "CS 808", "title": "Probabilistic ML", "subtitle": "Uncertainty in ML", "credits": 4, "hours": 60, "difficulty": "advanced", "prerequisites": ["cs801"], "topics": ["Bayesian Methods", "Graphical Models", "Variational Inference", "MCMC", "Gaussian Processes", "Bayesian Neural Networks", "Active Learning", "Causal Inference"], "languages": ["python"]},
                {"id": "cs809", "code": "CS 809", "title": "Speech Recognition", "subtitle": "Understanding Speech", "credits": 3, "hours": 45, "difficulty": "advanced", "prerequisites": ["cs802", "cs803"], "topics": ["Acoustic Modeling", "Language Modeling", "HMMs", "CTC", "End-to-End ASR", "Speaker Recognition", "Speech Synthesis", "Multimodal"], "languages": ["python"]},
                {"id": "cs810", "code": "CS 810", "title": "Robotics", "subtitle": "Intelligent Machines", "credits": 4, "hours": 60, "difficulty": "advanced", "prerequisites": ["cs804", "cs805"], "topics": ["Kinematics", "Motion Planning", "SLAM", "Control Systems", "Perception", "Manipulation", "Human-Robot Interaction", "Simulation"], "languages": ["python", "cpp"]}
            ]
        },
        {
            "year": 9,
            "name": "Compilers Year",
            "theme": "Language Implementation",
            "level": "advanced",
            "hours": 700,
            "courses": [
                {"id": "cs901", "code": "CS 901", "title": "Compiler Design II", "subtitle": "Advanced Compilation", "credits": 4, "hours": 60, "difficulty": "expert", "prerequisites": ["cs306"], "topics": ["SSA Form", "Data Flow Analysis", "Control Flow Analysis", "Loop Optimization", "Interprocedural Analysis", "Alias Analysis", "Points-to Analysis", "Profile-Guided Optimization"], "languages": ["cpp"]},
                {"id": "cs902", "code": "CS 902", "title": "Program Analysis", "subtitle": "Understanding Programs", "credits": 4, "hours": 60, "difficulty": "expert", "prerequisites": ["cs901"], "topics": ["Abstract Interpretation", "Type Systems", "Symbolic Execution", "Concolic Testing", "Taint Analysis", "Information Flow", "Bug Detection", "Security Analysis"], "languages": ["python"]},
                {"id": "cs903", "code": "CS 903", "title": "Code Generation", "subtitle": "From IR to Machine Code", "credits": 4, "hours": 60, "difficulty": "expert", "prerequisites": ["cs901"], "topics": ["Instruction Selection", "Register Allocation", "Instruction Scheduling", "Peephole Optimization", "Target-Specific Codegen", "SIMD Generation", "Link-Time Optimization", "Debug Information"], "languages": ["cpp"]},
                {"id": "cs904", "code": "CS 904", "title": "Runtime Systems", "subtitle": "Program Execution Support", "credits": 4, "hours": 60, "difficulty": "expert", "prerequisites": ["cs301", "cs901"], "topics": ["Memory Management", "Garbage Collection", "JIT Compilation", "Dynamic Loading", "Exception Handling", "Reflection", "Threading", "FFI"], "languages": ["c", "cpp"]},
                {"id": "cs905", "code": "CS 905", "title": "Virtual Machines", "subtitle": "Software CPUs", "credits": 4, "hours": 60, "difficulty": "expert", "prerequisites": ["cs904"], "topics": ["Interpretation", "JIT Compilation", "Tracing JIT", "Method JIT", "Inline Caching", "Deoptimization", "Safepoints", "Profile Collection"], "languages": ["cpp"]},
                {"id": "cs906", "code": "CS 906", "title": "Language Design", "subtitle": "Creating Programming Languages", "credits": 4, "hours": 60, "difficulty": "expert", "prerequisites": ["cs205", "cs901"], "topics": ["Syntax Design", "Type System Design", "Semantics", "Pragmatics", "Paradigm Selection", "Error Messages", "Tooling", "Evolution"], "languages": ["rust", "haskell"]},
                {"id": "cs907", "code": "CS 907", "title": "Domain-Specific Languages", "subtitle": "Languages for Specific Tasks", "credits": 3, "hours": 45, "difficulty": "expert", "prerequisites": ["cs906"], "topics": ["Internal DSLs", "External DSLs", "Language Workbenches", "Code Generation", "IDE Support", "Testing DSLs", "DSL Evolution", "Case Studies"], "languages": ["scala", "kotlin"]},
                {"id": "cs908", "code": "CS 908", "title": "Type Theory", "subtitle": "Types as Logic", "credits": 4, "hours": 60, "difficulty": "expert", "prerequisites": ["cs407", "cs906"], "topics": ["Simply Typed Lambda Calculus", "Polymorphism", "Dependent Types", "Linear Types", "Effect Systems", "Subtyping", "Type Inference", "Gradual Typing"], "languages": ["haskell", "agda"]},
                {"id": "cs909", "code": "CS 909", "title": "Program Synthesis", "subtitle": "Automatic Programming", "credits": 3, "hours": 45, "difficulty": "expert", "prerequisites": ["cs406", "cs902"], "topics": ["Inductive Synthesis", "Deductive Synthesis", "Sketch-Based", "Example-Based", "Neural Synthesis", "Constraint Solving", "Verification", "Applications"], "languages": ["python"]},
                {"id": "cs910", "code": "CS 910", "title": "Binary Analysis", "subtitle": "Reverse Engineering", "credits": 4, "hours": 60, "difficulty": "expert", "prerequisites": ["cs206", "cs902"], "topics": ["Disassembly", "Decompilation", "Control Flow Recovery", "Type Recovery", "Symbolic Execution", "Fuzzing", "Patching", "Malware Analysis"], "languages": ["c", "python"]}
            ]
        },
        {
            "year": 10,
            "name": "Graphics Year",
            "theme": "Computer Graphics & Visualization",
            "level": "advanced",
            "hours": 700,
            "courses": [
                {"id": "cs1001", "code": "CS 1001", "title": "Computer Graphics", "subtitle": "Creating Visual Worlds", "credits": 4, "hours": 60, "difficulty": "advanced", "prerequisites": ["cs201"], "topics": ["Rasterization", "Ray Tracing", "Shading", "Texturing", "Lighting", "Shadows", "Global Illumination", "GPU Programming"], "languages": ["cpp", "glsl"]},
                {"id": "cs1002", "code": "CS 1002", "title": "Real-Time Rendering", "subtitle": "Graphics at 60 FPS", "credits": 4, "hours": 60, "difficulty": "advanced", "prerequisites": ["cs1001"], "topics": ["GPU Architecture", "Shaders", "Deferred Rendering", "PBR", "Post-Processing", "LOD", "Culling", "Optimization"], "languages": ["cpp", "hlsl"]},
                {"id": "cs1003", "code": "CS 1003", "title": "Physically Based Rendering", "subtitle": "Realistic Images", "credits": 4, "hours": 60, "difficulty": "expert", "prerequisites": ["cs1001"], "topics": ["BRDF", "Light Transport", "Monte Carlo Methods", "Path Tracing", "Photon Mapping", "Spectral Rendering", "Subsurface Scattering", "Volumetrics"], "languages": ["cpp"]},
                {"id": "cs1004", "code": "CS 1004", "title": "Computational Geometry", "subtitle": "Algorithms for Shapes", "credits": 4, "hours": 60, "difficulty": "advanced", "prerequisites": ["cs202", "cs203"], "topics": ["Convex Hull", "Triangulation", "Voronoi Diagrams", "Range Searching", "Intersection", "Motion Planning", "Mesh Processing", "Surface Reconstruction"], "languages": ["cpp"]},
                {"id": "cs1005", "code": "CS 1005", "title": "Animation", "subtitle": "Bringing Objects to Life", "credits": 4, "hours": 60, "difficulty": "advanced", "prerequisites": ["cs1001"], "topics": ["Keyframing", "Interpolation", "Skeletal Animation", "Inverse Kinematics", "Physics Simulation", "Cloth Simulation", "Fluid Simulation", "Motion Capture"], "languages": ["cpp", "python"]},
                {"id": "cs1006", "code": "CS 1006", "title": "Scientific Visualization", "subtitle": "Visualizing Data", "credits": 4, "hours": 60, "difficulty": "advanced", "prerequisites": ["cs1001", "cs610"], "topics": ["Volume Rendering", "Flow Visualization", "Scalar Fields", "Vector Fields", "Isosurfaces", "Streamlines", "Uncertainty", "Large Data"], "languages": ["cpp", "python"]},
                {"id": "cs1007", "code": "CS 1007", "title": "Virtual Reality", "subtitle": "Immersive Experiences", "credits": 4, "hours": 60, "difficulty": "advanced", "prerequisites": ["cs1001", "cs1002"], "topics": ["VR Hardware", "Rendering for VR", "Interaction", "Locomotion", "Presence", "Performance", "Social VR", "Applications"], "languages": ["cpp", "csharp"]},
                {"id": "cs1008", "code": "CS 1008", "title": "Augmented Reality", "subtitle": "Blending Realities", "credits": 3, "hours": 45, "difficulty": "advanced", "prerequisites": ["cs804", "cs1007"], "topics": ["AR Hardware", "Tracking", "Registration", "Occlusion", "Lighting Estimation", "Hand Tracking", "AR Cloud", "Applications"], "languages": ["cpp", "swift"]},
                {"id": "cs1009", "code": "CS 1009", "title": "GPU Computing", "subtitle": "Parallel Processing Power", "credits": 3, "hours": 45, "difficulty": "advanced", "prerequisites": ["cs308", "cs1002"], "topics": ["CUDA", "OpenCL", "Compute Shaders", "Memory Hierarchy", "Parallel Patterns", "Optimization", "Multi-GPU", "Applications"], "languages": ["cuda", "cpp"]},
                {"id": "cs1010", "code": "CS 1010", "title": "Geometric Modeling", "subtitle": "Creating 3D Shapes", "credits": 4, "hours": 60, "difficulty": "advanced", "prerequisites": ["cs1001", "cs1004"], "topics": ["Curves", "Surfaces", "Subdivision", "Procedural Modeling", "CSG", "Implicit Surfaces", "Point Clouds", "Mesh Processing"], "languages": ["cpp", "python"]}
            ]
        },
        {
            "year": 11,
            "name": "Research Year I",
            "theme": "Advanced Algorithms & Complexity",
            "level": "expert",
            "hours": 700,
            "courses": [
                {"id": "cs1101", "code": "CS 1101", "title": "Advanced Algorithms", "subtitle": "Research-Level Algorithms", "credits": 4, "hours": 60, "difficulty": "expert", "prerequisites": ["cs203", "cs403"], "topics": ["Online Algorithms", "Streaming Algorithms", "Sublinear Algorithms", "Parallel Algorithms", "External Memory Algorithms", "Cache-Oblivious Algorithms", "Quantum Algorithms", "Fine-Grained Complexity"], "languages": ["cpp"]},
                {"id": "cs1102", "code": "CS 1102", "title": "Algorithmic Game Theory", "subtitle": "Algorithms Meet Economics", "credits": 4, "hours": 60, "difficulty": "expert", "prerequisites": ["cs203"], "topics": ["Mechanism Design", "Auction Theory", "Price of Anarchy", "Matching Markets", "Social Choice", "Network Games", "Learning in Games", "Blockchain Mechanisms"], "languages": ["python"]},
                {"id": "cs1103", "code": "CS 1103", "title": "Optimization", "subtitle": "Finding the Best", "credits": 4, "hours": 60, "difficulty": "expert", "prerequisites": ["cs203"], "topics": ["Linear Programming", "Convex Optimization", "Integer Programming", "Combinatorial Optimization", "Semidefinite Programming", "Submodular Optimization", "Online Optimization", "Numerical Methods"], "languages": ["python"]},
                {"id": "cs1104", "code": "CS 1104", "title": "Parameterized Complexity", "subtitle": "Beyond NP-Hardness", "credits": 4, "hours": 60, "difficulty": "expert", "prerequisites": ["cs403"], "topics": ["Fixed-Parameter Tractability", "Kernelization", "Branching Algorithms", "Treewidth", "W-Hierarchy", "ETH", "Parameterized Counting", "Applications"], "languages": []},
                {"id": "cs1105", "code": "CS 1105", "title": "Communication Complexity", "subtitle": "Limits of Communication", "credits": 4, "hours": 60, "difficulty": "expert", "prerequisites": ["cs403"], "topics": ["Deterministic CC", "Randomized CC", "One-Way CC", "NOF Model", "Lower Bounds", "Applications", "Quantum CC", "Information Complexity"], "languages": []},
                {"id": "cs1106", "code": "CS 1106", "title": "Proof Complexity", "subtitle": "Hardness of Proofs", "credits": 4, "hours": 60, "difficulty": "expert", "prerequisites": ["cs406"], "topics": ["Propositional Proof Systems", "Resolution", "Cutting Planes", "Algebraic Systems", "Lower Bounds", "Automatability", "Proof Search", "SAT Solving"], "languages": []},
                {"id": "cs1107", "code": "CS 1107", "title": "Coding Theory", "subtitle": "Information Protection", "credits": 4, "hours": 60, "difficulty": "expert", "prerequisites": ["cs405"], "topics": ["Linear Codes", "Reed-Solomon", "LDPC", "Polar Codes", "List Decoding", "Locally Decodable", "Quantum Error Correction", "Applications"], "languages": ["python"]},
                {"id": "cs1108", "code": "CS 1108", "title": "Derandomization", "subtitle": "Removing Randomness", "credits": 3, "hours": 45, "difficulty": "expert", "prerequisites": ["cs409"], "topics": ["Pseudorandom Generators", "Expanders", "Extractors", "Hardness vs Randomness", "BPP vs P", "Hashing", "Space-Bounded Derandomization", "Applications"], "languages": []},
                {"id": "cs1109", "code": "CS 1109", "title": "Algebraic Algorithms", "subtitle": "Algebra for Computing", "credits": 3, "hours": 45, "difficulty": "expert", "prerequisites": ["cs204"], "topics": ["Polynomial Identity Testing", "Polynomial Factoring", "Matrix Multiplication", "Linear Algebra Algorithms", "Algebraic Complexity", "GCT", "Tensor Decomposition", "Applications"], "languages": ["python"]},
                {"id": "cs1110", "code": "CS 1110", "title": "High-Dimensional Computation", "subtitle": "Algorithms in High Dimensions", "credits": 4, "hours": 60, "difficulty": "expert", "prerequisites": ["cs1103"], "topics": ["Concentration Inequalities", "Random Projection", "Nearest Neighbor Search", "Dimensionality Reduction", "Compressed Sensing", "Sparse Recovery", "Geometric Learning", "Applications"], "languages": ["python"]}
            ]
        },
        {
            "year": 12,
            "name": "Research Year II",
            "theme": "Distributed Computing & Systems",
            "level": "expert",
            "hours": 700,
            "courses": [
                {"id": "cs1201", "code": "CS 1201", "title": "Distributed Algorithms", "subtitle": "Algorithms for Networks", "credits": 4, "hours": 60, "difficulty": "expert", "prerequisites": ["cs503"], "topics": ["Leader Election", "Mutual Exclusion", "Consensus", "Broadcast", "Failure Detectors", "Self-Stabilization", "LOCAL Model", "CONGEST Model"], "languages": []},
                {"id": "cs1202", "code": "CS 1202", "title": "Distributed Computing Theory", "subtitle": "Fundamentals of Distribution", "credits": 4, "hours": 60, "difficulty": "expert", "prerequisites": ["cs1201"], "topics": ["FLP Impossibility", "CAP Theorem", "Linearizability", "Wait-Freedom", "Lock-Freedom", "Shared Memory", "Message Passing", "Byzantine Fault Tolerance"], "languages": []},
                {"id": "cs1203", "code": "CS 1203", "title": "Concurrent Data Structures", "subtitle": "Sharing Data Safely", "credits": 4, "hours": 60, "difficulty": "expert", "prerequisites": ["cs201", "cs1202"], "topics": ["Lock-Free Queues", "Skip Lists", "Hash Tables", "Trees", "Memory Reclamation", "Transactional Memory", "Relaxed Data Structures", "Performance"], "languages": ["cpp", "java"]},
                {"id": "cs1204", "code": "CS 1204", "title": "Fault-Tolerant Computing", "subtitle": "Building Reliable Systems", "credits": 4, "hours": 60, "difficulty": "expert", "prerequisites": ["cs503", "cs1202"], "topics": ["Replication", "Checkpointing", "Recovery", "Byzantine Agreement", "Quorum Systems", "Atomic Commit", "Paxos/Raft", "Practical Systems"], "languages": ["go", "rust"]},
                {"id": "cs1205", "code": "CS 1205", "title": "Peer-to-Peer Systems", "subtitle": "Decentralized Computing", "credits": 3, "hours": 45, "difficulty": "expert", "prerequisites": ["cs503", "cs701"], "topics": ["DHTs", "Content Distribution", "Overlay Networks", "Gossip Protocols", "Incentives", "Security", "NAT Traversal", "Applications"], "languages": ["go"]},
                {"id": "cs1206", "code": "CS 1206", "title": "Operating System Design", "subtitle": "Building Operating Systems", "credits": 4, "hours": 60, "difficulty": "expert", "prerequisites": ["cs301", "cs303"], "topics": ["Microkernel", "Exokernel", "Unikernel", "Virtual Machine Monitors", "Container Runtimes", "Storage Systems", "Networking Stack", "Security"], "languages": ["c", "rust"]},
                {"id": "cs1207", "code": "CS 1207", "title": "File Systems", "subtitle": "Managing Persistent Data", "credits": 4, "hours": 60, "difficulty": "expert", "prerequisites": ["cs301", "cs1206"], "topics": ["FFS", "LFS", "Copy-on-Write", "Journaling", "Crash Consistency", "Distributed File Systems", "Flash File Systems", "Deduplication"], "languages": ["c"]},
                {"id": "cs1208", "code": "CS 1208", "title": "Memory Systems", "subtitle": "Advanced Memory Management", "credits": 4, "hours": 60, "difficulty": "expert", "prerequisites": ["cs206", "cs904"], "topics": ["Virtual Memory", "Page Tables", "TLB", "NUMA", "Memory Allocators", "Garbage Collection", "Persistent Memory", "Memory Security"], "languages": ["c", "cpp"]},
                {"id": "cs1209", "code": "CS 1209", "title": "Storage Systems", "subtitle": "Data Persistence at Scale", "credits": 3, "hours": 45, "difficulty": "expert", "prerequisites": ["cs601", "cs1207"], "topics": ["Block Storage", "Object Storage", "Key-Value Stores", "LSM Trees", "B-Trees", "Compression", "Erasure Coding", "Tiering"], "languages": ["cpp", "rust"]},
                {"id": "cs1210", "code": "CS 1210", "title": "Systems Performance", "subtitle": "Making Systems Fast", "credits": 4, "hours": 60, "difficulty": "expert", "prerequisites": ["cs206", "cs301"], "topics": ["Profiling", "Tracing", "Benchmarking", "Workload Analysis", "Capacity Planning", "Kernel Tuning", "Application Tuning", "Performance Engineering"], "languages": ["c", "python"]}
            ]
        },
        {
            "year": 13,
            "name": "Specialization Year",
            "theme": "Domain Expertise",
            "level": "master",
            "hours": 700,
            "courses": [
                {"id": "cs1301", "code": "CS 1301", "title": "Advanced Machine Learning", "subtitle": "Cutting-Edge ML", "credits": 4, "hours": 60, "difficulty": "master", "prerequisites": ["cs801", "cs802"], "topics": ["Meta-Learning", "Few-Shot Learning", "Self-Supervised Learning", "Contrastive Learning", "Foundation Models", "Efficient ML", "ML Theory", "Emerging Directions"], "languages": ["python"]},
                {"id": "cs1302", "code": "CS 1302", "title": "Large Language Models", "subtitle": "The GPT Era", "credits": 4, "hours": 60, "difficulty": "master", "prerequisites": ["cs803"], "topics": ["Transformer Architecture", "Pre-training", "Fine-tuning", "RLHF", "Prompt Engineering", "RAG", "Agents", "Safety"], "languages": ["python"]},
                {"id": "cs1303", "code": "CS 1303", "title": "Advanced Deep Learning", "subtitle": "Beyond the Basics", "credits": 4, "hours": 60, "difficulty": "master", "prerequisites": ["cs802"], "topics": ["Normalization", "Attention Mechanisms", "Memory Networks", "Neural Architecture Search", "Pruning/Quantization", "Knowledge Distillation", "Continual Learning", "Interpretability"], "languages": ["python"]},
                {"id": "cs1304", "code": "CS 1304", "title": "Advanced Computer Vision", "subtitle": "State-of-the-Art Vision", "credits": 4, "hours": 60, "difficulty": "master", "prerequisites": ["cs804"], "topics": ["Vision Transformers", "Self-Supervised Vision", "3D Understanding", "Neural Radiance Fields", "Generative Models", "Video Understanding", "Multimodal Vision", "Efficient Vision"], "languages": ["python"]},
                {"id": "cs1305", "code": "CS 1305", "title": "Advanced NLP", "subtitle": "Language Understanding", "credits": 4, "hours": 60, "difficulty": "master", "prerequisites": ["cs803", "cs1302"], "topics": ["Semantic Parsing", "Dialogue Systems", "Knowledge Graphs", "Multilinguality", "Low-Resource NLP", "Grounding", "Reasoning", "Evaluation"], "languages": ["python"]},
                {"id": "cs1306", "code": "CS 1306", "title": "Bioinformatics", "subtitle": "Computing for Biology", "credits": 4, "hours": 60, "difficulty": "master", "prerequisites": ["cs202", "cs801"], "topics": ["Sequence Analysis", "Genome Assembly", "Phylogenetics", "Protein Structure", "Gene Expression", "Systems Biology", "Drug Discovery", "Clinical Informatics"], "languages": ["python", "r"]},
                {"id": "cs1307", "code": "CS 1307", "title": "Computational Finance", "subtitle": "Algorithms for Markets", "credits": 4, "hours": 60, "difficulty": "master", "prerequisites": ["cs801", "cs1103"], "topics": ["Algorithmic Trading", "Portfolio Optimization", "Risk Management", "Derivatives Pricing", "Market Microstructure", "High-Frequency Trading", "Alternative Data", "ML in Finance"], "languages": ["python"]},
                {"id": "cs1308", "code": "CS 1308", "title": "Quantum Machine Learning", "subtitle": "ML Meets Quantum", "credits": 3, "hours": 45, "difficulty": "master", "prerequisites": ["cs408", "cs801"], "topics": ["Quantum Feature Maps", "Variational Circuits", "Quantum Kernels", "Quantum Neural Networks", "Quantum Advantage", "NISQ Algorithms", "Classical Simulation", "Applications"], "languages": ["python"]},
                {"id": "cs1309", "code": "CS 1309", "title": "Formal Methods in Practice", "subtitle": "Verification at Scale", "credits": 4, "hours": 60, "difficulty": "master", "prerequisites": ["cs406", "cs902"], "topics": ["Industrial Verification", "Hardware Verification", "Protocol Verification", "Smart Contract Verification", "Compositional Verification", "Abstraction Refinement", "Certification", "Case Studies"], "languages": ["coq", "tla+"]},
                {"id": "cs1310", "code": "CS 1310", "title": "High-Performance Computing", "subtitle": "Extreme Scale Computing", "credits": 4, "hours": 60, "difficulty": "master", "prerequisites": ["cs308", "cs1009"], "topics": ["Supercomputer Architecture", "MPI Advanced", "Hybrid Parallelism", "Load Balancing", "Scalability", "Energy Efficiency", "Resilience", "Exascale"], "languages": ["cpp", "fortran"]}
            ]
        },
        {
            "year": 14,
            "name": "Innovation Year",
            "theme": "Original Research",
            "level": "master",
            "hours": 700,
            "courses": [
                {"id": "cs1401", "code": "CS 1401", "title": "Research Methods in CS", "subtitle": "Conducting Research", "credits": 4, "hours": 60, "difficulty": "master", "prerequisites": [], "topics": ["Problem Selection", "Literature Review", "Experimental Design", "Writing Papers", "Peer Review", "Presentations", "Ethics", "Collaboration"], "languages": []},
                {"id": "cs1402", "code": "CS 1402", "title": "Systems Research Seminar", "subtitle": "Reading Systems Papers", "credits": 3, "hours": 45, "difficulty": "master", "prerequisites": ["cs503"], "topics": ["Classic Papers", "Recent Work", "Paper Presentation", "Critical Analysis", "Research Directions", "Artifact Evaluation", "Reproduction Studies", "Benchmarking"], "languages": []},
                {"id": "cs1403", "code": "CS 1403", "title": "Theory Research Seminar", "subtitle": "Reading Theory Papers", "credits": 3, "hours": 45, "difficulty": "master", "prerequisites": ["cs403"], "topics": ["Proof Techniques", "Problem Selection", "Open Problems", "Paper Presentation", "Collaboration", "Theory Culture", "Impact", "Career Paths"], "languages": []},
                {"id": "cs1404", "code": "CS 1404", "title": "ML Research Seminar", "subtitle": "Reading ML Papers", "credits": 3, "hours": 45, "difficulty": "master", "prerequisites": ["cs801"], "topics": ["Empirical Methods", "Ablation Studies", "Reproducibility", "Benchmarks", "Dataset Creation", "Negative Results", "Hype vs Reality", "Responsible ML"], "languages": []},
                {"id": "cs1405", "code": "CS 1405", "title": "Research Project I", "subtitle": "Independent Research", "credits": 6, "hours": 120, "difficulty": "master", "prerequisites": ["cs1401"], "topics": ["Project Definition", "Literature Survey", "Implementation", "Experimentation", "Analysis", "Writing", "Presentation", "Iteration"], "languages": []},
                {"id": "cs1406", "code": "CS 1406", "title": "Research Project II", "subtitle": "Advanced Research", "credits": 6, "hours": 120, "difficulty": "master", "prerequisites": ["cs1405"], "topics": ["Deep Investigation", "Novel Contributions", "Paper Writing", "Submission", "Response to Reviews", "Camera Ready", "Presentation", "Future Work"], "languages": []},
                {"id": "cs1407", "code": "CS 1407", "title": "Industry Research", "subtitle": "Research in Practice", "credits": 4, "hours": 60, "difficulty": "master", "prerequisites": ["cs1401"], "topics": ["Industry vs Academia", "Product Research", "Tech Transfer", "Patents", "Research Teams", "Impact Metrics", "Communication", "Career Paths"], "languages": []},
                {"id": "cs1408", "code": "CS 1408", "title": "Open Source Development", "subtitle": "Contributing to OSS", "credits": 3, "hours": 45, "difficulty": "master", "prerequisites": [], "topics": ["OSS Culture", "Contributing", "Maintaining", "Community Building", "Governance", "Sustainability", "Legal Issues", "Impact"], "languages": []},
                {"id": "cs1409", "code": "CS 1409", "title": "Teaching Computer Science", "subtitle": "CS Education", "credits": 3, "hours": 45, "difficulty": "master", "prerequisites": [], "topics": ["Pedagogy", "Curriculum Design", "Assessment", "Active Learning", "Online Teaching", "Diversity", "Misconceptions", "Research in CSEd"], "languages": []},
                {"id": "cs1410", "code": "CS 1410", "title": "Thesis Preparation", "subtitle": "Writing Your Thesis", "credits": 4, "hours": 60, "difficulty": "master", "prerequisites": ["cs1406"], "topics": ["Thesis Structure", "Writing Process", "Committee Selection", "Defense Preparation", "Revisions", "Submission", "Publication", "Career Planning"], "languages": []}
            ]
        },
        {
            "year": 15,
            "name": "Mastery Year",
            "theme": "Teaching & Leadership",
            "level": "phd",
            "hours": 700,
            "courses": [
                {"id": "cs1501", "code": "CS 1501", "title": "Doctoral Dissertation", "subtitle": "Original Contribution", "credits": 12, "hours": 240, "difficulty": "phd", "prerequisites": ["cs1410"], "topics": ["Novel Research", "Significant Contribution", "Dissertation Writing", "Defense", "Publication Strategy", "Impact", "Future Directions", "Career Launch"], "languages": []},
                {"id": "cs1502", "code": "CS 1502", "title": "Research Leadership", "subtitle": "Leading Research Teams", "credits": 3, "hours": 45, "difficulty": "phd", "prerequisites": ["cs1401"], "topics": ["Team Building", "Mentorship", "Project Management", "Funding", "Collaboration", "Vision Setting", "Culture Building", "Conflict Resolution"], "languages": []},
                {"id": "cs1503", "code": "CS 1503", "title": "Grant Writing", "subtitle": "Funding Your Research", "credits": 3, "hours": 45, "difficulty": "phd", "prerequisites": ["cs1401"], "topics": ["Funding Sources", "Proposal Structure", "Budget Planning", "Review Process", "Rejection Handling", "Program Management", "Reporting", "Sustainability"], "languages": []},
                {"id": "cs1504", "code": "CS 1504", "title": "Academic Career Development", "subtitle": "The Academic Path", "credits": 2, "hours": 30, "difficulty": "phd", "prerequisites": [], "topics": ["Job Market", "Application Materials", "Interviews", "Negotiation", "Tenure Track", "Teaching Portfolio", "Service", "Work-Life Balance"], "languages": []},
                {"id": "cs1505", "code": "CS 1505", "title": "Industry Career Development", "subtitle": "Beyond Academia", "credits": 2, "hours": 30, "difficulty": "phd", "prerequisites": [], "topics": ["Industry Opportunities", "Research Labs", "Startups", "Consulting", "Interview Preparation", "Negotiation", "Transition", "Impact"], "languages": []},
                {"id": "cs1506", "code": "CS 1506", "title": "Science Communication", "subtitle": "Sharing Your Work", "credits": 3, "hours": 45, "difficulty": "phd", "prerequisites": [], "topics": ["Public Speaking", "Popular Writing", "Media Relations", "Social Media", "Podcasts", "Videos", "Policy Engagement", "Outreach"], "languages": []},
                {"id": "cs1507", "code": "CS 1507", "title": "Ethics in Computing Research", "subtitle": "Responsible Research", "credits": 3, "hours": 45, "difficulty": "phd", "prerequisites": [], "topics": ["Research Ethics", "Human Subjects", "Dual Use", "Responsible Disclosure", "Authorship", "Conflicts of Interest", "Reproducibility", "Societal Impact"], "languages": []},
                {"id": "cs1508", "code": "CS 1508", "title": "Special Topics Seminar", "subtitle": "Cutting-Edge Research", "credits": 3, "hours": 45, "difficulty": "phd", "prerequisites": [], "topics": ["Emerging Areas", "Interdisciplinary Work", "Guest Speakers", "Discussion", "Paper Reading", "Research Ideas", "Collaboration", "Future Trends"], "languages": []},
                {"id": "cs1509", "code": "CS 1509", "title": "Teaching Practicum", "subtitle": "Teaching Experience", "credits": 3, "hours": 45, "difficulty": "phd", "prerequisites": ["cs1409"], "topics": ["Course Design", "Lecture Delivery", "Office Hours", "Assessment", "Feedback", "Course Management", "TA Supervision", "Reflection"], "languages": []},
                {"id": "cs1510", "code": "CS 1510", "title": "Capstone: The Future of Computing", "subtitle": "What's Next?", "credits": 3, "hours": 45, "difficulty": "phd", "prerequisites": [], "topics": ["Emerging Technologies", "Grand Challenges", "Societal Impact", "Responsible Innovation", "Interdisciplinary Frontiers", "Your Contribution", "Legacy", "Celebration"], "languages": []}
            ]
        }
    ]
}

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_all_courses():
    """Get all courses flattened"""
    courses = []
    for year in CS_BIBLE_CURRICULUM["years"]:
        for course in year["courses"]:
            course["year_number"] = year["year"]
            course["year_name"] = year["name"]
            course["year_theme"] = year["theme"]
            courses.append(course)
    return courses

def get_courses_by_year(year_number):
    """Get courses for a specific year"""
    for year in CS_BIBLE_CURRICULUM["years"]:
        if year["year"] == year_number:
            return year
    return None

def get_course_by_id(course_id):
    """Get a specific course by ID"""
    for year in CS_BIBLE_CURRICULUM["years"]:
        for course in year["courses"]:
            if course["id"] == course_id:
                course["year_number"] = year["year"]
                course["year_name"] = year["name"]
                return course
    return None

def get_courses_by_language(language):
    """Get courses that teach a specific language"""
    courses = []
    for year in CS_BIBLE_CURRICULUM["years"]:
        for course in year["courses"]:
            if language in course.get("languages", []):
                courses.append(course)
    return courses

def get_courses_by_difficulty(difficulty):
    """Get courses by difficulty level"""
    courses = []
    for year in CS_BIBLE_CURRICULUM["years"]:
        for course in year["courses"]:
            if course.get("difficulty") == difficulty:
                courses.append(course)
    return courses

def get_curriculum_stats():
    """Get statistics about the curriculum"""
    total_courses = 0
    total_hours = 0
    total_credits = 0
    languages = set()
    difficulties = {}
    
    for year in CS_BIBLE_CURRICULUM["years"]:
        for course in year["courses"]:
            total_courses += 1
            total_hours += course.get("hours", 0)
            total_credits += course.get("credits", 0)
            
            for lang in course.get("languages", []):
                languages.add(lang)
            
            diff = course.get("difficulty", "unknown")
            difficulties[diff] = difficulties.get(diff, 0) + 1
    
    return {
        "total_courses": total_courses,
        "total_hours": total_hours,
        "total_credits": total_credits,
        "total_years": len(CS_BIBLE_CURRICULUM["years"]),
        "languages_covered": list(languages),
        "difficulty_distribution": difficulties
    }

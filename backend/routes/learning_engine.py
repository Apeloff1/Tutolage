"""
╭─────────────────────────────────────────────────────────────────────────╮
│              CODEDOCK IMMERSIVE LEARNING ENGINE v11.6                   │
│                                                                         │
│  Interactive, Gamified Learning with Progress Tracking                  │
│  - Adaptive challenges based on skill level                             │
│  - Spaced repetition for long-term retention                            │
│  - XP, achievements, streaks, and leaderboards                          │
│  - Live code exercises with instant feedback                            │
│  - Personalized learning paths                                          │
╰─────────────────────────────────────────────────────────────────────────╯
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any, Literal
from datetime import datetime, timedelta
from pathlib import Path
from dotenv import load_dotenv
import uuid
import os
import random
import json

# Load environment
ROOT_DIR = Path(__file__).parent.parent
load_dotenv(ROOT_DIR / '.env')

from emergentintegrations.llm.chat import LlmChat, UserMessage
from motor.motor_asyncio import AsyncIOMotorClient

router = APIRouter(prefix="/api/learning", tags=["Immersive Learning Engine"])

EMERGENT_LLM_KEY = os.environ.get('EMERGENT_LLM_KEY', '')
MONGO_URL = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')

# MongoDB Connection
mongo_client = AsyncIOMotorClient(MONGO_URL)
learning_db = mongo_client.codedock_learning

# ============================================================================
# DATA MODELS
# ============================================================================

class LearnerProfile(BaseModel):
    user_id: str
    display_name: str = "Learner"
    xp: int = 0
    level: int = 1
    streak_days: int = 0
    last_active: Optional[datetime] = None
    total_challenges_completed: int = 0
    total_lessons_completed: int = 0
    achievements: List[str] = []
    skill_ratings: Dict[str, int] = {}
    preferred_language: str = "python"
    learning_style: str = "visual"

class Challenge(BaseModel):
    challenge_id: str
    title: str
    description: str
    difficulty: Literal["easy", "medium", "hard", "expert"]
    category: str
    xp_reward: int
    time_limit_seconds: Optional[int] = None
    starter_code: Optional[str] = None
    test_cases: List[Dict[str, Any]] = []
    hints: List[str] = []
    solution_explanation: Optional[str] = None

class ChallengeSubmission(BaseModel):
    challenge_id: str
    user_id: str
    code: str
    language: str = "python"

class QuizQuestion(BaseModel):
    question_id: str
    question: str
    question_type: Literal["multiple_choice", "true_false", "fill_blank", "code_output"]
    options: Optional[List[str]] = None
    correct_answer: str
    explanation: str
    difficulty: int = 1
    category: str
    xp_reward: int = 10

# ============================================================================
# GAMIFICATION SYSTEM
# ============================================================================

LEVEL_THRESHOLDS = [
    0, 100, 250, 500, 1000, 1750, 2750, 4000, 5500, 7500,
    10000, 13000, 16500, 20500, 25000, 30000, 36000, 43000, 51000, 60000
]

ACHIEVEMENTS = {
    "first_steps": {"name": "First Steps", "description": "Complete your first challenge", "xp_bonus": 50, "icon": "footsteps"},
    "streak_3": {"name": "On Fire", "description": "3-day learning streak", "xp_bonus": 100, "icon": "flame"},
    "streak_7": {"name": "Dedicated Learner", "description": "7-day learning streak", "xp_bonus": 250, "icon": "star"},
    "streak_30": {"name": "Learning Machine", "description": "30-day learning streak", "xp_bonus": 1000, "icon": "trophy"},
    "physics_novice": {"name": "Physics Explorer", "description": "Complete 5 physics lessons", "xp_bonus": 150, "icon": "nuclear"},
    "math_wizard": {"name": "Math Wizard", "description": "Complete 10 math lessons", "xp_bonus": 200, "icon": "calculator"},
    "cs_master": {"name": "CS Master", "description": "Complete 20 CS lessons", "xp_bonus": 500, "icon": "code-slash"},
    "perfect_10": {"name": "Perfect 10", "description": "Get 10 challenges correct in a row", "xp_bonus": 300, "icon": "ribbon"},
    "speed_demon": {"name": "Speed Demon", "description": "Complete a challenge in under 60 seconds", "xp_bonus": 100, "icon": "flash"},
    "night_owl": {"name": "Night Owl", "description": "Learn after midnight", "xp_bonus": 50, "icon": "moon"},
    "early_bird": {"name": "Early Bird", "description": "Learn before 7am", "xp_bonus": 50, "icon": "sunny"},
    "explorer": {"name": "Explorer", "description": "Study all 3 subjects", "xp_bonus": 200, "icon": "compass"},
    "level_5": {"name": "Rising Star", "description": "Reach level 5", "xp_bonus": 150, "icon": "star-half"},
    "level_10": {"name": "Scholar", "description": "Reach level 10", "xp_bonus": 500, "icon": "school"},
    "level_20": {"name": "Grandmaster", "description": "Reach level 20", "xp_bonus": 2000, "icon": "diamond"},
    "quiz_ace": {"name": "Quiz Ace", "description": "Score 100% on 5 quizzes", "xp_bonus": 250, "icon": "checkmark-done"},
    "code_warrior": {"name": "Code Warrior", "description": "Complete 50 coding challenges", "xp_bonus": 500, "icon": "shield"},
    "persistent": {"name": "Persistence Pays", "description": "Retry and complete a failed challenge", "xp_bonus": 75, "icon": "refresh"},
}

def calculate_level(xp: int) -> int:
    """Calculate level from XP"""
    for i, threshold in enumerate(LEVEL_THRESHOLDS):
        if xp < threshold:
            return i
    return len(LEVEL_THRESHOLDS)

def xp_to_next_level(xp: int) -> int:
    """Calculate XP needed for next level"""
    level = calculate_level(xp)
    if level >= len(LEVEL_THRESHOLDS):
        return 0
    return LEVEL_THRESHOLDS[level] - xp

# ============================================================================
# SPACED REPETITION SYSTEM (SM-2 Algorithm)
# ============================================================================

class SpacedRepetitionItem(BaseModel):
    item_id: str
    user_id: str
    concept: str
    category: str
    easiness_factor: float = 2.5
    interval: int = 1  # days
    repetitions: int = 0
    next_review: datetime = datetime.utcnow()
    last_review: Optional[datetime] = None

def calculate_sm2(quality: int, item: SpacedRepetitionItem) -> SpacedRepetitionItem:
    """
    SM-2 Spaced Repetition Algorithm
    quality: 0-5 (0-1: complete blackout, 2-3: difficult recall, 4-5: easy recall)
    """
    if quality < 3:
        # Reset on poor recall
        item.repetitions = 0
        item.interval = 1
    else:
        if item.repetitions == 0:
            item.interval = 1
        elif item.repetitions == 1:
            item.interval = 6
        else:
            item.interval = int(item.interval * item.easiness_factor)
        item.repetitions += 1
    
    # Update easiness factor
    item.easiness_factor = max(1.3, item.easiness_factor + 0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
    
    # Schedule next review
    item.last_review = datetime.utcnow()
    item.next_review = datetime.utcnow() + timedelta(days=item.interval)
    
    return item

# ============================================================================
# CHALLENGE BANK
# ============================================================================

CHALLENGE_TEMPLATES = {
    "physics": [
        {
            "title": "Projectile Motion Calculator",
            "description": "Write a function that calculates the maximum height and range of a projectile given initial velocity and angle.",
            "difficulty": "medium",
            "xp_reward": 75,
            "starter_code": "import math\n\ndef projectile_motion(v0, angle_degrees):\n    # v0: initial velocity (m/s)\n    # angle_degrees: launch angle in degrees\n    # Return: (max_height, range) in meters\n    g = 9.8  # gravity\n    \n    # Your code here\n    pass",
            "hints": [
                "Convert angle to radians first: radians = degrees * pi / 180",
                "Max height = (v0 * sin(angle))^2 / (2 * g)",
                "Range = (v0^2 * sin(2*angle)) / g"
            ],
            "test_cases": [
                {"input": {"v0": 20, "angle_degrees": 45}, "expected_height": 10.2, "expected_range": 40.8, "tolerance": 0.5}
            ]
        },
        {
            "title": "Elastic Collision",
            "description": "Implement a function to calculate final velocities after a 1D elastic collision between two objects.",
            "difficulty": "hard",
            "xp_reward": 100,
            "starter_code": "def elastic_collision(m1, v1, m2, v2):\n    # m1, m2: masses\n    # v1, v2: initial velocities\n    # Return: (v1_final, v2_final)\n    \n    # Your code here\n    pass",
            "hints": [
                "Use conservation of momentum: m1*v1 + m2*v2 = m1*v1' + m2*v2'",
                "Use conservation of kinetic energy",
                "v1' = ((m1-m2)v1 + 2*m2*v2) / (m1+m2)"
            ]
        },
        {
            "title": "Simple Gravity Simulation",
            "description": "Create a simple gravity update function for a game object.",
            "difficulty": "easy",
            "xp_reward": 30,
            "starter_code": "def update_position(y, velocity_y, gravity, dt):\n    # y: current height\n    # velocity_y: current vertical velocity\n    # gravity: acceleration due to gravity (positive = down)\n    # dt: time step\n    # Return: (new_y, new_velocity_y)\n    \n    pass",
            "hints": ["velocity = velocity + gravity * dt", "position = position + velocity * dt"]
        }
    ],
    "math": [
        {
            "title": "Vector Dot Product",
            "description": "Implement a function to calculate the dot product of two 3D vectors.",
            "difficulty": "easy",
            "xp_reward": 25,
            "starter_code": "def dot_product(v1, v2):\n    # v1, v2: lists of 3 numbers [x, y, z]\n    # Return: scalar dot product\n    \n    pass",
            "hints": ["Dot product = x1*x2 + y1*y2 + z1*z2"],
            "test_cases": [{"input": {"v1": [1,2,3], "v2": [4,5,6]}, "expected": 32}]
        },
        {
            "title": "Matrix Multiplication",
            "description": "Implement 2x2 matrix multiplication without using numpy.",
            "difficulty": "medium",
            "xp_reward": 60,
            "starter_code": "def matrix_multiply_2x2(a, b):\n    # a, b: 2x2 matrices as nested lists [[a,b],[c,d]]\n    # Return: result matrix\n    \n    pass",
            "hints": ["result[i][j] = sum(a[i][k] * b[k][j] for k in range(2))"]
        },
        {
            "title": "Linear Interpolation (Lerp)",
            "description": "Implement linear interpolation - essential for smooth game animations.",
            "difficulty": "easy",
            "xp_reward": 20,
            "starter_code": "def lerp(a, b, t):\n    # a: start value\n    # b: end value\n    # t: interpolation factor (0 to 1)\n    # Return: interpolated value\n    \n    pass",
            "hints": ["lerp = a + (b - a) * t", "When t=0, result=a. When t=1, result=b"]
        },
        {
            "title": "Quaternion to Euler Angles",
            "description": "Convert quaternion rotation to Euler angles (simplified version).",
            "difficulty": "expert",
            "xp_reward": 150,
            "starter_code": "import math\n\ndef quat_to_euler(w, x, y, z):\n    # Returns (roll, pitch, yaw) in radians\n    \n    pass"
        }
    ],
    "cs": [
        {
            "title": "Binary Search",
            "description": "Implement binary search to find an element in a sorted array.",
            "difficulty": "easy",
            "xp_reward": 30,
            "starter_code": "def binary_search(arr, target):\n    # Return index of target, or -1 if not found\n    \n    pass",
            "hints": ["Use two pointers: left and right", "middle = (left + right) // 2", "If target < arr[mid], search left half"]
        },
        {
            "title": "A* Pathfinding Heuristic",
            "description": "Implement the Manhattan distance heuristic for A* pathfinding.",
            "difficulty": "medium",
            "xp_reward": 50,
            "starter_code": "def manhattan_distance(pos1, pos2):\n    # pos1, pos2: tuples (x, y)\n    # Return: Manhattan distance\n    \n    pass",
            "hints": ["Manhattan distance = |x1-x2| + |y1-y2|"]
        },
        {
            "title": "Simple State Machine",
            "description": "Implement a basic state machine for game AI states.",
            "difficulty": "medium",
            "xp_reward": 75,
            "starter_code": "class StateMachine:\n    def __init__(self):\n        self.states = {}\n        self.current_state = None\n    \n    def add_state(self, name, state_func):\n        pass\n    \n    def set_state(self, name):\n        pass\n    \n    def update(self):\n        pass"
        },
        {
            "title": "Object Pool Pattern",
            "description": "Implement an object pool for efficient game object reuse.",
            "difficulty": "hard",
            "xp_reward": 100,
            "starter_code": "class ObjectPool:\n    def __init__(self, create_func, initial_size=10):\n        self.create_func = create_func\n        self.pool = []\n        self.active = []\n        # Initialize pool\n        pass\n    \n    def acquire(self):\n        # Get object from pool\n        pass\n    \n    def release(self, obj):\n        # Return object to pool\n        pass"
        }
    ]
}

QUIZ_BANK = {
    "physics": [
        {
            "question": "What is the formula for kinetic energy?",
            "question_type": "multiple_choice",
            "options": ["KE = mv", "KE = 1/2 mv²", "KE = mgh", "KE = Fd"],
            "correct_answer": "KE = 1/2 mv²",
            "explanation": "Kinetic energy is the energy of motion, calculated as half the mass times velocity squared.",
            "category": "classical_mechanics"
        },
        {
            "question": "In a game, an object is falling with no air resistance. Which physics principle determines its acceleration?",
            "question_type": "multiple_choice",
            "options": ["Newton's First Law", "Conservation of Momentum", "Gravitational Acceleration (g = 9.8 m/s²)", "Hooke's Law"],
            "correct_answer": "Gravitational Acceleration (g = 9.8 m/s²)",
            "explanation": "Objects in free fall accelerate at approximately 9.8 m/s² due to Earth's gravity.",
            "category": "game_physics"
        },
        {
            "question": "True or False: In an elastic collision, both momentum AND kinetic energy are conserved.",
            "question_type": "true_false",
            "options": ["True", "False"],
            "correct_answer": "True",
            "explanation": "Elastic collisions conserve both momentum and kinetic energy. Inelastic collisions only conserve momentum.",
            "category": "collisions"
        },
        {
            "question": "What will print?\n```python\nvelocity = 10\ndt = 0.016  # 60fps\nacceleration = -9.8\nvelocity += acceleration * dt\nprint(round(velocity, 2))\n```",
            "question_type": "code_output",
            "options": ["9.84", "10.16", "9.98", "10.02"],
            "correct_answer": "9.84",
            "explanation": "velocity = 10 + (-9.8 * 0.016) = 10 - 0.1568 = 9.8432, rounded to 9.84",
            "category": "game_physics"
        }
    ],
    "math": [
        {
            "question": "What is the dot product of vectors (1,2,3) and (4,5,6)?",
            "question_type": "multiple_choice",
            "options": ["32", "21", "15", "27"],
            "correct_answer": "32",
            "explanation": "Dot product = 1*4 + 2*5 + 3*6 = 4 + 10 + 18 = 32",
            "category": "linear_algebra"
        },
        {
            "question": "What does lerp(0, 100, 0.5) return?",
            "question_type": "multiple_choice",
            "options": ["0", "25", "50", "100"],
            "correct_answer": "50",
            "explanation": "Linear interpolation with t=0.5 returns the midpoint. lerp = 0 + (100-0)*0.5 = 50",
            "category": "interpolation"
        },
        {
            "question": "True or False: Quaternions avoid gimbal lock, making them better than Euler angles for 3D rotations.",
            "question_type": "true_false",
            "options": ["True", "False"],
            "correct_answer": "True",
            "explanation": "Quaternions provide smooth interpolation and avoid the gimbal lock problem that affects Euler angles.",
            "category": "rotations"
        }
    ],
    "cs": [
        {
            "question": "What is the time complexity of binary search?",
            "question_type": "multiple_choice",
            "options": ["O(1)", "O(n)", "O(log n)", "O(n²)"],
            "correct_answer": "O(log n)",
            "explanation": "Binary search divides the search space in half each iteration, giving O(log n) complexity.",
            "category": "algorithms"
        },
        {
            "question": "Which data structure is best for implementing a game's entity-component system lookup?",
            "question_type": "multiple_choice",
            "options": ["Array", "Linked List", "Hash Map / Dictionary", "Stack"],
            "correct_answer": "Hash Map / Dictionary",
            "explanation": "Hash maps provide O(1) average lookup time, perfect for quick component access by entity ID.",
            "category": "data_structures"
        },
        {
            "question": "In A* pathfinding, what does f(n) = g(n) + h(n) represent?",
            "question_type": "multiple_choice",
            "options": [
                "f = frames, g = graphics, h = height",
                "f = total cost, g = cost so far, h = estimated cost to goal",
                "f = function, g = global, h = heuristic",
                "f = final, g = given, h = half"
            ],
            "correct_answer": "f = total cost, g = cost so far, h = estimated cost to goal",
            "explanation": "A* uses f(n) as the total estimated cost, combining the known path cost g(n) with the heuristic h(n).",
            "category": "algorithms"
        }
    ]
}

# ============================================================================
# API ENDPOINTS
# ============================================================================

@router.get("/info")
async def get_learning_info():
    """Get learning engine info"""
    return {
        "name": "CodeDock Immersive Learning Engine",
        "version": "11.6.0",
        "description": "Interactive, gamified learning with progress tracking and spaced repetition",
        "features": [
            "Adaptive coding challenges",
            "Interactive quizzes with instant feedback",
            "XP and leveling system",
            "Achievement badges",
            "Learning streaks",
            "Spaced repetition for long-term retention",
            "Personalized learning paths",
            "Real-time code execution",
            "Progress analytics"
        ],
        "total_achievements": len(ACHIEVEMENTS),
        "max_level": len(LEVEL_THRESHOLDS),
        "subjects": ["physics", "math", "cs"]
    }

@router.get("/profile/{user_id}")
async def get_learner_profile(user_id: str):
    """Get or create learner profile"""
    profile = await learning_db.profiles.find_one({"user_id": user_id})
    
    if not profile:
        # Create new profile
        new_profile = {
            "user_id": user_id,
            "display_name": "Learner",
            "xp": 0,
            "level": 1,
            "streak_days": 0,
            "last_active": datetime.utcnow(),
            "total_challenges_completed": 0,
            "total_lessons_completed": 0,
            "total_quizzes_completed": 0,
            "perfect_quizzes": 0,
            "achievements": [],
            "skill_ratings": {"physics": 50, "math": 50, "cs": 50},
            "subjects_studied": [],
            "created_at": datetime.utcnow()
        }
        await learning_db.profiles.insert_one(new_profile)
        profile = new_profile
    else:
        # Check streak
        last_active = profile.get("last_active")
        if last_active:
            days_since = (datetime.utcnow() - last_active).days
            if days_since > 1:
                # Streak broken
                await learning_db.profiles.update_one(
                    {"user_id": user_id},
                    {"$set": {"streak_days": 0}}
                )
                profile["streak_days"] = 0
    
    # Calculate level info
    xp = profile.get("xp", 0)
    level = calculate_level(xp)
    xp_needed = xp_to_next_level(xp)
    
    return {
        **profile,
        "_id": str(profile.get("_id", "")),
        "level": level,
        "xp_to_next_level": xp_needed,
        "current_level_xp": xp - (LEVEL_THRESHOLDS[level-1] if level > 0 else 0),
        "level_total_xp": (LEVEL_THRESHOLDS[level] - LEVEL_THRESHOLDS[level-1]) if level < len(LEVEL_THRESHOLDS) else 0
    }

@router.post("/xp/award")
async def award_xp(
    user_id: str,
    amount: int,
    reason: str = "Activity",
    category: Optional[str] = None
):
    """Award XP to a learner"""
    profile = await learning_db.profiles.find_one({"user_id": user_id})
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    old_xp = profile.get("xp", 0)
    new_xp = old_xp + amount
    old_level = calculate_level(old_xp)
    new_level = calculate_level(new_xp)
    
    # Update profile
    update_data = {
        "xp": new_xp,
        "last_active": datetime.utcnow()
    }
    
    if category:
        # Update skill rating
        skill_key = f"skill_ratings.{category}"
        current_skill = profile.get("skill_ratings", {}).get(category, 50)
        new_skill = min(100, current_skill + (amount // 10))
        update_data[skill_key] = new_skill
        
        # Track subjects studied
        subjects = profile.get("subjects_studied", [])
        if category not in subjects:
            update_data["subjects_studied"] = subjects + [category]
    
    await learning_db.profiles.update_one(
        {"user_id": user_id},
        {"$set": update_data}
    )
    
    # Log XP transaction
    await learning_db.xp_log.insert_one({
        "user_id": user_id,
        "amount": amount,
        "reason": reason,
        "category": category,
        "timestamp": datetime.utcnow()
    })
    
    result = {
        "xp_awarded": amount,
        "new_xp_total": new_xp,
        "level_up": new_level > old_level,
        "old_level": old_level,
        "new_level": new_level
    }
    
    # Check for level achievements
    new_achievements = []
    if new_level >= 5 and "level_5" not in profile.get("achievements", []):
        new_achievements.append("level_5")
    if new_level >= 10 and "level_10" not in profile.get("achievements", []):
        new_achievements.append("level_10")
    if new_level >= 20 and "level_20" not in profile.get("achievements", []):
        new_achievements.append("level_20")
    
    if new_achievements:
        for ach in new_achievements:
            result["new_achievements"] = new_achievements
            bonus_xp = ACHIEVEMENTS[ach]["xp_bonus"]
            await learning_db.profiles.update_one(
                {"user_id": user_id},
                {
                    "$push": {"achievements": ach},
                    "$inc": {"xp": bonus_xp}
                }
            )
    
    return result

@router.get("/challenges/{category}")
async def get_challenges(category: str, difficulty: Optional[str] = None):
    """Get available challenges for a category"""
    if category not in CHALLENGE_TEMPLATES:
        raise HTTPException(status_code=404, detail="Category not found")
    
    challenges = CHALLENGE_TEMPLATES[category]
    if difficulty:
        challenges = [c for c in challenges if c.get("difficulty") == difficulty]
    
    return {
        "category": category,
        "total_challenges": len(challenges),
        "challenges": [
            {
                "challenge_id": f"{category}_{i}",
                "title": c["title"],
                "description": c["description"],
                "difficulty": c["difficulty"],
                "xp_reward": c["xp_reward"]
            }
            for i, c in enumerate(challenges)
        ]
    }

@router.get("/challenge/{category}/{index}")
async def get_challenge_detail(category: str, index: int):
    """Get full challenge details"""
    if category not in CHALLENGE_TEMPLATES:
        raise HTTPException(status_code=404, detail="Category not found")
    
    challenges = CHALLENGE_TEMPLATES[category]
    if index >= len(challenges):
        raise HTTPException(status_code=404, detail="Challenge not found")
    
    challenge = challenges[index]
    return {
        "challenge_id": f"{category}_{index}",
        "category": category,
        **challenge
    }

@router.post("/challenge/submit")
async def submit_challenge(
    user_id: str,
    category: str,
    challenge_index: int,
    code: str,
    time_taken_seconds: int = 0
):
    """Submit a challenge solution for evaluation"""
    if category not in CHALLENGE_TEMPLATES:
        raise HTTPException(status_code=404, detail="Category not found")
    
    challenges = CHALLENGE_TEMPLATES[category]
    if challenge_index >= len(challenges):
        raise HTTPException(status_code=404, detail="Challenge not found")
    
    challenge = challenges[challenge_index]
    
    # Use AI to evaluate the solution
    chat = LlmChat(api_key=EMERGENT_LLM_KEY)
    
    evaluation_prompt = f"""Evaluate this code solution for the following challenge:

Challenge: {challenge['title']}
Description: {challenge['description']}
Expected behavior: The function should work correctly.

Student's Code:
```python
{code}
```

Provide a JSON response with:
1. "passed": true/false - does the code correctly solve the problem?
2. "score": 0-100 - quality score
3. "feedback": specific feedback on the solution
4. "improvements": list of suggested improvements
5. "correct_concepts": list of concepts the student demonstrated correctly

Be encouraging but honest. Return ONLY valid JSON."""
    
    response = await chat.send_async([UserMessage(content=evaluation_prompt)])
    
    try:
        # Try to parse JSON from response
        import re
        json_match = re.search(r'\{[^{}]*\}', response.text, re.DOTALL)
        if json_match:
            evaluation = json.loads(json_match.group())
        else:
            evaluation = {"passed": False, "score": 50, "feedback": response.text, "improvements": []}
    except:
        evaluation = {"passed": False, "score": 50, "feedback": response.text, "improvements": []}
    
    passed = evaluation.get("passed", False)
    score = evaluation.get("score", 50)
    
    # Award XP based on result
    xp_earned = 0
    achievements_earned = []
    
    if passed:
        base_xp = challenge["xp_reward"]
        # Bonus for high score
        score_bonus = int(base_xp * (score / 100) * 0.5)
        xp_earned = base_xp + score_bonus
        
        # Update profile
        await learning_db.profiles.update_one(
            {"user_id": user_id},
            {
                "$inc": {"total_challenges_completed": 1, "xp": xp_earned},
                "$set": {"last_active": datetime.utcnow()}
            }
        )
        
        # Check for first challenge achievement
        profile = await learning_db.profiles.find_one({"user_id": user_id})
        if profile and profile.get("total_challenges_completed", 0) == 1:
            achievements_earned.append("first_steps")
        
        # Speed demon achievement
        if time_taken_seconds > 0 and time_taken_seconds < 60:
            if "speed_demon" not in profile.get("achievements", []):
                achievements_earned.append("speed_demon")
        
        # Award achievement XP
        for ach in achievements_earned:
            await learning_db.profiles.update_one(
                {"user_id": user_id},
                {
                    "$push": {"achievements": ach},
                    "$inc": {"xp": ACHIEVEMENTS[ach]["xp_bonus"]}
                }
            )
            xp_earned += ACHIEVEMENTS[ach]["xp_bonus"]
    
    return {
        "passed": passed,
        "score": score,
        "xp_earned": xp_earned,
        "feedback": evaluation.get("feedback", ""),
        "improvements": evaluation.get("improvements", []),
        "correct_concepts": evaluation.get("correct_concepts", []),
        "achievements_earned": [ACHIEVEMENTS[a] for a in achievements_earned] if achievements_earned else [],
        "challenge_xp": challenge["xp_reward"],
        "hints_available": len(challenge.get("hints", []))
    }

@router.get("/quiz/{category}")
async def get_quiz(category: str, count: int = 5):
    """Get a quiz for a category"""
    if category not in QUIZ_BANK:
        raise HTTPException(status_code=404, detail="Category not found")
    
    questions = QUIZ_BANK[category]
    selected = random.sample(questions, min(count, len(questions)))
    
    # Don't include correct answers in response
    quiz_questions = []
    for i, q in enumerate(selected):
        quiz_questions.append({
            "question_id": f"{category}_q{i}",
            "question": q["question"],
            "question_type": q["question_type"],
            "options": q["options"],
            "category": q["category"],
            "xp_reward": 10
        })
    
    return {
        "quiz_id": f"quiz_{category}_{uuid.uuid4().hex[:8]}",
        "category": category,
        "total_questions": len(quiz_questions),
        "total_xp": len(quiz_questions) * 10,
        "questions": quiz_questions
    }

@router.post("/quiz/submit")
async def submit_quiz(
    user_id: str,
    category: str,
    answers: List[Dict[str, str]]  # [{"question_index": 0, "answer": "..."}]
):
    """Submit quiz answers for grading"""
    if category not in QUIZ_BANK:
        raise HTTPException(status_code=404, detail="Category not found")
    
    questions = QUIZ_BANK[category]
    correct = 0
    total = len(answers)
    results = []
    
    for ans in answers:
        q_idx = ans.get("question_index", 0)
        if q_idx < len(questions):
            q = questions[q_idx]
            is_correct = ans.get("answer") == q["correct_answer"]
            if is_correct:
                correct += 1
            results.append({
                "question": q["question"][:50] + "...",
                "your_answer": ans.get("answer"),
                "correct_answer": q["correct_answer"],
                "is_correct": is_correct,
                "explanation": q["explanation"]
            })
    
    score_percent = (correct / total * 100) if total > 0 else 0
    xp_earned = correct * 10
    
    # Perfect quiz bonus
    perfect = correct == total and total > 0
    if perfect:
        xp_earned += 25  # Bonus for perfect score
    
    # Update profile
    update_data = {
        "$inc": {
            "total_quizzes_completed": 1,
            "xp": xp_earned
        },
        "$set": {"last_active": datetime.utcnow()}
    }
    if perfect:
        update_data["$inc"]["perfect_quizzes"] = 1
    
    await learning_db.profiles.update_one(
        {"user_id": user_id},
        update_data
    )
    
    # Check for quiz ace achievement
    achievements = []
    profile = await learning_db.profiles.find_one({"user_id": user_id})
    if profile and profile.get("perfect_quizzes", 0) >= 5:
        if "quiz_ace" not in profile.get("achievements", []):
            achievements.append("quiz_ace")
            await learning_db.profiles.update_one(
                {"user_id": user_id},
                {
                    "$push": {"achievements": "quiz_ace"},
                    "$inc": {"xp": ACHIEVEMENTS["quiz_ace"]["xp_bonus"]}
                }
            )
    
    return {
        "correct": correct,
        "total": total,
        "score_percent": round(score_percent, 1),
        "xp_earned": xp_earned,
        "perfect_score": perfect,
        "results": results,
        "achievements_earned": achievements,
        "encouragement": (
            "Perfect score! You're amazing!" if perfect else
            "Great job! Keep learning!" if score_percent >= 70 else
            "Good effort! Review the explanations to improve." if score_percent >= 50 else
            "Keep practicing! Every attempt makes you stronger."
        )
    }

@router.get("/achievements")
async def get_all_achievements():
    """Get all available achievements"""
    return {
        "total": len(ACHIEVEMENTS),
        "achievements": [
            {
                "id": ach_id,
                **ach_data
            }
            for ach_id, ach_data in ACHIEVEMENTS.items()
        ]
    }

@router.get("/streak/{user_id}")
async def update_streak(user_id: str):
    """Update and get learning streak"""
    profile = await learning_db.profiles.find_one({"user_id": user_id})
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    last_active = profile.get("last_active")
    current_streak = profile.get("streak_days", 0)
    
    if last_active:
        days_since = (datetime.utcnow() - last_active).days
        if days_since == 0:
            # Already active today
            pass
        elif days_since == 1:
            # Continue streak
            current_streak += 1
            await learning_db.profiles.update_one(
                {"user_id": user_id},
                {
                    "$set": {"streak_days": current_streak, "last_active": datetime.utcnow()}
                }
            )
            
            # Check streak achievements
            achievements = []
            if current_streak >= 3 and "streak_3" not in profile.get("achievements", []):
                achievements.append("streak_3")
            if current_streak >= 7 and "streak_7" not in profile.get("achievements", []):
                achievements.append("streak_7")
            if current_streak >= 30 and "streak_30" not in profile.get("achievements", []):
                achievements.append("streak_30")
            
            for ach in achievements:
                await learning_db.profiles.update_one(
                    {"user_id": user_id},
                    {
                        "$push": {"achievements": ach},
                        "$inc": {"xp": ACHIEVEMENTS[ach]["xp_bonus"]}
                    }
                )
        else:
            # Streak broken
            current_streak = 1
            await learning_db.profiles.update_one(
                {"user_id": user_id},
                {
                    "$set": {"streak_days": 1, "last_active": datetime.utcnow()}
                }
            )
    else:
        # First activity
        current_streak = 1
        await learning_db.profiles.update_one(
            {"user_id": user_id},
            {
                "$set": {"streak_days": 1, "last_active": datetime.utcnow()}
            }
        )
    
    return {
        "streak_days": current_streak,
        "message": f"{current_streak} day streak!" if current_streak > 1 else "Start of a new streak!",
        "next_milestone": (
            3 if current_streak < 3 else
            7 if current_streak < 7 else
            30 if current_streak < 30 else
            current_streak + 1
        )
    }

@router.get("/leaderboard")
async def get_leaderboard(limit: int = 10):
    """Get XP leaderboard"""
    cursor = learning_db.profiles.find(
        {},
        {"user_id": 1, "display_name": 1, "xp": 1, "streak_days": 1, "achievements": 1}
    ).sort("xp", -1).limit(limit)
    
    leaders = []
    async for profile in cursor:
        leaders.append({
            "rank": len(leaders) + 1,
            "user_id": profile["user_id"],
            "display_name": profile.get("display_name", "Learner"),
            "xp": profile.get("xp", 0),
            "level": calculate_level(profile.get("xp", 0)),
            "streak_days": profile.get("streak_days", 0),
            "achievement_count": len(profile.get("achievements", []))
        })
    
    return {
        "leaderboard": leaders,
        "updated_at": datetime.utcnow().isoformat()
    }

@router.get("/daily-challenge")
async def get_daily_challenge():
    """Get the daily challenge"""
    # Use date as seed for consistent daily challenge
    today = datetime.utcnow().strftime("%Y%m%d")
    random.seed(int(today))
    
    # Pick random category and challenge
    category = random.choice(list(CHALLENGE_TEMPLATES.keys()))
    challenges = CHALLENGE_TEMPLATES[category]
    challenge = random.choice(challenges)
    
    random.seed()  # Reset seed
    
    return {
        "daily_challenge_id": f"daily_{today}",
        "category": category,
        "title": challenge["title"],
        "description": challenge["description"],
        "difficulty": challenge["difficulty"],
        "xp_reward": challenge["xp_reward"] * 2,  # Double XP for daily
        "bonus": "2x XP for daily challenge!",
        "starter_code": challenge.get("starter_code"),
        "expires_at": (datetime.utcnow().replace(hour=23, minute=59, second=59)).isoformat()
    }

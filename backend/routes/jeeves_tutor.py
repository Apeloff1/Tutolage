"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    JEEVES - AI CODE BUTLER v11.0.0                            ║
║                                                                               ║
║  Your Personal AI Coding Tutor & Assistant                                    ║
║  - Personalized teaching style                                                ║
║  - Adaptive difficulty                                                        ║
║  - Context-aware assistance                                                   ║
║  - Code explanation at your level                                             ║
║  - Debugging companion                                                        ║
║  - Best practices mentor                                                      ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any, Literal
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
import uuid
import os

# Load environment
ROOT_DIR = Path(__file__).parent.parent
load_dotenv(ROOT_DIR / '.env')

from emergentintegrations.llm.chat import LlmChat, UserMessage

router = APIRouter(prefix="/jeeves", tags=["Jeeves AI Tutor"])

EMERGENT_LLM_KEY = os.environ.get('EMERGENT_LLM_KEY', '')

# ============================================================================
# DATA MODELS
# ============================================================================

class JeevesRequest(BaseModel):
    message: str = Field(..., min_length=1, description="Your question or request")
    context: Optional[str] = Field(None, description="Code or context")
    skill_level: Literal["beginner", "intermediate", "advanced", "expert"] = "intermediate"
    language: str = "python"
    personality: Literal["formal", "friendly", "encouraging", "concise"] = "friendly"
    session_id: Optional[str] = None

class ExplainRequest(BaseModel):
    code: str = Field(..., min_length=1)
    language: str = "python"
    depth: Literal["eli5", "beginner", "detailed", "expert"] = "beginner"
    focus: Optional[str] = Field(None, description="Specific aspect to focus on")

class DebugHelpRequest(BaseModel):
    code: str = Field(..., min_length=1)
    error: Optional[str] = None
    expected_behavior: Optional[str] = None
    language: str = "python"
    skill_level: str = "intermediate"

class ConceptRequest(BaseModel):
    concept: str = Field(..., min_length=2, description="Programming concept to learn")
    context: Optional[str] = Field(None, description="What you're trying to build")
    skill_level: str = "intermediate"
    include_examples: bool = True
    language: str = "python"

class PracticeRequest(BaseModel):
    topic: str
    difficulty: Literal["easy", "medium", "hard"] = "medium"
    language: str = "python"
    count: int = Field(3, ge=1, le=10)

# ============================================================================
# JEEVES PERSONALITY SYSTEM
# ============================================================================

JEEVES_PERSONALITIES = {
    "formal": """You are Jeeves, a distinguished AI code butler with impeccable manners.
Speak formally but warmly, like a trusted family butler.
Use phrases like "Very good, sir/madam", "If I may suggest", "Indeed".
Be precise, professional, and thorough in your explanations.""",
    
    "friendly": """You are Jeeves, a friendly and approachable AI coding buddy.
Be warm, encouraging, and conversational.
Use casual language but remain helpful and accurate.
Celebrate successes and be supportive during struggles.""",
    
    "encouraging": """You are Jeeves, an enthusiastic and motivating AI coding coach.
Be extremely positive and encouraging.
Celebrate every small win. Turn mistakes into learning opportunities.
Use phrases like "Great question!", "You've got this!", "Let's figure this out together!".""",
    
    "concise": """You are Jeeves, a no-nonsense AI coding assistant.
Be direct and to the point. Minimize fluff.
Give clear, actionable answers quickly.
Only elaborate when specifically asked."""
}

SKILL_LEVEL_CONTEXT = {
    "beginner": "Explain everything simply. Avoid jargon. Use lots of analogies. Don't assume prior knowledge.",
    "intermediate": "Balance explanation with efficiency. Assume basic programming knowledge. Introduce intermediate concepts.",
    "advanced": "Be technical and precise. Discuss trade-offs, edge cases, and optimizations. Assume strong fundamentals.",
    "expert": "Peer-level discussion. Focus on nuances, advanced patterns, performance implications, and cutting-edge practices."
}

# ============================================================================
# AI HELPER
# ============================================================================

async def call_jeeves(prompt: str, personality: str, skill_level: str, session_id: str = None) -> str:
    try:
        system = f"""{JEEVES_PERSONALITIES.get(personality, JEEVES_PERSONALITIES['friendly'])}

{SKILL_LEVEL_CONTEXT.get(skill_level, SKILL_LEVEL_CONTEXT['intermediate'])}

You help with:
- Explaining code and concepts
- Debugging issues
- Teaching best practices
- Suggesting improvements
- Answering programming questions
- Providing encouragement and motivation

Always be helpful, accurate, and adapt to the user's level."""

        chat = LlmChat(
            api_key=EMERGENT_LLM_KEY,
            session_id=session_id or f"jeeves-{uuid.uuid4().hex[:8]}",
            system_message=system
        ).with_model("openai", "gpt-4o")
        
        response = await chat.send_message(UserMessage(text=prompt))
        return response.content if hasattr(response, 'content') else str(response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Jeeves encountered an issue: {str(e)}")

# ============================================================================
# JEEVES ENDPOINTS
# ============================================================================

@router.get("/info")
async def get_jeeves_info():
    """Meet Jeeves, your AI Code Butler"""
    return {
        "name": "Jeeves",
        "title": "AI Code Butler & Personal Tutor",
        "version": "11.0.0",
        "tagline": "At your service, ready to assist with all your coding needs.",
        "capabilities": [
            "Code explanation at any level",
            "Debugging assistance",
            "Concept teaching",
            "Best practices guidance",
            "Code review",
            "Practice problem generation",
            "Learning path suggestions",
            "Motivation and encouragement"
        ],
        "personalities": {
            "formal": "Distinguished and precise, like a traditional butler",
            "friendly": "Warm and approachable coding buddy",
            "encouraging": "Enthusiastic coach who celebrates your wins",
            "concise": "Direct and efficient, minimal fluff"
        },
        "skill_levels": ["beginner", "intermediate", "advanced", "expert"],
        "languages_fluent": [
            "Python", "JavaScript", "TypeScript", "Java", "C++", "C",
            "Rust", "Go", "Swift", "Kotlin", "Ruby", "PHP", "C#"
        ],
        "specialties": [
            "Data Structures & Algorithms",
            "Object-Oriented Programming",
            "Functional Programming",
            "Web Development",
            "Mobile Development",
            "Database Design",
            "System Design",
            "Testing & QA"
        ]
    }

@router.post("/ask")
async def ask_jeeves(request: JeevesRequest):
    """Ask Jeeves anything about coding"""
    request_id = str(uuid.uuid4())
    
    prompt = f"""User's question: {request.message}

{f'Code/Context:{chr(10)}```{request.language}{chr(10)}{request.context}{chr(10)}```' if request.context else ''}

Language focus: {request.language}

Please help with this query. Remember to adapt your response to a {request.skill_level} level developer."""

    try:
        response = await call_jeeves(prompt, request.personality, request.skill_level, request.session_id)
        
        return {
            "id": request_id,
            "jeeves_response": response,
            "session_id": request.session_id or f"jeeves-{request_id[:8]}",
            "personality": request.personality,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/explain")
async def explain_code(request: ExplainRequest):
    """Have Jeeves explain code in detail"""
    request_id = str(uuid.uuid4())
    
    depth_instructions = {
        "eli5": "Explain like I'm 5 years old. Use simple analogies, no jargon.",
        "beginner": "Explain for someone new to programming. Define terms, be thorough.",
        "detailed": "Comprehensive technical explanation with all details.",
        "expert": "Expert-level analysis: patterns, trade-offs, optimizations, edge cases."
    }
    
    prompt = f"""Please explain this {request.language} code:

```{request.language}
{request.code}
```

{depth_instructions[request.depth]}

{f'Focus specifically on: {request.focus}' if request.focus else ''}

Provide:
1. **Overview** - What does this code do?
2. **Line-by-Line** - Walk through key parts
3. **Key Concepts** - What programming concepts are used?
4. **Potential Issues** - Any bugs or improvements?
5. **Learning Points** - What can be learned from this code?"""

    try:
        response = await call_jeeves(prompt, "friendly", 
                                       "beginner" if request.depth in ["eli5", "beginner"] else "advanced")
        
        return {
            "id": request_id,
            "explanation": response,
            "depth": request.depth,
            "language": request.language,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/debug-help")
async def debug_help(request: DebugHelpRequest):
    """Get Jeeves' help debugging code"""
    request_id = str(uuid.uuid4())
    
    prompt = f"""I need help debugging this {request.language} code:

```{request.language}
{request.code}
```

{f'**Error Message:**{chr(10)}{request.error}' if request.error else ''}
{f'**Expected Behavior:** {request.expected_behavior}' if request.expected_behavior else ''}

Please help me understand:
1. What's wrong with the code?
2. Why is it happening?
3. How do I fix it?
4. How do I prevent this in the future?

Give me the fixed code and explain the changes.
Be supportive - debugging is hard!"""

    try:
        response = await call_jeeves(prompt, "encouraging", request.skill_level)
        
        return {
            "id": request_id,
            "debug_assistance": response,
            "language": request.language,
            "had_error": bool(request.error),
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/teach-concept")
async def teach_concept(request: ConceptRequest):
    """Have Jeeves teach you a programming concept"""
    request_id = str(uuid.uuid4())
    
    prompt = f"""Teach me about: **{request.concept}**

Language: {request.language}
My level: {request.skill_level}
{f'I want to use this for: {request.context}' if request.context else ''}

Please provide:
1. **What is it?** - Clear definition
2. **Why use it?** - Benefits and use cases
3. **How does it work?** - Explanation of the mechanics
{'4. **Code Examples** - Practical examples with comments' if request.include_examples else ''}
5. **Common Mistakes** - What to avoid
6. **Best Practices** - How to use it well
7. **Related Concepts** - What to learn next
8. **Practice Exercise** - A small challenge to try

Make it engaging and memorable!"""

    try:
        response = await call_jeeves(prompt, "encouraging", request.skill_level)
        
        return {
            "id": request_id,
            "lesson": response,
            "concept": request.concept,
            "language": request.language,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/practice")
async def generate_practice(request: PracticeRequest):
    """Get practice problems from Jeeves"""
    request_id = str(uuid.uuid4())
    
    prompt = f"""Generate {request.count} {request.difficulty} practice problems about {request.topic} in {request.language}.

For each problem provide:
1. **Problem Title**
2. **Description** - Clear problem statement
3. **Examples** - Input/output examples
4. **Constraints** - Any limitations
5. **Hints** - Progressive hints (don't give away solution)
6. **Starter Code** - Template to begin with
7. **Solution** (hidden) - Correct solution
8. **Explanation** - Why the solution works

Make problems:
- Practical and applicable
- Progressively challenging
- Fun and engaging
- Teaching real skills"""

    try:
        response = await call_jeeves(prompt, "encouraging", 
                                       "intermediate" if request.difficulty == "medium" else 
                                       "beginner" if request.difficulty == "easy" else "advanced")
        
        return {
            "id": request_id,
            "practice_problems": response,
            "topic": request.topic,
            "difficulty": request.difficulty,
            "count": request.count,
            "language": request.language,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/motivate")
async def get_motivation(mood: str = "stuck", context: Optional[str] = None):
    """Get encouragement from Jeeves when you need it"""
    request_id = str(uuid.uuid4())
    
    mood_prompts = {
        "stuck": "The developer is stuck on a problem and feeling frustrated.",
        "imposter": "The developer is experiencing imposter syndrome.",
        "overwhelmed": "The developer is overwhelmed by how much there is to learn.",
        "failed": "The developer's code failed and they're feeling down.",
        "bored": "The developer is bored and losing motivation.",
        "excited": "The developer is excited about a success - celebrate with them!"
    }
    
    prompt = f"""{mood_prompts.get(mood, mood_prompts['stuck'])}

{f'Context: {context}' if context else ''}

Give them a warm, genuine, encouraging message. Include:
1. Acknowledgment of their feelings
2. Perspective (this is normal/temporary)
3. A specific actionable suggestion
4. An inspiring quote or story about famous programmers who faced similar challenges
5. A reminder of how far they've come

Be genuinely supportive, not generic or preachy."""

    try:
        response = await call_jeeves(prompt, "encouraging", "intermediate")
        
        return {
            "id": request_id,
            "message": response,
            "mood": mood,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/tip-of-the-day")
async def tip_of_the_day(language: str = "python", level: str = "intermediate"):
    """Get Jeeves' tip of the day"""
    import hashlib
    today = datetime.utcnow().strftime("%Y-%m-%d")
    seed = hashlib.md5(f"{today}-{language}-{level}".encode()).hexdigest()
    
    prompt = f"""Give me one excellent {language} tip for a {level} developer.

The tip should be:
- Practical and immediately useful
- Not too basic, not too obscure
- Include a code example
- Explain why it's useful

Format:
**💡 Tip of the Day**
[The tip]

**Example:**
```{language}
[code example]
```

**Why it matters:**
[explanation]

Seed for variety: {seed}"""

    try:
        response = await call_jeeves(prompt, "friendly", level)
        
        return {
            "date": today,
            "tip": response,
            "language": language,
            "level": level
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

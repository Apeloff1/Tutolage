"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                      CURRICULUM ENGINE v11.0.0                                ║
║                                                                               ║
║  Complete Learning Management System:                                         ║
║  • Course progression tracking                                                ║
║  • Prerequisites management                                                   ║
║  • Quizzes & assessments                                                     ║
║  • Completion certificates                                                   ║
║  • Learning analytics                                                        ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum
import uuid

# Import CS Classes
from cs_classes import get_class, get_all_classes, get_class_summary

router = APIRouter(prefix="/curriculum", tags=["Curriculum Engine"])

# ============================================================================
# MODELS
# ============================================================================

class ProgressStatus(str, Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class CourseProgress(BaseModel):
    course_id: str
    user_id: str
    status: ProgressStatus = ProgressStatus.NOT_STARTED
    current_week: int = 0
    completed_weeks: List[int] = []
    quiz_scores: Dict[int, float] = {}
    assignments_completed: List[str] = []
    started_at: Optional[str] = None
    last_activity: Optional[str] = None
    completion_percentage: float = 0.0

class QuizSubmission(BaseModel):
    course_id: str
    week: int
    answers: List[Dict[str, Any]]

class CertificateRequest(BaseModel):
    course_id: str
    user_id: str

# ============================================================================
# IN-MEMORY STORAGE (Would be MongoDB in production)
# ============================================================================

user_progress: Dict[str, Dict[str, CourseProgress]] = {}
certificates: Dict[str, List[Dict]] = {}

# ============================================================================
# CURRICULUM ENDPOINTS
# ============================================================================

@router.get("/info")
async def get_curriculum_info():
    """Get curriculum engine information"""
    class_summary = get_class_summary()
    return {
        "name": "CodeDock Curriculum Engine",
        "version": "11.0.0",
        "total_classes": class_summary["total_classes"],
        "total_hours": class_summary["total_hours"],
        "features": [
            "Course progression tracking",
            "Prerequisites management",
            "Interactive quizzes",
            "Code exercises with auto-grading",
            "Completion certificates",
            "Learning analytics",
            "Personalized recommendations",
            "Spaced repetition review"
        ],
        "available_classes": class_summary["classes"]
    }

@router.get("/classes")
async def list_all_classes():
    """Get all available CS classes"""
    classes = get_all_classes()
    return {
        "total": len(classes),
        "classes": [
            {
                "id": c["id"],
                "code": c["code"],
                "title": c["title"],
                "subtitle": c["subtitle"],
                "hours": c["hours"],
                "weeks": c["weeks"] if isinstance(c["weeks"], int) else len(c["weeks"]),
                "level": c["level"],
                "prerequisites": c["prerequisites"]
            }
            for c in classes
        ]
    }

@router.get("/classes/{class_id}")
async def get_class_details(class_id: str):
    """Get detailed information about a specific class"""
    class_data = get_class(class_id)
    if not class_data:
        raise HTTPException(status_code=404, detail=f"Class '{class_id}' not found")
    return class_data

@router.get("/classes/{class_id}/week/{week_num}")
async def get_class_week(class_id: str, week_num: int):
    """Get content for a specific week of a class"""
    class_data = get_class(class_id)
    if not class_data:
        raise HTTPException(status_code=404, detail=f"Class '{class_id}' not found")
    
    weeks = class_data.get("weeks", [])
    if isinstance(weeks, list):
        for week in weeks:
            if isinstance(week, dict) and week.get("week") == week_num:
                return week
    
    weeks_summary = class_data.get("weeks_summary", [])
    for week in weeks_summary:
        if week.get("week") == week_num:
            return week
    
    raise HTTPException(status_code=404, detail=f"Week {week_num} not found")

@router.get("/classes/{class_id}/code-examples")
async def get_class_code_examples(class_id: str):
    """Get all code examples from a class"""
    class_data = get_class(class_id)
    if not class_data:
        raise HTTPException(status_code=404, detail=f"Class '{class_id}' not found")
    
    examples = []
    weeks = class_data.get("weeks", [])
    
    if isinstance(weeks, list):
        for week in weeks:
            if isinstance(week, dict) and "code_examples" in week:
                for example in week["code_examples"]:
                    examples.append({
                        "week": week.get("week"),
                        "week_title": week.get("title"),
                        **example
                    })
    
    return {
        "class_id": class_id,
        "total_examples": len(examples),
        "examples": examples
    }

# ============================================================================
# PROGRESS TRACKING
# ============================================================================

@router.post("/progress/start")
async def start_course(course_id: str, user_id: str = "default_user"):
    """Start a course and begin tracking progress"""
    class_data = get_class(course_id)
    if not class_data:
        raise HTTPException(status_code=404, detail=f"Class '{course_id}' not found")
    
    if user_id not in user_progress:
        user_progress[user_id] = {}
    
    if course_id not in user_progress[user_id]:
        user_progress[user_id][course_id] = CourseProgress(
            course_id=course_id,
            user_id=user_id,
            status=ProgressStatus.IN_PROGRESS,
            current_week=1,
            started_at=datetime.utcnow().isoformat(),
            last_activity=datetime.utcnow().isoformat()
        )
    
    return {
        "status": "started",
        "course_id": course_id,
        "progress": user_progress[user_id][course_id].dict()
    }

@router.get("/progress/{course_id}")
async def get_course_progress(course_id: str, user_id: str = "default_user"):
    """Get progress for a specific course"""
    if user_id in user_progress and course_id in user_progress[user_id]:
        return user_progress[user_id][course_id].dict()
    
    return CourseProgress(
        course_id=course_id,
        user_id=user_id
    ).dict()

@router.post("/progress/{course_id}/complete-week")
async def complete_week(course_id: str, week: int, user_id: str = "default_user"):
    """Mark a week as completed"""
    if user_id not in user_progress or course_id not in user_progress[user_id]:
        raise HTTPException(status_code=400, detail="Course not started")
    
    progress = user_progress[user_id][course_id]
    
    if week not in progress.completed_weeks:
        progress.completed_weeks.append(week)
        progress.completed_weeks.sort()
    
    progress.current_week = max(progress.current_week, week + 1)
    progress.last_activity = datetime.utcnow().isoformat()
    
    # Calculate completion percentage
    class_data = get_class(course_id)
    total_weeks = class_data.get("weeks", 15)
    if isinstance(total_weeks, list):
        total_weeks = len(total_weeks)
    
    progress.completion_percentage = (len(progress.completed_weeks) / total_weeks) * 100
    
    # Check if course is complete
    if progress.completion_percentage >= 100:
        progress.status = ProgressStatus.COMPLETED
    
    return {
        "status": "week_completed",
        "week": week,
        "progress": progress.dict()
    }

@router.post("/progress/{course_id}/quiz")
async def submit_quiz(course_id: str, submission: QuizSubmission, user_id: str = "default_user"):
    """Submit a quiz and receive score"""
    if user_id not in user_progress or course_id not in user_progress[user_id]:
        raise HTTPException(status_code=400, detail="Course not started")
    
    progress = user_progress[user_id][course_id]
    
    # Simulate quiz grading (would be more sophisticated in production)
    correct = sum(1 for a in submission.answers if a.get("correct", False))
    total = len(submission.answers)
    score = (correct / total * 100) if total > 0 else 0
    
    progress.quiz_scores[submission.week] = score
    progress.last_activity = datetime.utcnow().isoformat()
    
    return {
        "status": "quiz_submitted",
        "week": submission.week,
        "score": score,
        "correct": correct,
        "total": total,
        "passed": score >= 70
    }

@router.get("/progress/all")
async def get_all_progress(user_id: str = "default_user"):
    """Get progress for all courses"""
    if user_id not in user_progress:
        return {"user_id": user_id, "courses": []}
    
    return {
        "user_id": user_id,
        "courses": [p.dict() for p in user_progress[user_id].values()]
    }

# ============================================================================
# CERTIFICATES
# ============================================================================

@router.post("/certificate/generate")
async def generate_certificate(request: CertificateRequest):
    """Generate completion certificate"""
    user_id = request.user_id
    course_id = request.course_id
    
    # Verify course completion
    if user_id not in user_progress or course_id not in user_progress[user_id]:
        raise HTTPException(status_code=400, detail="Course not found in progress")
    
    progress = user_progress[user_id][course_id]
    
    if progress.status != ProgressStatus.COMPLETED:
        raise HTTPException(status_code=400, detail="Course not yet completed")
    
    # Get class info
    class_data = get_class(course_id)
    
    # Generate certificate
    cert_id = str(uuid.uuid4())
    certificate = {
        "certificate_id": cert_id,
        "user_id": user_id,
        "course_id": course_id,
        "course_title": class_data["title"],
        "course_code": class_data["code"],
        "hours": class_data["hours"],
        "issued_at": datetime.utcnow().isoformat(),
        "average_quiz_score": sum(progress.quiz_scores.values()) / len(progress.quiz_scores) if progress.quiz_scores else 0,
        "verification_url": f"/api/curriculum/certificate/verify/{cert_id}"
    }
    
    # Store certificate
    if user_id not in certificates:
        certificates[user_id] = []
    certificates[user_id].append(certificate)
    
    return certificate

@router.get("/certificate/verify/{cert_id}")
async def verify_certificate(cert_id: str):
    """Verify a certificate"""
    for user_certs in certificates.values():
        for cert in user_certs:
            if cert["certificate_id"] == cert_id:
                return {"valid": True, "certificate": cert}
    
    return {"valid": False, "message": "Certificate not found"}

@router.get("/certificates")
async def get_user_certificates(user_id: str = "default_user"):
    """Get all certificates for a user"""
    if user_id not in certificates:
        return {"user_id": user_id, "certificates": []}
    
    return {
        "user_id": user_id,
        "certificates": certificates[user_id]
    }

# ============================================================================
# LEARNING ANALYTICS
# ============================================================================

@router.get("/analytics")
async def get_learning_analytics(user_id: str = "default_user"):
    """Get learning analytics for a user"""
    if user_id not in user_progress:
        return {
            "user_id": user_id,
            "total_courses_started": 0,
            "total_courses_completed": 0,
            "total_hours_studied": 0,
            "average_quiz_score": 0,
            "learning_streak": 0
        }
    
    courses = user_progress[user_id]
    completed = [p for p in courses.values() if p.status == ProgressStatus.COMPLETED]
    
    all_quiz_scores = []
    for p in courses.values():
        all_quiz_scores.extend(p.quiz_scores.values())
    
    total_hours = sum(
        get_class(p.course_id)["hours"] * (p.completion_percentage / 100)
        for p in courses.values()
        if get_class(p.course_id)
    )
    
    return {
        "user_id": user_id,
        "total_courses_started": len(courses),
        "total_courses_completed": len(completed),
        "total_hours_studied": round(total_hours, 1),
        "average_quiz_score": round(sum(all_quiz_scores) / len(all_quiz_scores), 1) if all_quiz_scores else 0,
        "certificates_earned": len(certificates.get(user_id, [])),
        "skills_acquired": [
            "Data Structures",
            "Algorithms",
            "Object-Oriented Programming",
            "Database Design",
            "SQL",
            "System Design"
        ] if completed else []
    }

# ============================================================================
# RECOMMENDATIONS
# ============================================================================

@router.get("/recommendations")
async def get_recommendations(user_id: str = "default_user"):
    """Get personalized course recommendations"""
    completed_ids = []
    in_progress_ids = []
    
    if user_id in user_progress:
        for course_id, progress in user_progress[user_id].items():
            if progress.status == ProgressStatus.COMPLETED:
                completed_ids.append(course_id)
            elif progress.status == ProgressStatus.IN_PROGRESS:
                in_progress_ids.append(course_id)
    
    all_classes = get_all_classes()
    recommendations = []
    
    for cls in all_classes:
        if cls["id"] not in completed_ids and cls["id"] not in in_progress_ids:
            # Check prerequisites
            prereqs_met = all(
                prereq in completed_ids
                for prereq in cls.get("prerequisites", [])
            )
            
            if prereqs_met or not cls.get("prerequisites"):
                recommendations.append({
                    "course_id": cls["id"],
                    "title": cls["title"],
                    "reason": "Based on your progress" if completed_ids else "Great starting point",
                    "estimated_hours": cls["hours"]
                })
    
    return {
        "user_id": user_id,
        "recommendations": recommendations[:5]
    }

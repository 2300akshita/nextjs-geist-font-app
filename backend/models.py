from pydantic import BaseModel, Field, validator
from typing import List, Optional
from config import (
    MIN_LESSONS_PER_MODULE,
    MAX_LESSONS_PER_MODULE,
    MIN_QUIZZES,
    MAX_QUIZZES,
    QUIZ_OPTIONS_COUNT,
    ERROR_MESSAGES
)

class Lesson(BaseModel):
    """Model for a lesson within a module."""
    title: str = Field(..., min_length=3)
    explanation: str = Field(..., min_length=10)
    content: str = Field(..., min_length=10)
    coding_task: Optional[str] = Field(None, min_length=10)
    key_takeaway: Optional[str] = Field(None, min_length=10)

    @validator('explanation')
    def validate_explanation_length(cls, v):
        lines = v.split('\n')
        if not (5 <= len(lines) <= 10):
            raise ValueError(ERROR_MESSAGES["explanation_length"])
        return v

class Module(BaseModel):
    """Model for a course module."""
    name: str = Field(..., min_length=3)
    lessons: List[Lesson]

    @validator('lessons')
    def validate_lessons_count(cls, v):
        if not (MIN_LESSONS_PER_MODULE <= len(v) <= MAX_LESSONS_PER_MODULE):
            raise ValueError(
                f"Module must have between {MIN_LESSONS_PER_MODULE} and {MAX_LESSONS_PER_MODULE} lessons"
            )
        return v

class Quiz(BaseModel):
    """Model for a quiz question."""
    question: str = Field(..., min_length=10)
    options: List[str] = Field(..., min_items=QUIZ_OPTIONS_COUNT, max_items=QUIZ_OPTIONS_COUNT)
    correct_answer: str

    @validator('correct_answer')
    def validate_correct_answer(cls, v, values):
        if 'options' in values and v not in values['options']:
            raise ValueError("Correct answer must be one of the options")
        return v

    @validator('options')
    def validate_options(cls, v):
        if len(set(v)) != len(v):
            raise ValueError("Quiz options must be unique")
        if any(not option.strip() for option in v):
            raise ValueError("Quiz options cannot be empty")
        return v

class CourseResponse(BaseModel):
    """Model for the complete course response."""
    topic: str = Field(..., min_length=2)
    level: str = Field(..., regex='^(beginner|intermediate|advanced)$')
    days: int = Field(..., ge=1, le=30)
    modules: List[Module]
    tasks: List[str] = Field(..., min_items=1)
    quizzes: List[Quiz]
    practice_plan: List[str] = Field(..., min_items=3)

    @validator('modules')
    def validate_modules(cls, v):
        if not v:
            raise ValueError(ERROR_MESSAGES["no_modules"])
        return v

    @validator('quizzes')
    def validate_quizzes_count(cls, v):
        if not (MIN_QUIZZES <= len(v) <= MAX_QUIZZES):
            raise ValueError(
                f"Course must have between {MIN_QUIZZES} and {MAX_QUIZZES} quizzes"
            )
        return v

    @validator('tasks')
    def validate_tasks(cls, v, values):
        if 'days' in values and len(v) < values['days']:
            raise ValueError("Must have at least one task per day")
        return v

    @validator('practice_plan')
    def validate_practice_plan(cls, v):
        required_prefixes = ['Daily:', 'Weekly:', 'Monthly:']
        if not all(any(plan.startswith(prefix) for prefix in required_prefixes) for plan in v):
            raise ValueError(
                "Practice plan must include daily, weekly, and monthly activities"
            )
        return v

    class Config:
        """Pydantic model configuration."""
        json_encoders = {
            # Add custom JSON encoders if needed
        }
        schema_extra = {
            "example": {
                "topic": "Python Programming",
                "level": "beginner",
                "days": 7,
                "modules": [
                    {
                        "name": "Introduction to Python",
                        "lessons": [
                            {
                                "title": "Getting Started with Python",
                                "explanation": "Python is a high-level programming language...\n" * 5,
                                "content": "Basic Python syntax and data types",
                                "coding_task": "Write a simple Python program",
                                "key_takeaway": "Python basics and environment setup"
                            }
                        ]
                    }
                ],
                "tasks": [
                    "Day 1: Set up Python environment",
                    "Day 2: Practice basic syntax"
                ],
                "quizzes": [
                    {
                        "question": "What is Python?",
                        "options": [
                            "A programming language",
                            "A snake",
                            "A text editor",
                            "An operating system"
                        ],
                        "correct_answer": "A programming language"
                    }
                ],
                "practice_plan": [
                    "Daily: Code for 1 hour",
                    "Weekly: Complete one project",
                    "Monthly: Review and refactor code"
                ]
            }
        }

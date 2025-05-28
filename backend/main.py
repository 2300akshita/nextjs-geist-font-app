from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from pydantic import BaseModel
from typing import List, Optional
from loguru import logger

app = FastAPI(default_response_class=ORJSONResponse)  # Set ORJSONResponse as default

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080", "http://0.0.0.0:8080", "http://127.0.0.1:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

class Lesson(BaseModel):
    title: str
    content: str

class Module(BaseModel):
    name: str
    lessons: List[Lesson]

class Quiz(BaseModel):
    question: str
    options: List[str]
    correct_answer: str

class CourseResponse(BaseModel):
    topic: str
    level: str
    days: int
    modules: List[Module]
    tasks: List[str]
    quizzes: List[Quiz]
    practice_plan: List[str]

    class Config:
        json_encoders = {
            # Add custom encoders if needed
        }
        schema_extra = {
            "example": {
                "topic": "Test Topic",
                "level": "beginner",
                "days": 3,
                "modules": [
                    {
                        "name": "Test Module",
                        "lessons": [
                            {
                                "title": "Test Lesson",
                                "content": "Test Content"
                            }
                        ]
                    }
                ],
                "tasks": ["Task 1", "Task 2"],
                "quizzes": [
                    {
                        "question": "Test Question",
                        "options": ["A", "B", "C"],
                        "correct_answer": "A"
                    }
                ],
                "practice_plan": ["Daily Practice", "Weekly Review"]
            }
        }

class CourseRequest(BaseModel):
    topic: str
    level: str
    days: int

@app.post("/test-json", response_model=CourseResponse)
async def test_json_endpoint():
    """Test endpoint that returns properly formatted JSON."""
    return CourseResponse(
        topic="Test Topic",
        level="beginner",
        days=3,
        modules=[
            Module(
                name="Test Module",
                lessons=[
                    Lesson(
                        title="Test Lesson",
                        content="Test Content"
                    )
                ]
            )
        ],
        tasks=["Task 1", "Task 2"],
        quizzes=[
            Quiz(
                question="Test Question",
                options=["A", "B", "C"],
                correct_answer="A"
            )
        ],
        practice_plan=["Daily Practice", "Weekly Review"]
    )

@app.post("/generate-course", response_model=CourseResponse)
async def generate_course_endpoint(request: CourseRequest):
    """Generate a course based on the provided parameters."""
    try:
        logger.info(f"Generating course for topic: {request.topic}, level: {request.level}, days: {request.days}")
        
        return CourseResponse(
            topic=request.topic,
            level=request.level,
            days=request.days,
            modules=[
                Module(
                    name=f"Introduction to {request.topic}",
                    lessons=[
                        Lesson(
                            title="Getting Started",
                            content=f"Basic introduction to {request.topic}"
                        ),
                        Lesson(
                            title="Core Concepts",
                            content=f"Understanding the fundamentals of {request.topic}"
                        )
                    ]
                )
            ],
            tasks=[f"Day {i+1}: Practice {request.topic}" for i in range(request.days)],
            quizzes=[
                Quiz(
                    question=f"What is {request.topic}?",
                    options=["A", "B", "C", "D"],
                    correct_answer="A"
                )
            ],
            practice_plan=[
                f"Daily: Study {request.topic}",
                f"Weekly: Review {request.topic}"
            ]
        )
        
    except Exception as e:
        logger.error(f"Error generating course: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def read_root():
    return {"status": "API is running"}

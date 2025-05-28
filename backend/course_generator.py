import logging
from typing import List, Dict, Optional
import json
from models import CourseResponse, Module, Lesson, Quiz
from config import AI_AVAILABLE, ERROR_MESSAGES
from ai_service import AIService
from json_utils import parse_json_response
from loguru import logger

def validate_topic(topic: str) -> bool:
    """Validate if the topic is appropriate for course generation."""
    if not topic or len(topic.strip()) < 2:
        raise ValueError("Invalid topic: Topic must be at least 2 characters long")
    return True

def validate_course_content(content: Dict) -> bool:
    """Validate the generated course content structure."""
    required_fields = ["modules", "tasks", "quizzes", "practice_plan"]
    for field in required_fields:
        if field not in content:
            raise ValueError(f"Missing required field: {field}")
        
    if not content["modules"]:
        raise ValueError("Course must have at least one module")
        
    return True

async def generate_course(topic: str, level: str, days: int) -> CourseResponse:
    """Main function: try AI first, then fallback."""
    try:
        # Validate input
        validate_topic(topic)
        
        if AI_AVAILABLE:
            try:
                logger.info("Attempting AI-based course generation")
                return await generate_course_with_ai(topic, level, days)
            except Exception as e:
                logger.warning(f"AI generation failed with error: {e}")
                logger.info("Falling back to rule-based generation")
        
        # Fallback to rule-based if AI is not available or fails
        return generate_course_rule_based(topic, level, days)
        
    except Exception as e:
        logger.error(f"Course generation failed: {str(e)}")
        raise

def generate_course_rule_based(topic: str, level: str, days: int) -> CourseResponse:
    """A rule-based course generator as a fallback."""
    logger.info("Using rule-based course generation")
    
    try:
        # Select content based on topic
        if "c++" in topic.lower():
            content = generate_cpp_content()
        else:  # Default to web development
            content = generate_web_dev_content()
        
        # Validate content structure
        validate_course_content(content)
        
        # Create modules from content
        modules = []
        for module_data in content["modules"]:
            lessons = []
            for lesson_data in module_data["lessons"]:
                lesson = Lesson(
                    title=lesson_data["title"],
                    explanation=lesson_data["explanation"],
                    content=lesson_data["content"],
                    coding_task=lesson_data["coding_task"],
                    key_takeaway=lesson_data["key_takeaway"]
                )
                lessons.append(lesson)
            
            module = Module(
                name=module_data["name"],
                lessons=lessons
            )
            modules.append(module)
        
        # Create quizzes from content
        quizzes = [
            Quiz(
                question=quiz_data["question"],
                options=quiz_data["options"],
                correct_answer=quiz_data["correct_answer"]
            )
            for quiz_data in content["quizzes"]
        ]
        
        # Create daily tasks
        tasks = [f"Day {i+1}: Complete the daily module and practice exercises" for i in range(days)]
        
        # Create a practice plan
        practice_plan = [
            f"Daily: Study theory and complete coding exercises",
            f"Weekly: Work on a small project applying learned concepts",
            f"Monthly: Build a comprehensive project combining all skills"
        ]
        
        return CourseResponse(
            topic=topic,
            level=level,
            days=days,
            modules=modules,
            tasks=tasks,
            quizzes=quizzes,
            practice_plan=practice_plan
        )
    except Exception as e:
        logger.error(f"Rule-based generation failed: {str(e)}")
        raise ValueError(f"Failed to generate course content: {str(e)}")

async def generate_course_with_ai(topic: str, level: str, days: int) -> CourseResponse:
    """Generate a course using the AI service."""
    logger.info("Attempting to generate course using AI")
    
    ai_service = AIService()
    try:
        content = await ai_service.generate_course_content(topic, level, days)
        if not content:
            raise ValueError("AI service returned empty content")
            
        # Validate content structure
        validate_course_content(content)
        
        try:
            # Create modules
            modules_data = parse_json_response(content.get("modules", "[]"))
            modules = []
            for module_data in modules_data:
                lessons = [
                    Lesson(
                        title=lesson["title"],
                        explanation=lesson.get("explanation", "Detailed explanation to be added"),
                        content=lesson["content"],
                        coding_task=lesson.get("coding_task", "Practice task to be added"),
                        key_takeaway=lesson.get("key_takeaway", "Key points to remember")
                    )
                    for lesson in module_data.get("lessons", [])
                ]
                modules.append(Module(name=module_data["name"], lessons=lessons))
            
            # Parse tasks
            tasks = content.get("tasks", [])
            if not tasks:
                raise ValueError("No tasks generated")
            
            # Parse quizzes
            quizzes_data = content.get("quizzes", [])
            if not quizzes_data:
                raise ValueError("No quizzes generated")
                
            quizzes = [
                Quiz(
                    question=quiz["question"],
                    options=quiz["options"],
                    correct_answer=quiz["correct_answer"]
                )
                for quiz in quizzes_data
            ]
            
            # Parse practice plan
            practice_plan = content.get("practice_plan", [])
            if not practice_plan:
                raise ValueError("No practice plan generated")
            
            return CourseResponse(
                topic=topic,
                level=level,
                days=days,
                modules=modules,
                tasks=tasks,
                quizzes=quizzes,
                practice_plan=practice_plan
            )
            
        except Exception as e:
            logger.error(f"Error parsing AI-generated content: {e}")
            raise ValueError(f"Failed to parse AI-generated content: {str(e)}")
            
    except Exception as e:
        logger.error(f"AI generation failed: {e}")
        raise ValueError(f"AI generation failed: {str(e)}")

def generate_cpp_content():
    """Generate C++ course content as an example."""
    return {
        "modules": [
            {
                "name": "Day 1: Introduction to C++",
                "lessons": [
                    {
                        "title": "Getting Started with C++",
                        "explanation": """C++ is a powerful general-purpose programming language that extends C with object-oriented features. Created by Bjarne Stroustrup in 1979, it has become one of the most widely used programming languages.

Key features that make C++ stand out:
1. Object-Oriented Programming support with classes and inheritance
2. Low-level memory manipulation capabilities
3. High performance and efficiency
4. Extensive standard library
5. Platform independence and portability

C++ is commonly used in system programming, game development, embedded systems, and high-performance applications where direct hardware access and performance are crucial.""",
                        "content": "Basic syntax, variables, and data types in C++",
                        "coding_task": """Create a simple C++ program that:
1. Declares variables of different data types (int, float, char)
2. Performs basic arithmetic operations
3. Prints the results to the console

Example structure:
```cpp
#include <iostream>
using namespace std;

int main() {
    // Your code here
    return 0;
}
```""",
                        "key_takeaway": "C++ combines the efficiency of C with object-oriented features, making it ideal for both system-level and application development."
                    }
                ]
            }
        ],
        "quizzes": [
            {
                "question": "Which of the following is NOT a key feature of C++?",
                "options": [
                    "Object-Oriented Programming",
                    "Automatic garbage collection",
                    "Low-level memory manipulation",
                    "Platform independence"
                ],
                "correct_answer": "Automatic garbage collection"
            }
        ],
        "tasks": ["Day 1: Complete introduction to C++ module"],
        "practice_plan": [
            "Daily: Practice basic syntax and data types",
            "Weekly: Build small console applications",
            "Monthly: Create a comprehensive C++ project"
        ]
    }

def generate_web_dev_content():
    """Generate Web Development course content as an example."""
    return {
        "modules": [
            {
                "name": "Day 1: Introduction to Web Development",
                "lessons": [
                    {
                        "title": "Understanding Web Development Fundamentals",
                        "explanation": """Web development is the process of creating websites and web applications. It encompasses several key technologies and concepts that work together to deliver content on the internet.

The three core technologies of web development are:
1. HTML (HyperText Markup Language) - Structures the content
2. CSS (Cascading Style Sheets) - Styles the presentation
3. JavaScript - Adds interactivity and dynamic behavior

Modern web development also includes:
- Frontend frameworks like React and Vue.js
- Backend technologies like Node.js and Python
- Database systems for data storage
- Version control systems like Git""",
                        "content": "Basic HTML structure and common elements",
                        "coding_task": """Create a simple HTML webpage that includes:
1. A header with a title
2. A navigation menu
3. Main content area with paragraphs and images
4. A footer with contact information

Example structure:
```html
<!DOCTYPE html>
<html>
<head>
    <title>My First Webpage</title>
</head>
<body>
    <!-- Your code here -->
</body>
</html>
```""",
                        "key_takeaway": "Web development combines HTML, CSS, and JavaScript to create interactive websites."
                    }
                ]
            }
        ],
        "quizzes": [
            {
                "question": "Which language is responsible for styling web pages?",
                "options": [
                    "HTML",
                    "CSS",
                    "JavaScript",
                    "Python"
                ],
                "correct_answer": "CSS"
            }
        ],
        "tasks": ["Day 1: Complete introduction to web development module"],
        "practice_plan": [
            "Daily: Practice HTML and CSS basics",
            "Weekly: Build simple web pages",
            "Monthly: Create a complete website"
        ]
    }

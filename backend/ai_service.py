import ollama
import json
from loguru import logger
from typing import Dict, List, Optional
from config import AI_MODEL, OLLAMA_HOST, MAX_TOKENS, TEMPERATURE
from json_utils import parse_json_response, format_course_response

class AIServiceError(Exception):
    """Custom exception for AI service errors"""
    pass

class AIService:
    def __init__(self):
        self.model = AI_MODEL
        self.host = OLLAMA_HOST
        
    async def generate_content(self, prompt: str, expect_json: bool = False, max_retries: int = 3) -> Optional[str]:
        """Generate content using Ollama with specified model."""
        for attempt in range(max_retries):
            try:
                if expect_json:
                    prompt = f"""
                    You are a JSON generator. Your task is to generate valid JSON based on the following requirements.
                    Rules:
                    1. Return ONLY valid JSON, no other text
                    2. Include all necessary commas between elements
                    3. Format the JSON properly with correct indentation
                    4. Do not include any explanations or markdown
                    5. Do not use code blocks or ```json markers
                    6. Ensure all JSON is properly escaped
                    7. Add commas after every object in arrays
                    8. Add commas after every key-value pair except the last one in an object
                    
                    Requirements:
                    {prompt}
                    """
                
                response = ollama.generate(
                    model=self.model,
                    prompt=prompt,
                    stream=False,
                    options={
                        "temperature": TEMPERATURE,
                        "max_tokens": MAX_TOKENS
                    }
                )
                
                if expect_json:
                    try:
                        result = parse_json_response(response['response'])
                        if result:
                            return result
                        raise AIServiceError("Failed to parse JSON response")
                    except json.JSONDecodeError as e:
                        logger.error(f"JSON parsing error: {e}")
                        if attempt < max_retries - 1:
                            logger.info(f"Retrying JSON generation (attempt {attempt + 2}/{max_retries})")
                            continue
                        raise AIServiceError("Failed to generate valid JSON after multiple attempts")
                
                return response['response']
                
            except Exception as e:
                logger.error(f"Error generating content with Ollama (attempt {attempt + 1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    continue
                raise AIServiceError(f"Failed to generate content: {str(e)}")
                
        return None

    async def generate_course_content(self, topic: str, level: str, days: int) -> Dict:
        """Generate a complete course structure with content."""
        try:
            # Generate modules with lessons
            modules_prompt = f"""
            Create a JSON object representing a {level} level course on {topic} with {days} days of content.
            The JSON must follow this exact structure, including all commas:
            {{
                "modules": [
                    {{
                        "name": "Module Name",
                        "lessons": [
                            {{
                                "title": "Lesson Title",
                                "explanation": "Detailed explanation (5-10 lines)",
                                "content": "Detailed lesson content",
                                "coding_task": "Specific coding task with instructions",
                                "key_takeaway": "Key points to remember"
                            }},
                            {{
                                "title": "Another Lesson",
                                "explanation": "Detailed explanation (5-10 lines)",
                                "content": "More content",
                                "coding_task": "Specific coding task with instructions",
                                "key_takeaway": "Key points to remember"
                            }}
                        ]
                    }}
                ]
            }}
            """
            
            modules_content = await self.generate_content(modules_prompt, expect_json=True)
            if not modules_content:
                raise AIServiceError("Failed to generate modules content")
            
            # Generate daily tasks
            tasks_prompt = f"""
            Create a JSON array of {days} daily tasks for learning {topic} at {level} level.
            Format must be exactly:
            {{
                "tasks": [
                    "Day 1: Detailed task description",
                    "Day 2: Detailed task description",
                    "Day 3: Detailed task description"
                ]
            }}
            """
            
            tasks = await self.generate_content(tasks_prompt, expect_json=True)
            if not tasks:
                raise AIServiceError("Failed to generate tasks")
            
            # Generate quizzes
            quizzes_prompt = f"""
            Create a JSON object with 5 quiz questions for {topic} at {level} level.
            Format must be exactly:
            {{
                "quizzes": [
                    {{
                        "question": "Question text",
                        "options": ["Option A", "Option B", "Option C", "Option D"],
                        "correct_answer": "Correct option"
                    }},
                    {{
                        "question": "Another question",
                        "options": ["Option A", "Option B", "Option C", "Option D"],
                        "correct_answer": "Correct option"
                    }}
                ]
            }}
            """
            
            quizzes = await self.generate_content(quizzes_prompt, expect_json=True)
            if not quizzes:
                raise AIServiceError("Failed to generate quizzes")
            
            # Generate practice plan
            practice_prompt = f"""
            Create a JSON object with a practice plan for {topic} at {level} level.
            Format must be exactly:
            {{
                "practice_plan": [
                    "Daily: Practice activity description",
                    "Weekly: Practice activity description",
                    "Monthly: Practice activity description"
                ]
            }}
            """
            
            practice_plan = await self.generate_content(practice_prompt, expect_json=True)
            if not practice_plan:
                raise AIServiceError("Failed to generate practice plan")
            
            # Combine all content
            course_content = {
                "topic": topic,
                "level": level,
                "days": days,
                "modules": modules_content.get("modules", []),
                "tasks": tasks.get("tasks", []),
                "quizzes": quizzes.get("quizzes", []),
                "practice_plan": practice_plan.get("practice_plan", [])
            }
            
            # Validate the combined content
            if not course_content["modules"]:
                raise AIServiceError("No modules were generated")
            if not course_content["tasks"]:
                raise AIServiceError("No tasks were generated")
            if not course_content["quizzes"]:
                raise AIServiceError("No quizzes were generated")
            if not course_content["practice_plan"]:
                raise AIServiceError("No practice plan was generated")
            
            return course_content
            
        except AIServiceError as e:
            logger.error(f"AI service error: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in course content generation: {e}")
            raise AIServiceError(f"Failed to generate course content: {str(e)}")

import json
from typing import Any, Dict, Optional, Union
from loguru import logger
from config import ERROR_MESSAGES

class JSONParsingError(Exception):
    """Custom exception for JSON parsing errors"""
    pass

def clean_json_string(json_str: str) -> str:
    """Clean and prepare JSON string for parsing."""
    try:
        # Remove any markdown code block markers
        json_str = json_str.replace("```json", "").replace("```", "")
        
        # Remove any leading/trailing whitespace
        json_str = json_str.strip()
        
        # Handle potential line breaks and indentation
        json_str = json_str.replace("\r", "").replace("\t", "  ")
        
        return json_str
    except Exception as e:
        logger.error(f"Error cleaning JSON string: {e}")
        raise JSONParsingError("Failed to clean JSON string")

def validate_json_structure(data: Dict) -> bool:
    """Validate the structure of parsed JSON data."""
    required_fields = ["modules", "tasks", "quizzes", "practice_plan"]
    
    try:
        # Check for required top-level fields
        for field in required_fields:
            if field not in data:
                raise JSONParsingError(ERROR_MESSAGES["missing_field"].format(field=field))
        
        # Validate modules structure
        if not data["modules"]:
            raise JSONParsingError(ERROR_MESSAGES["no_modules"])
            
        for module in data["modules"]:
            if not isinstance(module, dict):
                raise JSONParsingError(ERROR_MESSAGES["invalid_module"])
            if "name" not in module or "lessons" not in module:
                raise JSONParsingError(ERROR_MESSAGES["invalid_module"])
            if not module["lessons"]:
                raise JSONParsingError(ERROR_MESSAGES["missing_lessons"])
                
            for lesson in module["lessons"]:
                if not isinstance(lesson, dict):
                    raise JSONParsingError(ERROR_MESSAGES["invalid_lesson"])
                required_lesson_fields = ["title", "explanation", "content"]
                for field in required_lesson_fields:
                    if field not in lesson:
                        raise JSONParsingError(f"Missing required field in lesson: {field}")
        
        # Validate quizzes structure
        if not data["quizzes"]:
            raise JSONParsingError(ERROR_MESSAGES["no_quizzes"])
            
        for quiz in data["quizzes"]:
            if not isinstance(quiz, dict):
                raise JSONParsingError(ERROR_MESSAGES["invalid_quiz"])
            required_quiz_fields = ["question", "options", "correct_answer"]
            for field in required_quiz_fields:
                if field not in quiz:
                    raise JSONParsingError(f"Missing required field in quiz: {field}")
            if len(quiz["options"]) != 4:  # Assuming we want exactly 4 options
                raise JSONParsingError(ERROR_MESSAGES["quiz_options"])
        
        # Validate tasks and practice plan
        if not data["tasks"]:
            raise JSONParsingError("No tasks provided")
        if not data["practice_plan"]:
            raise JSONParsingError(ERROR_MESSAGES["no_practice_plan"])
        
        return True
        
    except JSONParsingError:
        raise
    except Exception as e:
        logger.error(f"Error validating JSON structure: {e}")
        raise JSONParsingError(ERROR_MESSAGES["validation"])

def parse_json_response(response: str) -> Optional[Dict]:
    """Parse and validate JSON response from AI service."""
    try:
        # Clean the JSON string
        cleaned_json = clean_json_string(response)
        
        try:
            # Attempt to parse the JSON
            data = json.loads(cleaned_json)
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {e}")
            raise JSONParsingError(ERROR_MESSAGES["json_parsing"])
        
        # Validate the parsed data
        if not data:
            raise JSONParsingError(ERROR_MESSAGES["empty_content"])
            
        # For responses that should contain course content, validate the structure
        if isinstance(data, dict) and any(key in data for key in ["modules", "tasks", "quizzes"]):
            validate_json_structure(data)
        
        return data
        
    except JSONParsingError:
        raise
    except Exception as e:
        logger.error(f"Error parsing JSON response: {e}")
        raise JSONParsingError(f"Failed to parse JSON response: {str(e)}")

def format_course_response(data: Dict) -> Dict:
    """Format and validate course response data."""
    try:
        # Ensure all required fields are present
        required_fields = ["topic", "level", "days", "modules", "tasks", "quizzes", "practice_plan"]
        for field in required_fields:
            if field not in data:
                raise JSONParsingError(ERROR_MESSAGES["missing_field"].format(field=field))
        
        # Format and validate each section
        formatted_data = {
            "topic": str(data["topic"]),
            "level": str(data["level"]),
            "days": int(data["days"]),
            "modules": data["modules"],
            "tasks": [str(task) for task in data["tasks"]],
            "quizzes": data["quizzes"],
            "practice_plan": [str(plan) for plan in data["practice_plan"]]
        }
        
        # Validate the structure
        validate_json_structure(formatted_data)
        
        return formatted_data
        
    except JSONParsingError:
        raise
    except Exception as e:
        logger.error(f"Error formatting course response: {e}")
        raise JSONParsingError(f"Failed to format course response: {str(e)}")

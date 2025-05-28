import os
from loguru import logger

# AI Service Configuration
AI_AVAILABLE = os.getenv("AI_AVAILABLE", "true").lower() in ("true", "1", "yes")
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
AI_MODEL = os.getenv("AI_MODEL", "mistral")

# API Configuration
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "2000"))
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))
MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))

# Content Generation Settings
MIN_LESSONS_PER_MODULE = int(os.getenv("MIN_LESSONS_PER_MODULE", "3"))
MAX_LESSONS_PER_MODULE = int(os.getenv("MAX_LESSONS_PER_MODULE", "5"))
MIN_QUIZZES = int(os.getenv("MIN_QUIZZES", "3"))
MAX_QUIZZES = int(os.getenv("MAX_QUIZZES", "5"))
MIN_EXPLANATION_LINES = int(os.getenv("MIN_EXPLANATION_LINES", "5"))
MAX_EXPLANATION_LINES = int(os.getenv("MAX_EXPLANATION_LINES", "10"))
QUIZ_OPTIONS_COUNT = int(os.getenv("QUIZ_OPTIONS_COUNT", "4"))

# Logging Configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = os.getenv(
    "LOG_FORMAT",
    "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
)

# Configure logging
logger.remove()  # Remove default handler
logger.add(
    "api.log",
    level=LOG_LEVEL,
    format=LOG_FORMAT,
    rotation="500 MB",
    compression="zip"
)

# Error Messages
ERROR_MESSAGES = {
    # Input Validation Errors
    "invalid_topic": "Invalid topic: Topic must be at least 2 characters long",
    "invalid_level": "Invalid level: Must be one of 'beginner', 'intermediate', or 'advanced'",
    "invalid_days": "Invalid days: Must be between 1 and 30",
    
    # Content Generation Errors
    "ai_generation": "Failed to generate content using AI service",
    "json_parsing": "Failed to parse JSON response",
    "validation": "Failed to validate course structure",
    "missing_field": "Missing required field in course structure: {field}",
    "empty_content": "Generated content is empty or invalid",
    
    # Module Errors
    "no_modules": "Course must have at least one module",
    "invalid_module": "Invalid module structure",
    "missing_lessons": "Module must have at least one lesson",
    
    # Lesson Errors
    "invalid_lesson": "Invalid lesson structure",
    "explanation_length": f"Explanation must be between {MIN_EXPLANATION_LINES} and {MAX_EXPLANATION_LINES} lines",
    
    # Quiz Errors
    "no_quizzes": "Course must have at least one quiz",
    "invalid_quiz": "Invalid quiz structure",
    "quiz_options": f"Quiz must have exactly {QUIZ_OPTIONS_COUNT} options",
    
    # Practice Plan Errors
    "no_practice_plan": "Course must have a practice plan",
    "invalid_practice_plan": "Invalid practice plan structure",
    
    # System Errors
    "server_error": "An unexpected error occurred. Please try again later.",
    "service_unavailable": "Service is temporarily unavailable. Please try again later.",
    "timeout": "Request timed out. Please try again.",
    
    # AI Service Errors
    "ai_unavailable": "AI service is temporarily unavailable",
    "ai_timeout": "AI service request timed out",
    "ai_error": "Error communicating with AI service",
    
    # File System Errors
    "file_not_found": "Required file not found: {file}",
    "file_access": "Error accessing file: {file}",
    
    # Database Errors
    "db_connection": "Database connection error",
    "db_query": "Database query error",
    
    # Authentication Errors
    "auth_required": "Authentication required",
    "invalid_token": "Invalid authentication token",
    "token_expired": "Authentication token has expired"
}

try:
    import ollama
    OLLAMA_AVAILABLE = True
    logger.info("Ollama integration available")
except ImportError:
    OLLAMA_AVAILABLE = False
    logger.warning("Ollama not available, falling back to rule-based generation")
    AI_AVAILABLE = False

# Log configuration on startup
logger.info(f"AI Service Configuration: Available={AI_AVAILABLE}, Model={AI_MODEL}")
logger.info(f"Content Generation Settings: Min Lessons={MIN_LESSONS_PER_MODULE}, Max Lessons={MAX_LESSONS_PER_MODULE}")
logger.info(f"API Configuration: Max Tokens={MAX_TOKENS}, Temperature={TEMPERATURE}")

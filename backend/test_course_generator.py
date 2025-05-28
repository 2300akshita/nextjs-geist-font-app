import asyncio
from course_generator import generate_course
import json
from loguru import logger

async def test_course_generation():
    logger.info("Starting course generation test")
    """Test the course generator with different topics."""
    
    try:
        # Test C++ course generation
        logger.info("Generating C++ Course")
        cpp_course = await generate_course("C++", "beginner", 5)
        logger.info("C++ course generated successfully")
        logger.debug(json.dumps(cpp_course.dict(), indent=2))
    
        logger.info("Verifying C++ course structure")
        # Verify course structure
        assert len(cpp_course.modules) > 0, "Course should have at least one module"
        assert len(cpp_course.quizzes) > 0, "Course should have at least one quiz"
        
        # Verify lesson structure
        lesson = cpp_course.modules[0].lessons[0]
        assert len(lesson.explanation.split('\n')) >= 5, "Explanation should be at least 5 lines"
        assert lesson.coding_task, "Lesson should have a coding task"
        assert lesson.key_takeaway, "Lesson should have a key takeaway"
        
        # Verify quiz structure
        quiz = cpp_course.quizzes[0]
        assert len(quiz.options) == 4, "Quiz should have exactly 4 options"
        
        logger.info("C++ course structure verified successfully")
    
        # Test Web Development course generation
        logger.info("Generating Web Development Course")
        web_course = await generate_course("Web Development", "beginner", 5)
        logger.info("Web Development course generated successfully")
        logger.debug(json.dumps(web_course.dict(), indent=2))
        
        logger.info("Verifying Web Development course structure")
        # Verify course structure
        assert len(web_course.modules) > 0, "Course should have at least one module"
        assert len(web_course.quizzes) > 0, "Course should have at least one quiz"
        
        # Verify lesson structure
        lesson = web_course.modules[0].lessons[0]
        assert len(lesson.explanation.split('\n')) >= 5, "Explanation should be at least 5 lines"
        assert lesson.coding_task, "Lesson should have a coding task"
        assert lesson.key_takeaway, "Lesson should have a key takeaway"
        
        # Verify quiz structure
        quiz = web_course.quizzes[0]
        assert len(quiz.options) == 4, "Quiz should have exactly 4 options"
        
        logger.info("Web Development course structure verified successfully")
        logger.info("All tests passed successfully!")
        
    except Exception as e:
        logger.error(f"Test failed with error: {str(e)}")
        raise

if __name__ == "__main__":
    asyncio.run(test_course_generation())

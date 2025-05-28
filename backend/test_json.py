import json
from json_utils import parse_json_response, clean_json_response, fix_json_string

test_json = """
{
    "modules": [
        {
            "name": "Introduction to Python",
            "lessons": [
                {
                    "title": "Getting Started",
                    "content": "Basic setup and first program"
                },
                {
                    "title": "Variables",
                    "content": "Understanding variables"
                }
            ]
        },
        {
            "name": "Control Flow",
            "lessons": [
                {
                    "title": "If Statements",
                    "content": "Learning conditionals"
                }
            ]
        }
    ],
    "tasks": [
        "Day 1: Setup Python",
        "Day 2: Write first program"
    ],
    "quizzes": [
        {
            "question": "What is Python?",
            "options": ["A", "B", "C", "D"],
            "correct_answer": "A"
        }
    ],
    "practice_plan": [
        "Daily: Code review",
        "Weekly: Project work"
    ]
}
"""

# Test with problematic JSON that's missing commas
problematic_json = """
{
    "modules": [
        {
            "name": "Introduction to Python"
            "lessons": [
                {
                    "title": "Getting Started"
                    "content": "Basic setup and first program"
                }
                {
                    "title": "Variables"
                    "content": "Understanding variables"
                }
            ]
        }
        {
            "name": "Control Flow"
            "lessons": [
                {
                    "title": "If Statements"
                    "content": "Learning conditionals"
                }
            ]
        }
    ]
    "tasks": [
        "Day 1: Setup Python"
        "Day 2: Write first program"
    ]
}
"""

def test_json_parsing():
    print("Testing JSON parsing...")
    
    # Test with valid JSON
    print("\n1. Testing with valid JSON:")
    try:
        parsed = json.loads(test_json)
        print("✓ Direct parsing successful!")
        print(json.dumps(parsed, indent=2))
    except json.JSONDecodeError as e:
        print(f"✗ Direct parsing failed: {e}")
    
    # Test with problematic JSON
    print("\n2. Testing with problematic JSON:")
    print("Original problematic JSON:")
    print(problematic_json)
    
    print("\nCleaning JSON...")
    cleaned = clean_json_response(problematic_json)
    print("Cleaned JSON:")
    print(cleaned)
    
    print("\nFixing JSON...")
    fixed = fix_json_string(cleaned)
    print("Fixed JSON:")
    print(fixed)
    
    print("\nParsing fixed JSON...")
    try:
        parsed = json.loads(fixed)
        print("✓ Parsing successful!")
        print(json.dumps(parsed, indent=2))
    except json.JSONDecodeError as e:
        print(f"✗ Parsing failed: {e}")
    
    # Test complete parse_json_response
    print("\n3. Testing complete parse_json_response with problematic JSON:")
    result = parse_json_response(problematic_json)
    if result:
        print("✓ Parsing successful!")
        print(json.dumps(result, indent=2))
    else:
        print("✗ Parsing failed!")

if __name__ == "__main__":
    test_json_parsing()

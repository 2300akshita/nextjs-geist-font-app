import ollama
import json

def clean_json_response(response: str) -> str:
    """Clean up the JSON response from Ollama."""
    # Remove markdown code block markers
    content = response.strip()
    if content.startswith('```'):
        content = '\n'.join(content.split('\n')[1:-1])
    
    # Add missing commas in JSON objects
    lines = content.split('\n')
    cleaned_lines = []
    for i, line in enumerate(lines):
        line = line.rstrip()
        if line and i < len(lines) - 1:
            next_line = lines[i + 1].strip()
            if (line.endswith('"') and next_line.startswith('"')) or \
               (line.endswith('}') and next_line.startswith('"')):
                line += ','
        cleaned_lines.append(line)
    
    return '\n'.join(cleaned_lines)

def test_ollama():
    print("Testing Ollama with a simple JSON generation task...")
    try:
        prompt = """
        You are a JSON generator. Your task is to generate valid JSON based on the following requirements.
        Rules:
        1. Return ONLY valid JSON, no other text
        2. Do not include any explanations
        3. Include all necessary commas between elements
        4. Ensure all JSON is properly formatted
        
        Generate a JSON object with this structure:
        {
            "modules": [
                {
                    "name": "Introduction to Python",
                    "lessons": [
                        {
                            "title": "Getting Started",
                            "content": "Basic Python setup and first program"
                        }
                    ]
                }
            ]
        }
        """
        
        print("Sending request to Ollama...")
        response = ollama.generate(
            model='mistral',
            prompt=prompt,
            stream=False
        )
        
        print("\nRaw response:", response['response'])
        
        # Clean and parse the response
        cleaned_json = clean_json_response(response['response'])
        print("\nCleaned JSON:", cleaned_json)
        
        # Try to parse the cleaned JSON
        try:
            json_response = json.loads(cleaned_json)
            print("\nParsed JSON:", json.dumps(json_response, indent=2))
            return True
        except json.JSONDecodeError as e:
            print("\nFailed to parse cleaned response as JSON:", str(e))
            return False
            
    except Exception as e:
        print("Error occurred:", str(e))
        return False

if __name__ == "__main__":
    print("Starting simple Ollama JSON test...")
    test_ollama()

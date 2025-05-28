import requests
import json

def test_json_endpoint():
    url = "http://localhost:8000/test-json"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    response = requests.post(url, headers=headers)
    
    # Get the raw response text
    print("Raw response:")
    print(response.text)
    print("\nParsed JSON:")
    try:
        parsed = json.loads(response.text)
        print(json.dumps(parsed, indent=2))
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")

if __name__ == "__main__":
    test_json_endpoint()

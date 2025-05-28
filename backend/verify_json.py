import requests
import json
from pprint import pprint

def verify_json():
    # Test the minimal endpoint
    response = requests.get("http://localhost:8002/test")
    data = response.json()
    
    print("Raw response text:")
    print(response.text)
    print("\nParsed JSON (pretty-printed):")
    print(json.dumps(data, indent=2, ensure_ascii=False))
    print("\nResponse headers:")
    print(response.headers)
    
    # Verify JSON structure
    print("\nJSON validation:")
    try:
        json.loads(response.text)
        print("✓ Valid JSON structure")
    except json.JSONDecodeError as e:
        print(f"✗ Invalid JSON: {e}")

if __name__ == "__main__":
    verify_json()

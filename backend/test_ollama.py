import ollama
import sys

def test_ollama():
    print("Starting Ollama test...")
    try:
        print("Attempting to connect to Ollama...")
        response = ollama.generate(
            model='mistral',
            prompt='Write a hello world program in Python.',
            stream=False
        )
        print("Response received from Ollama!")
        print("Response content:", response['response'])
        return True
    except Exception as e:
        print("Error occurred:", str(e), file=sys.stderr)
        return False

if __name__ == "__main__":
    print("Testing Ollama connection...")
    test_ollama()

import subprocess
import sys


def test_ollama_models():
    print("Testing available Ollama models...")

    # First, list available models
    try:
        result = subprocess.run(["ollama", "list"], capture_output=True, text=True, timeout=30)
        print("Available models:")
        print(result.stdout)

        # Test each model with a simple prompt
        models = ["phi", "phi3:mini", "codellama:7b"]

        for model in models:
            print(f"\n--- Testing {model} ---")
            try:
                test_prompt = "Say 'TEST OK' in one word."
                result = subprocess.run(
                    ["ollama", "run", model, test_prompt],
                    capture_output=True,
                    text=True,
                    timeout=30
                )

                print(f"Status: {result.returncode}")
                print(f"Output: {result.stdout[:100]}...")
                if result.stderr:
                    print(f"Error: {result.stderr[:200]}...")

            except subprocess.TimeoutExpired:
                print(f"❌ {model} timeout")
            except Exception as e:
                print(f"❌ {model} error: {e}")

    except Exception as e:
        print(f"❌ Cannot run ollama list: {e}")
        print("\nMake sure Ollama is installed and running:")
        print("1. Download from: https://ollama.ai/")
        print("2. Run: ollama serve")
        print("3. Pull a model: ollama pull phi")


if __name__ == "__main__":
    test_ollama_models()
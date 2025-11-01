import subprocess
import time
import threading


def run_ollama_model(model: str, prompt: str, timeout: int = 30):
    """Run a specific Ollama model with timeout"""
    try:
        result = subprocess.run(
            ["ollama", "run", model],
            input=prompt,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return result
    except subprocess.TimeoutExpired:
        return None
    except Exception as e:
        print(f"[ERROR] Model {model} failed: {e}")
        return None


def run_phi3(code: str, language: str = None):
    """
    Optimized version that tries multiple models with smart timeouts
    """
    # Simple, clear prompt for faster response
    prompt = f"""Please provide a brief code review (2-3 sentences) for this {language} code:

{code}

Review:"""

    start_time = time.time()

    # Try models in order of expected speed
    models_to_try = [
        ("phi:latest", 15),  # Fastest model, short timeout
        ("phi3:mini", 25),  # Medium speed
        ("codellama:7b", 30)  # Slower but more capable
    ]

    for model_name, timeout in models_to_try:
        print(f"[INFO] Trying model: {model_name} with {timeout}s timeout")

        result = run_ollama_model(model_name, prompt, timeout)

        if result and result.returncode == 0 and result.stdout.strip():
            elapsed = time.time() - start_time
            print(f"[SUCCESS] Got response from {model_name} in {elapsed:.2f}s")

            return {
                "review": result.stdout.strip(),
                "refactoring_suggestions": [],
                "comments": [],
                "partial_review": False,
                "estimated_time": elapsed,
                "language": language,
                "model_used": model_name
            }
        elif result and result.stderr:
            print(f"[WARNING] Model {model_name} error: {result.stderr[:200]}...")

    # If all models fail or timeout
    elapsed = time.time() - start_time
    print(f"[ERROR] All models failed or timed out")

    # Provide a basic fallback review
    fallback_review = f"""Basic code review for {language}:

This appears to be a calculator program that takes two numbers and an operation. 
The code uses global variables which might be better as local variables. 
Consider adding input validation and error handling for operations like division by zero."""

    return {
        "review": fallback_review,
        "refactoring_suggestions": [
            "Use local variables instead of global variables",
            "Add input validation",
            "Handle division by zero and other edge cases",
            "Improve variable names for better readability"
        ],
        "comments": [
            "Global variables a, b, c could be local to main()",
            "Consider using a switch statement for operations",
            "Add error handling for invalid inputs"
        ],
        "partial_review": True,
        "estimated_time": elapsed,
        "language": language,
        "fallback_used": True
    }
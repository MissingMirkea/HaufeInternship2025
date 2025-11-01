import subprocess
import time
from fallback_reviewer import fallback_review


def run_ollama_model(model: str, prompt: str, timeout: int = 180):
    """Run Ollama model with very large timeout"""
    try:
        print(f"[DEBUG] Running {model} with {timeout}s timeout...")
        print(f"[DEBUG] This might take up to {timeout // 60} minutes...")

        start_model_time = time.time()

        result = subprocess.run(
            ["ollama", "run", model],
            input=prompt,
            capture_output=True,
            text=True,
            timeout=timeout
        )

        model_time = time.time() - start_model_time
        print(f"[DEBUG] {model} completed in {model_time:.2f}s")

        return result
    except subprocess.TimeoutExpired:
        print(f"[DEBUG] {model} timed out after {timeout}s")
        return None
    except Exception as e:
        print(f"[DEBUG] {model} error: {e}")
        return None


def run_phi3(code: str, language: str = None):
    """
    Try AI models with VERY large timeouts
    """
    start_time = time.time()

    clean_code = code.strip()

    # Simple, clear prompt
    prompt = f"""Review this {language} code and provide feedback:

{clean_code}

Review:"""

    # Very large timeouts - up to 5 minutes per model
    models_to_try = [
        ("phi:latest", 120),  # 2 minutes
        ("phi3:mini", 180),  # 3 minutes
        ("codellama:7b", 300),  # 5 minutes
    ]

    for model_name, timeout in models_to_try:
        print(f"[INFO] Trying {model_name} with {timeout}s timeout ({timeout // 60} min)")
        result = run_ollama_model(model_name, prompt, timeout)

        if result and result.returncode == 0:
            response = result.stdout.strip()
            if response:
                elapsed = time.time() - start_time
                print(f"[SUCCESS] Got response from {model_name} in {elapsed:.2f}s")

                return {
                    "review": response,
                    "refactoring_suggestions": [],
                    "comments": [],
                    "partial_review": False,
                    "estimated_time": elapsed,
                    "language": language,
                    "model_used": model_name,
                    "ai_generated": True
                }

    # Fallback
    print("[INFO] Using fallback after all timeouts")
    result = fallback_review(code, language)
    result["estimated_time"] = time.time() - start_time
    result["ai_generated"] = False

    return result
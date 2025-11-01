import subprocess
import time


def preload_model(model_name: str):
    """Pre-load a model by sending a simple prompt"""
    print(f"Pre-loading {model_name}...")
    try:
        subprocess.run(
            ["ollama", "run", model_name, "Hello"],
            timeout=10,
            capture_output=True
        )
        print(f"✅ {model_name} pre-loaded")
        return True
    except:
        print(f"⚠️  {model_name} pre-load failed (but might still work)")
        return False


if __name__ == "__main__":
    print("Pre-loading models for faster responses...")
    models = ["phi:latest", "phi3:mini"]

    for model in models:
        preload_model(model)

    print("Pre-loading complete!")
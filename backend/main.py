from fastapi import FastAPI, Form, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from review_runner import run_phi3
from language_detector import detect_language
import time

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/review")
async def review_code(file: UploadFile = File(None), code_text: str = Form(None), language: str = Form(None)):
    try:
        start_time = time.time()

        if file:
            code = (await file.read()).decode()
            print(f"[INFO] Received file: {file.filename}, size: {len(code)} chars")
            if not language or language == "Auto-detect":
                language = detect_language(code)
        elif code_text:
            code = code_text
            print(f"[INFO] Received code text: {len(code)} chars")
            if not language or language == "Auto-detect":
                language = detect_language(code)
        else:
            return {"error": "No code provided"}

        print(f"[INFO] Processing {language} code with Ollama...")
        result = run_phi3(code, language)

        total_time = time.time() - start_time
        print(f"[INFO] Review completed in {total_time:.2f}s")

        return result

    except Exception as e:
        print(f"[ERROR] {str(e)}")
        return {"error": f"Server error: {str(e)}"}


@app.get("/")
def root():
    return {"message": "Code Review API is running!"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}
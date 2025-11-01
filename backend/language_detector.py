import re


def detect_language(code: str) -> str:
    code_lower = code.lower()

    # Check for C++ patterns first
    if re.search(r'^\s*#include\s*<|int main\s*\(|using namespace std;', code_lower):
        return "C++"
    elif re.search(r'^\s*def\s+\w+|import\s+\w+|from\s+\w+|print\s*\(', code_lower, re.MULTILINE):
        return "Python"
    elif re.search(r'function\s+\w+|console\.log|const\s+|let\s+|var\s+', code_lower):
        return "JavaScript"
    elif re.search(r'public\s+class|System\.out\.println|import\s+java\.', code_lower):
        return "Java"
    elif re.search(r'package\s+\w+|func\s+\w+', code_lower):
        return "Go"
    elif re.search(r'def\s+\w+|end\s*$|puts\s+', code_lower, re.MULTILINE):
        return "Ruby"
    else:
        return "Unknown"
def estimate_processing_time(lines: int) -> float:
    return min(lines * 0.1, 60)  # Max 60 seconds

def process_code_preview(code_lines: list, max_lines: int = 50):
    if len(code_lines) > max_lines:
        return code_lines[:max_lines], True
    return code_lines, False
"""
utils/helpers.py
Utility functions for CV Adviser.
"""
def validate_pdf(uploaded_file) -> tuple[bool, str]:
    """
    Basic validation for uploaded PDF file.
    Returns (is_valid: bool, message: str)
    """
    MAX_SIZE_MB = 5
    if uploaded_file is None:
        return False, "No file uploaded."

    # Check size (bytes → MB)
    size_mb = uploaded_file.size / (1024 * 1024)
    if size_mb > MAX_SIZE_MB:
        return False, f"File too large ({size_mb:.1f} MB). Maximum allowed: {MAX_SIZE_MB} MB."

    # Check MIME type
    if uploaded_file.type != "application/pdf":
        return False, "Only PDF files are supported."

    return True, "OK"


def truncate_text(text: str, max_chars: int = 6000) -> str:
    """
    Truncate text to max_chars to avoid exceeding model token limits.
    Adds a note if truncation occurred.
    """
    if len(text) <= max_chars:
        return text
    return text[:max_chars] + "\n\n[...CV truncated for analysis — please ensure CV is concise...]"


def build_download_bundle(
    eval_result: str,
    scoring_result: str,
    grammar_result: str,
    skill_gap_result: str,
    role: str
) -> str:
    """
    Combine all results into a single downloadable Markdown report.
    """
    sep = "\n\n---\n\n"
    parts = [
        f"# CV Adviser — Full Report\n**Target Role:** {role}\n",
        f"## CV Scoring & Rating\n{scoring_result}",
        f"## CV Evaluation\n{eval_result}",
        f"## Grammar & Formatting Feedback\n{grammar_result}",
    ]
    if skill_gap_result:
        parts.append(f"## Skill Gap Analysis\n{skill_gap_result}")
    return sep.join(parts)

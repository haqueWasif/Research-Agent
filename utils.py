"""
Utility functions for the Research Tool
"""

import regex as re
from dotenv import load_dotenv
import streamlit as st
import os
import pypandoc
import tempfile


os.environ["PATH"] += os.pathsep + r"C:\Program Files\Pandoc"


def remove_think_tags(text: str) -> str:
    """
    Remove <think> tags from the output
    
    Args:
        text: Input text with potential <think> tags
        
    Returns:
        Cleaned text without <think> tags
    """
    text = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)
    return text.strip()


def load_environment():
    """Load environment variables from .env file"""
    load_dotenv()


def get_api_key() -> str:
    # Try Streamlit secrets first (production)
    try:
        return st.secrets["OPENROUTER_API_KEY"]
    except (KeyError, FileNotFoundError):
        pass
    
    # Fall back to environment variable (local development)
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY not found")
    return api_key


def truncate_text(text: str, max_length: int = 20) -> str:
    """
    Truncate text to max length with ellipsis
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        
    Returns:
        Truncated text
    """
    if len(text) > max_length:
        return text[:max_length] + "..."
    return text

def markdown_to_pdf(markdown_text: str) -> bytes | None:
    """
    Convert Markdown text to a PDF for Streamlit deployment.
    Handles Greek, Chinese, and math symbols using a Unicode-safe font.
    """
    # Main text font
    main_font = "Noto Serif"
    # Math symbols font (supports 𝜇, 𝛴, etc.)
    math_font = "Noto Math"

    tmp_file = None
    try:
        tmp_file = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False)
        pdf_path = tmp_file.name
        tmp_file.close()

        # Convert Markdown -> PDF
        pypandoc.convert_text(
            markdown_text,
            to="pdf",
            format="md",
            outputfile=pdf_path,
            extra_args=[
                "--pdf-engine=xelatex",
                "-V", f"mainfont={main_font}",
                "-V", f"mathfont={math_font}"
            ]
        )

        with open(pdf_path, "rb") as f:
            pdf_bytes = f.read()

        return pdf_bytes

    except Exception as e:
        print(f"[PDF Generation Error] {e}")
        print("➡️ Make sure XeLaTeX and Noto Math font are installed on your system.")
        return None

    finally:
        if tmp_file and os.path.exists(pdf_path):
            os.remove(pdf_path)

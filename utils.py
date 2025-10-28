"""
Utility functions for the Research Tool
"""

import regex as re
from dotenv import load_dotenv
import streamlit as st
import os
import subprocess
import pandoc

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

import subprocess

def markdown_to_pdf(markdown_text):
    process = subprocess.Popen(
        ["pandoc", "-f", "markdown", "-t", "pdf", "-o", "-"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    pdf_bytes, error = process.communicate(input=markdown_text.encode("utf-8"))

    if process.returncode != 0:
        raise RuntimeError(f"Pandoc failed: {error.decode()}")

    return pdf_bytes



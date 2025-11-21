"""
Configuration settings for the Research Tool
"""

class Config:
    """Application configuration"""
    # API Configuration
    OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
    MODEL_NAME = "x-ai/grok-4.1-fast:free"s
    
    # Templates
    TEMPLATE_PATH = "template.json"
    
    # UI Configuration
    PAGE_TITLE = "Research Tool"
    PAGE_ICON = "📚"
    LAYOUT = "wide"
    
    # Paper format options
    PAPER_FORMATS = [
        'Research Paper',
        'Essay',
        'Blog Post',
        'Technical Report',
        'Literature Review',
        'Case Study',
        'White Paper'
    ]
    
    # Writing style options
    WRITING_STYLES = [
        'Academic',
        'Professional',
        'Conversational',
        'Technical',
        'Persuasive',
        'Analytical',
        'Descriptive'
    ]
    
    # Length options
    LENGTH_OPTIONS = [
        'Short (500 words)',
        'Medium (1000 words)',
        'Long (2000 words)',
        'Very Long (3000+ words)'
    ]

    # Chatbot Settings
    CHATBOT_MODEL = "minimax/minimax-m2:free" 
    CHATBOT_TEMPERATURE = 0.7
    CHATBOT_MAX_HISTORY = 20  # Max messages to keep in session
    
    # Floating Widget Settings
    CHATBOT_BUTTON_SIZE = 60  # pixels
    CHATBOT_WINDOW_WIDTH = 380  # pixels
    CHATBOT_WINDOW_HEIGHT = 600  # pixels

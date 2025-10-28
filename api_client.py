"""
API client for OpenRouter
"""

from typing import Optional
from openai import OpenAI
from config import Config


class OpenRouterClient:
    """Handle OpenRouter API interactions"""
    
    def __init__(self, api_key: str):
        """
        Initialize the API client
        
        Args:
            api_key: OpenRouter API key
        """
        self.client = OpenAI(
            base_url=Config.OPENROUTER_BASE_URL,
            api_key=api_key
        )
    
    def generate_completion(self, prompt: str) -> Optional[str]:
        """
        Generate completion from the API
        
        Args:
            prompt: The formatted prompt string
            
        Returns:
            Generated text content or None on error
        """
        try:
            completion = self.client.chat.completions.create(
                model=Config.MODEL_NAME,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=10000000
            )
            return completion.choices[0].message.content
        except Exception as e:
            print(f"API Error: {str(e)}")
            return None

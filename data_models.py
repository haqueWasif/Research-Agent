"""
Data structures for the Research Tool
"""

from dataclasses import dataclass
from typing import Dict


@dataclass
class UserInput:
    """User input data structure"""
    paper_format: str
    writing_style: str
    length: str
    topic: str
    
    def is_valid(self) -> bool:
        """Validate user input"""
        return bool(
            self.topic.strip() and 
            self.paper_format and 
            self.writing_style and 
            self.length
        )
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            'paper_format': self.paper_format,
            'writing_style': self.writing_style,
            'length': self.length,
            'topic': self.topic
        }


@dataclass
class EngineeredPrompt:
    """Engineered prompt data structure"""
    original_topic: str
    formatted_prompt: str
    metadata: Dict
    
    def __str__(self) -> str:
        return self.formatted_prompt

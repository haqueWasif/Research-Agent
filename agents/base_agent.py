"""
Base agent class for all agents
"""

from abc import ABC, abstractmethod


class BaseAgent(ABC):
    """Abstract base class for all agents"""
    
    def __init__(self, name: str):
        """
        Initialize base agent
        
        Args:
            name: Name of the agent
        """
        self.name = name
    
    @abstractmethod
    def run(self, *args, **kwargs):
        """
        Run the agent
        
        Must be implemented by subclasses
        """
        pass
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name='{self.name}')"

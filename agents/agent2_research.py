"""
Agent 2: Research Generator Agent
Responsibility: Generate research content from engineered prompts
"""

from typing import Optional
from api_client import OpenRouterClient
from data_models import EngineeredPrompt
from utils import remove_think_tags
from agents.base_agent import BaseAgent


class ResearchGeneratorAgent(BaseAgent):
    """
    Agent 2: Handles research content generation
    """
    
    def __init__(self, api_client: OpenRouterClient):
        """
        Initialize the agent
        
        Args:
            api_client: OpenRouterClient instance
        """
        super().__init__(name="ResearchGeneratorAgent")
        self.api_client = api_client
    
    def generate_research(self, engineered_prompt: EngineeredPrompt) -> Optional[str]:
        """
        Generate research content from engineered prompt
        
        Args:
            engineered_prompt: EngineeredPrompt object from Agent 1
            
        Returns:
            Generated research content or None on error
        """

        result = self.api_client.generate_completion(
            engineered_prompt.formatted_prompt
        )
        return result
    
    def process_output(self, raw_output: str) -> str:
        """
        Process the raw output
        
        Args:
            raw_output: Raw output from API
            
        Returns:
            Processed output
        """
        cleaned = remove_think_tags(raw_output)
        return cleaned
    
    def run(self, engineered_prompt: EngineeredPrompt) -> Optional[str]:
        """
        Run the research generator agent
        
        Args:
            engineered_prompt: EngineeredPrompt from Agent 1
            
        Returns:
            Processed research content or None on error
        """
        raw_output = self.generate_research(engineered_prompt)
        
        if raw_output:
            processed_output = self.process_output(raw_output)
            return processed_output
        
        return None

from typing import Optional
from data_models import UserInput, EngineeredPrompt
from api_client import OpenRouterClient
from agents.base_agent import BaseAgent

class PromptEngineeringAgent(BaseAgent):
    """
    Agent 1: Generates an optimized prompt for Agent 2 using an LLM
    """

    def __init__(self,  api_client: OpenRouterClient):
        """
        Args:
            api_client: OpenRouterClient instance
        """
        super().__init__(name="PromptEngineeringAgent")
        self.api_client = api_client

    def generate_prompt(self, user_input: UserInput) -> Optional[EngineeredPrompt]:
        """
        Use LLM to engineer the best prompt for the research task
        """
        # Create an instruction for the LLM about what type of prompt we want.
        system_instruction = (
            "Given the research goal below and constraints, generate an optimized, detailed prompt "
            "that will help another advanced AI agent produce the required research content.\n"
            f"Paper Format: {user_input.paper_format}\n"
            f"Writing Style: {user_input.writing_style}\n"
            f"Length: {user_input.length}\n"
            f"Topic or Query: {user_input.topic}\n\n"
            "IMPORTANT: Ensure that all math formulas in the generated research content "
            "are formatted using LaTeX syntax. Use $...$ for inline math and $$...$$ for display math. "
            "Do not convert formulas to Unicode symbols. Provide clean LaTeX-ready output."
        )


        try:    
            prompt_response = self.api_client.generate_completion(system_instruction)
            if not prompt_response:
                return None
            
            metadata = {
                'paper_format': user_input.paper_format,
                'writing_style': user_input.writing_style,
                'length': user_input.length,
                'original_topic': user_input.topic
            }

            return EngineeredPrompt(
                original_topic=user_input.topic,
                formatted_prompt=str(prompt_response),
                metadata=metadata
            )
        except Exception as e:
            print(f"Error generating engineered prompt: {str(e)}")
            return None

    def run(self, user_input: UserInput) -> Optional[EngineeredPrompt]:
        """
        Run the prompt generation process with an LLM
        """
        return self.generate_prompt(user_input)

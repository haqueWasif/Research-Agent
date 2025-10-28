"""
Main application orchestrator
Coordinates between agents and UI
"""

from utils import load_environment, get_api_key
from api_client import OpenRouterClient
from agents.agent1_prompt import PromptEngineeringAgent
from agents.agent2_research import ResearchGeneratorAgent
from ui.interface import UIInterface
from config import Config
import streamlit as st

class ResearchToolApp:
    """Main application orchestrator"""
    
    def __init__(self):
        """Initialize the application"""
        load_environment()
        
        try:
            api_key = get_api_key()
        except ValueError as e:
            st.error(f"❌ Configuration Error: {str(e)}")
            st.stop()
        
        # Initialize agents
        self.prompt_agent = PromptEngineeringAgent(OpenRouterClient(api_key))
        self.research_agent = ResearchGeneratorAgent(OpenRouterClient(api_key))
        
        # Initialize UI
        self.ui = UIInterface()
    
    def run(self):
        """Run the application"""

        # Setup and render
        self.ui.setup_page()
        self.ui.render_header()
        
        # Collect user input
        user_input = self.ui.render_input_form()
        
        # Generate button
        if self.ui.render_generate_button():
            if not user_input.is_valid():
                self.ui.show_error("❌ Please fill in all fields")
                return
            
            # Agent 1: Engineer prompt
            progress = self.ui.show_progress("⏳ Preparing your research request...")
            engineered_prompt = self.prompt_agent.run(user_input)
            
            print(engineered_prompt)
            if not engineered_prompt:
                self.ui.show_error("❌ Failed to prepare request. Please try again.")
                return
            
            # Agent 2: Generate research
            progress.info("⏳ Generating research content...")
            st.divider()
            
            research_content = self.research_agent.run(engineered_prompt)
            
            if not research_content:
                self.ui.show_error("❌ Failed to generate research. Please try again.")
                return
            
            # Clear progress and display results
            self.ui.clear_progress(progress)
            
            st.markdown("### Step 2: Your Generated Research")
            #self.ui.display_metadata(engineered_prompt.metadata)
            st.divider()
            
            self.ui.display_content(research_content)
            st.divider()
            
            self.ui.render_download_button(research_content)

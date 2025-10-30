"""
Main application orchestrator with Chatbot
Prevents unnecessary reruns and page refresh
"""

from utils import load_environment, get_api_key
from api_client import OpenRouterClient
from agents.agent1_prompt import PromptEngineeringAgent
from agents.agent2_research import ResearchGeneratorAgent
from ui.interface import UIInterface
from chatbot.chatbot_service import ResearchAgentChatbot
from config import Config
import streamlit as st
from uuid import uuid4


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
        
        # Initialize research agents
        self.prompt_agent = PromptEngineeringAgent(OpenRouterClient(api_key))
        self.research_agent = ResearchGeneratorAgent(OpenRouterClient(api_key))
        
        # Initialize chatbot service
        self.chatbot = ResearchAgentChatbot(api_key, Config.CHATBOT_MODEL)
        
        # Initialize UI
        self.ui = UIInterface()

    def _get_generated_content_context(self) -> str:
        """Extract context from generated content"""
        context = "RESEARCH-AGENT APP CONTEXT:\n\n"
        
        context += "Available Formats:\n"
        context += "- " + "\n- ".join(Config.PAPER_FORMATS) + "\n\n"
        
        context += "Available Styles:\n"
        context += "- " + "\n- ".join(Config.WRITING_STYLES) + "\n\n"
        
        context += "Available Lengths:\n"
        context += "- " + "\n- ".join(Config.LENGTH_OPTIONS) + "\n\n"
        
        if "generated_content" in st.session_state:
            context += f"Recently Generated: {st.session_state.generated_content.get('title', 'N/A')}\n"
        
        return context

    def render_floating_chatbot(self):
        """Render chatbot in sidebar - SEPARATE from main area"""
        
        # Initialize session state for chatbot
        if "chatbot_session_id" not in st.session_state:
            st.session_state.chatbot_session_id = str(uuid4())
            context = self._get_generated_content_context()
            self.chatbot.create_session(
                st.session_state.chatbot_session_id,
                context,
                session_state=st.session_state
            )
        
        if "chat_messages" not in st.session_state:
            st.session_state.chat_messages = []
        
        with st.sidebar:
            st.markdown("---")
            st.markdown("### 🤖 Research Assistant")
            
            messages_container = st.container()
            
            # Get user input
            user_input = st.chat_input("Ask about your research...")
            
            # Process message
            if user_input:
                st.session_state.chat_messages.append({
                    "role": "user",
                    "content": user_input
                })
                
                with st.spinner("Thinking..."):
                    result = self.chatbot.send_message(
                        st.session_state.chatbot_session_id,
                        user_input,
                        session_state=st.session_state
                    )
                
                if result["success"]:
                    st.session_state.chat_messages.append({
                        "role": "assistant",
                        "content": result["response"]
                    })
                else:
                    st.session_state.chat_messages.append({
                        "role": "assistant",
                        "content": f"❌ Error: {result.get('error')}"
                    })
            
            # Render messages
            with messages_container:
                for msg in st.session_state.chat_messages:
                    with st.chat_message(msg["role"]):
                        st.write(msg["content"])

    def _update_chatbot_with_document(self, research_content: str):
        """Update chatbot with generated document"""
        
        new_context = self._get_generated_content_context()
        
        new_context += f"\n\nCURRENT DOCUMENT:\n"
        new_context += f"{'='*60}\n"
        new_context += research_content
        new_context += f"\n{'='*60}\n"
        new_context += "\nHelp the user with this document."
        
        if "chatbot_session_id" in st.session_state:
            self.chatbot.update_context(
                st.session_state.chatbot_session_id,
                new_context,
                session_state=st.session_state
            )
            st.success("✅ Chatbot loaded with your document!")

    def run(self):
        """Run the application"""
        
        # Setup page
        self.ui.setup_page()
        
        # Render chatbot in sidebar (FIRST)
        self.render_floating_chatbot()
        
        # Main content area
        self.ui.render_header()
        user_input = self.ui.render_input_form()
        
        # Generate button
        if self.ui.render_generate_button():
            if not user_input.is_valid():
                self.ui.show_error("❌ Please fill in all fields")
                return
            
            try:
                # Agent 1: Engineer prompt
                progress = self.ui.show_progress("⏳ Preparing your research request...")
                engineered_prompt = self.prompt_agent.run(user_input)
                
                if not engineered_prompt:
                    self.ui.show_error("❌ Failed to prepare request. Please try again.")
                    return
                
                # Agent 2: Generate research
                progress.info("⏳ Generating research content...")
                st.divider()
                
                research_content = self.research_agent.run(engineered_prompt)
                
                if not research_content or research_content == "":
                    self.ui.show_error("❌ Failed to generate research. Please try again.")
                    return
                
                # Clear progress
                self.ui.clear_progress(progress)
                
                # ✅ CACHE THE CONTENT in session_state
                # This prevents regeneration on future reruns
                st.session_state.last_content = research_content
                st.session_state.last_title = (
                    engineered_prompt.get("title", "Untitled") 
                    if isinstance(engineered_prompt, dict) 
                    else "Generated Content"
                )
                
                # Display results
                st.markdown("### Step 2: Your Generated Research")
                st.divider()
                
                self.ui.display_content(research_content)
                st.divider()
                
                self.ui.render_download_button(research_content)
                
                # Store for chatbot
                st.session_state.generated_content = {
                    "title": st.session_state.last_title,
                    "content": research_content
                }
                
                # Update chatbot with document
                self._update_chatbot_with_document(research_content)
            
            except Exception as e:
                self.ui.show_error(f"❌ Error: {str(e)}")
                import traceback
                traceback.print_exc()
        
        # DISPLAY CACHED CONTENT IF IT EXISTS
        # This prevents regeneration when sidebar changes
        elif "last_content" in st.session_state:
            st.markdown("### Step 2: Your Generated Research")
            st.divider()
            
            self.ui.display_content(st.session_state.last_content)
            st.divider()
            
            self.ui.render_download_button(st.session_state.last_content)
            
            st.markdown("""
            ---
            💡 **Tip:** Ask the chatbot about your content in the sidebar!
            """)



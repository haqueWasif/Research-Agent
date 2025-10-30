"""
Chatbot service for Research-Agent
Stores sessions in Streamlit session_state to survive reruns
"""

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage
from typing import Dict
import os


class ResearchAgentChatbot:
    """Chatbot service - sessions stored in Streamlit session_state"""

    def __init__(self, api_key: str = None, model: str = "minimax/minimax-m2:free"):
        """Initialize chatbot"""
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")
        self.model = model
        # NOT storing sessions here - they'll be in st.session_state instead

    def create_session(self, session_id: str, internal_context: str = None, session_state=None):
        """
        Create a new conversation session
        
        Args:
            session_id: Unique session identifier
            internal_context: Context from generated content
            session_state: Streamlit session_state object
        """
        
        if session_state is None:
            raise ValueError("session_state is required")
        
        # Initialize LLM
        llm = ChatOpenAI(
            api_key=self.api_key,
            model=self.model,
            temperature=0.7,
            base_url="https://openrouter.ai/api/v1"
        )

        # Build system prompt
        system_prompt = self._build_system_prompt(internal_context)

        # Store in session_state (survives Streamlit reruns!)
        session_state.chatbot_sessions = session_state.get("chatbot_sessions", {})
        session_state.chatbot_sessions[session_id] = {
            "llm": llm,
            "system_prompt": system_prompt,
            "context": internal_context,
            "messages": [],
            "history": []
        }

    def _build_system_prompt(self, internal_context: str = None) -> str:
        """Build system prompt with context about Research-Agent"""
        
        base_prompt = """You are Research Assistant for the Research Content Generator application.

You help users understand their generated research papers, essays, blog posts, technical reports, literature reviews, case studies, and white papers.

Your role:
- Answer questions about the user's generated content
- Explain writing styles used (Academic, Professional, Conversational, Technical, Persuasive, Analytical, Descriptive)
- Help clarify content topics and structure
- Provide suggestions for improvement or revision
- Maintain context about all previous conversations

Guidelines:
- Provide clear, concise answers
- Reference specific parts of the content when relevant
- Maintain a professional and helpful tone
- Remember the conversation history"""

        if internal_context:
            base_prompt += f"\n\nCONTEXT ABOUT USER'S CONTENT:\n{internal_context}"

        return base_prompt

    def send_message(self, session_id: str, user_message: str, session_state=None) -> Dict:
        """
        Send message and get response
        
        Args:
            session_id: Session identifier
            user_message: User's message
            session_state: Streamlit session_state object
            
        Returns:
            Response with message and metadata
        """
        
        if session_state is None:
            raise ValueError("session_state is required")
        
        # Get sessions from session_state
        sessions = session_state.get("chatbot_sessions", {})
        
        if session_id not in sessions:
            return {
                "success": False,
                "error": "Session not found. Create session first."
            }

        try:
            session = sessions[session_id]
            llm = session["llm"]
            history = session["history"]
            
            # Build message list
            messages = [HumanMessage(content=session["system_prompt"])]
            
            # Add history (last 10 messages to save tokens)
            for msg in history[-10:]:
                if msg["role"] == "user":
                    messages.append(HumanMessage(content=msg["content"]))
                else:
                    messages.append(AIMessage(content=msg["content"]))
            
            # Add current message
            messages.append(HumanMessage(content=user_message))
            
            # Get response
            response = llm.invoke(messages)
            response_text = response.content
            
            # Store in history
            history.append({"role": "user", "content": user_message})
            history.append({"role": "assistant", "content": response_text})
            session["messages"].append({"role": "user", "content": user_message})
            session["messages"].append({"role": "assistant", "content": response_text})

            return {
                "success": True,
                "response": response_text,
                "session_id": session_id,
                "message_count": len(session["messages"])
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "session_id": session_id
            }

    def get_messages(self, session_id: str, session_state=None) -> list:
        """Get messages for a session"""
        if session_state is None:
            raise ValueError("session_state is required")
        
        sessions = session_state.get("chatbot_sessions", {})
        if session_id not in sessions:
            return []
        return sessions[session_id]["messages"]

    def clear_session(self, session_id: str, session_state=None):
        """Clear a session"""
        if session_state is None:
            raise ValueError("session_state is required")
        
        sessions = session_state.get("chatbot_sessions", {})
        if session_id in sessions:
            del sessions[session_id]

    def update_context(self, session_id: str, new_context: str, session_state=None):
        """Update context for existing session"""
        if session_state is None:
            raise ValueError("session_state is required")
        
        sessions = session_state.get("chatbot_sessions", {})
        if session_id not in sessions:
            return False
        
        sessions[session_id]["context"] = new_context
        sessions[session_id]["system_prompt"] = self._build_system_prompt(new_context)
        return True


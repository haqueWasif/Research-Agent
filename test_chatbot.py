import os
from dotenv import load_dotenv
from chatbot.chatbot_service import ResearchAgentChatbot

load_dotenv()

# Test
api_key = os.getenv("OPENROUTER_API_KEY")
if not api_key:
    print("❌ No API key found in .env")
    exit(1)

try:
    chatbot = ResearchAgentChatbot(api_key)
    session_id = "test-123"
    
    chatbot.create_session(session_id)
    print("✅ Session created")
    
    response = chatbot.send_message(session_id, "What is your purpose?")
    print(f"✅ Response received")
    print(f"Bot: {response['response']}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

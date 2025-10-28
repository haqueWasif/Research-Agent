# 📚 Research Content Generator

A sophisticated multi-agent AI system that generates high-quality research papers, essays, technical reports, and other academic content using advanced prompt engineering and LLM-powered content generation.

## 🎯 Overview

**Research Content Generator** is a professional-grade application built with Streamlit that leverages a two-agent architecture to produce publication-ready research content:

- **Agent 1 (Prompt Engineering Agent)**: Uses an LLM to dynamically generate optimized prompts based on user requirements
- **Agent 2 (Research Generator Agent)**: Generates high-quality research content using the engineered prompts

The system provides a clean, user-focused interface that hides all backend complexity, allowing users to focus on what matters: specifying their needs and receiving polished output.

## 🏗️ Architecture

### Two-Agent System

```
User Input
    ↓
[Agent 1: Prompt Engineering]
    • Analyzes user preferences
    • Generates optimized prompts
    ↓
[Agent 2: Research Generation]
    • Produces content using engineered prompts
    • Cleans and formats output
    ↓
Download-Ready Content
```

### Project Structure

```
research_tool/
├── config.py                  # Configuration & constants
├── data_models.py             # Data structures (UserInput, EngineeredPrompt)
├── api_client.py              # LLM API client (OpenRouter)
├── utils.py                   # Utility functions
├── ui/
│   ├── __init__.py
│   └── interface.py           # Streamlit UI components
├── agents/
│   ├── __init__.py
│   ├── base_agent.py          # Abstract base agent class
│   ├── agent1_prompt.py       # Prompt Engineering Agent
│   └── agent2_research.py     # Research Generator Agent
├── app.py                     # Application orchestrator
├── main.py                    # Entry point
├── .env                       # Environment variables (not in repo)
├── template.json              # (Optional) Fallback prompt template
└── README.md                  # This file
```

## ✨ Features

### Supported Content Types
- Research Papers
- Essays
- Blog Posts
- Technical Reports
- Literature Reviews
- Case Studies
- White Papers

### Writing Styles
- Academic
- Professional
- Conversational
- Technical
- Persuasive
- Analytical
- Descriptive

### Content Lengths
- Short (500 words)
- Medium (1000 words)
- Long (2000 words)
- Very Long (3000+ words)

### Additional Features
- **Smart Prompt Engineering**: Uses LLM to generate optimized prompts
- **Clean Output**: Automatically removes thinking tags and formatting artifacts
- **One-Click Download**: Export generated content as text files
- **Professional UI**: Clean, distraction-free user interface
- **Modular Architecture**: Easy to extend with new agents or features
- **Error Handling**: Graceful error messages and validation

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- OpenRouter API key (or compatible LLM API key)

### Installation

1. **Clone or download the project**
   ```bash
   git clone <repository-url>
   cd research_tool
   ```

2. **Create virtual environment (recommended)**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create `.env` file**
   ```bash
   echo "OPENROUTER_API_KEY=your_api_key_here" > .env
   ```

   Or manually create `.env`:
   ```
   OPENROUTER_API_KEY=sk-or-v1-xxxxxxxxxxxxx
   ```

5. **Create `template.json` (optional fallback)**
   ```json
   {
       "input_variables": ["paper_input", "style_input", "length_input", "user_input"],
       "template": "Write a {paper_input} in {style_input} style about {user_input}. The output should be approximately {length_input} in length."
   }
   ```

### Quick Start

```bash
streamlit run main.py
```

The application will open in your default browser at `http://localhost:8501`

## 📖 Usage

### Basic Workflow

1. **Open the application** and you'll see the Research Content Generator interface
2. **Fill in your requirements**:
   - Select paper format (Research Paper, Essay, etc.)
   - Choose writing style (Academic, Professional, etc.)
   - Pick desired length (Short, Medium, Long, Very Long)
   - Enter your research topic or question
3. **Click "Generate Research Content"** button
4. **Wait** for Agent 1 and Agent 2 to process (usually 10-30 seconds)
5. **Review** the generated content
6. **Download** as text file with one click

### Example Topics

- "The impact of machine learning on healthcare systems"
- "Sustainable energy solutions for developing nations"
- "Blockchain technology in supply chain management"
- "Artificial intelligence ethics and governance"
- "Remote work culture and employee productivity"

## 🔧 Configuration

All configuration is centralized in `config.py`:

```python
class Config:
    # API Settings
    OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
    MODEL_NAME = "minimax/minimax-m2:free"
    
    # UI Settings
    PAGE_TITLE = "Research Tool"
    PAGE_ICON = "📚"
    LAYOUT = "wide"
    
    # Content Options
    PAPER_FORMATS = [...]
    WRITING_STYLES = [...]
    LENGTH_OPTIONS = [...]
```

### Switching LLM Models

To use a different LLM (e.g., GPT-4, Claude):

1. Update `Config.MODEL_NAME` in `config.py`
2. Update API endpoint if necessary in `Config.OPENROUTER_BASE_URL`
3. Ensure your API key supports the new model

## 🏗️ Module Documentation

### Core Modules

#### `config.py`
- Centralized configuration
- Model settings, UI constants, content options
- Single source of truth for all settings

#### `data_models.py`
- `UserInput`: Stores user preferences with validation
- `EngineeredPrompt`: Contains generated prompt and metadata
- Both use dataclass decorators for clean code

#### `api_client.py`
- `OpenRouterClient`: Handles LLM API calls
- Implements error handling and retry logic
- Returns raw output from API

#### `utils.py`
- `remove_think_tags()`: Cleans LLM reasoning tags from output
- `load_environment()`: Loads environment variables
- `get_api_key()`: Retrieves and validates API key
- `truncate_text()`: Truncates long strings for display

#### `ui/interface.py`
- `UIInterface`: Static class containing all UI components
- Methods for rendering forms, buttons, content, downloads
- Separation of UI logic from business logic

### Agent Modules

#### `agents/base_agent.py`
- `BaseAgent`: Abstract base class for all agents
- Forces implementation of `run()` method
- Provides common agent interface

#### `agents/agent1_prompt.py`
- `PromptEngineeringAgent`: Generates optimized prompts using LLM
- Takes `UserInput`, returns `EngineeredPrompt`
- Implements intelligent prompt generation

#### `agents/agent2_research.py`
- `ResearchGeneratorAgent`: Generates research content
- Takes `EngineeredPrompt`, returns cleaned content
- Implements output processing and formatting

### Application Module

#### `app.py`
- `ResearchToolApp`: Main orchestrator class
- Initializes all components
- Coordinates workflow between agents and UI
- Handles user interaction and error states

#### `main.py`
- Entry point for the application
- Creates and runs `ResearchToolApp`

## 🔐 Security

### Best Practices

- **Never commit `.env` file** to version control
- **Use environment variables** for sensitive data
- **Validate user input** before processing
- **Handle API errors** gracefully
- **Limit API calls** to prevent abuse

### API Key Safety

```python
# Good - from environment
api_key = os.getenv("OPENROUTER_API_KEY")

# Bad - hardcoded
api_key = "sk-or-v1-xxxxx"  # DO NOT DO THIS
```

## 📦 Dependencies

See `requirements.txt`:

```
streamlit>=1.28.0
openai>=1.0.0
langchain-core>=0.1.0
python-dotenv>=1.0.0
regex>=2023.0.0
```

### Why Each Dependency?

- **streamlit**: Web framework for creating the UI
- **openai**: SDK for LLM API calls
- **langchain-core**: Prompt template management
- **python-dotenv**: Environment variable management
- **regex**: Advanced text pattern matching (for tag removal)

## 🚦 Error Handling

The application includes comprehensive error handling:

| Error | Cause | Solution |
|-------|-------|----------|
| API Key Not Found | Missing `.env` or env variable | Create `.env` with `OPENROUTER_API_KEY` |
| API Connection Failed | Network issue or invalid key | Check internet, verify API key validity |
| Template Load Failed | Missing or invalid `template.json` | Verify file exists and is valid JSON |
| Prompt Engineering Failed | LLM error or invalid input | Check input, review API logs |
| Content Generation Failed | LLM error or timeout | Try again, check API status |

## 🔄 Workflow Example

```
Input: "Impact of AI on healthcare"
Format: Research Paper
Style: Academic
Length: Medium (1000 words)

↓

Agent 1 generates optimized prompt:
"Write a comprehensive research paper in academic style 
about the impact of AI on healthcare systems. The paper 
should be approximately 1000 words and include introduction, 
methodology, findings, and conclusion. Use formal language 
and include relevant statistics and case studies..."

↓

Agent 2 receives engineered prompt and generates:
"Title: The Impact of Artificial Intelligence on Modern Healthcare Systems

Introduction:
Artificial intelligence (AI) has emerged as a transformative 
technology in the healthcare industry, fundamentally changing 
how medical professionals diagnose, treat, and manage patient care...
[continues for ~1000 words]"

↓

Output cleaned and formatted for download
```

## 🎨 Customization

### Adding New Paper Formats

Edit `config.py`:
```python
PAPER_FORMATS = [
    'Research Paper',
    'Essay',
    'Your New Format',  # Add here
    # ...
]
```

### Adding New Writing Styles

Edit `config.py`:
```python
WRITING_STYLES = [
    'Academic',
    'Your New Style',  # Add here
    # ...
]
```

### Adding New Agent

1. Create `agents/agent3_example.py`:
```python
from agents.base_agent import BaseAgent

class ExampleAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="ExampleAgent")
    
    def run(self, content):
        # Your logic here
        return processed_content
```

2. Initialize in `app.py`:
```python
self.example_agent = ExampleAgent()
```

3. Use in workflow:
```python
result = self.example_agent.run(previous_result)
```

## 📊 Performance

### Typical Timings

- **Prompt Engineering**: 2-5 seconds
- **Content Generation**: 15-45 seconds (depends on length)
- **Total**: 20-50 seconds per request

### Optimization Tips

- Use shorter content lengths for faster results
- Specific topics generate faster than vague ones
- Less complex writing styles may be faster

## 🐛 Troubleshooting

### Application won't start
```bash
# Check Python version
python --version  # Should be 3.8+

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### "API Key not found" error
```bash
# Verify .env file exists
ls -la .env

# Verify content
cat .env

# Should contain:
# OPENROUTER_API_KEY=your_key_here
```

### Slow content generation
- Check internet connection
- Verify API service status
- Try shorter content length
- Consider using faster model variant

### Output quality issues
- Try more specific topic descriptions
- Adjust writing style selection
- Increase content length for more detail
- Review and refine the generated prompt in logs

## 📈 Future Enhancements

Potential features for future versions:

- [ ] Fact-checking agent (Agent 3)
- [ ] Citation generator agent (Agent 4)
- [ ] Plagiarism detection agent
- [ ] Multi-language support
- [ ] Custom style templates
- [ ] Content variation generation
- [ ] Collaborative editing mode
- [ ] Cloud storage integration
- [ ] Batch processing for multiple topics
- [ ] Performance analytics and metrics

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Make your changes
4. Commit (`git commit -m 'Add AmazingFeature'`)
5. Push to branch (`git push origin feature/AmazingFeature`)
6. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

For issues, questions, or suggestions:

- Open an issue on GitHub
- Check existing issues for solutions
- Review the troubleshooting section
- Check API service status

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Powered by [OpenRouter API](https://openrouter.ai/)
- Uses [LangChain](https://www.langchain.com/) for prompt management
- Inspired by best practices in prompt engineering and multi-agent systems

## 📝 Changelog

### Version 1.0.0 (2025-10-28)
- Initial release
- Two-agent architecture (Prompt Engineering + Content Generation)
- Support for 7 paper formats and 7 writing styles
- Clean, user-focused interface
- Modular, extensible codebase

---

**Made with ❤️ by [Your Name/Team]**

For the latest updates and information, visit the [project repository](https://github.com/yourusername/research-tool)
# Research-Agent

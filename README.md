# LLM Tutorials

This folder contains comprehensive tutorials for building LLM-powered applications and agent systems. Each tutorial is self-contained with detailed explanations and practical examples.

## 📚 Available Tutorials

### 1. LLM Agents (`llm-agents/`)
A complete walkthrough of building LLM agents from basic concepts to sophisticated multi-agent systems.

**Topics Covered:**
- Basic Agent Architecture
- Specialized Agents (Fact Extraction, Sentiment Analysis)
- Tool Integration (Web Search, Wikipedia)
- Agent Coordination Patterns
- Multi-Agent Orchestration
- Real-world Applications

**File:** `llm-agents/simple_agents.ipynb`

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher

### Installation

1. **Clone or navigate to the tutorials folder:**
   ```bash
   cd /path/to/tutorials
   ```

2. **Install required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

   Or install individually:
   ```bash
   pip install jupyter google-generativeai python-dotenv requests wikipediaapi
   ```

3. **Set up API keys** (see API Configuration section below)

4. **Launch Jupyter:**
   ```bash
   jupyter notebook
   # or
   jupyter lab
   ```

## 🔑 API Configuration

The tutorials require API keys for various services. Create a `.env` file in each tutorial folder with the following structure:

### For `llm-agents/` tutorial:

Create `llm-agents/.env`:
```env
# Required: Google Gemini API Key
GEMINI_API_KEY=your_gemini_api_key_here

# Optional: For web search functionality
BRAVE_SEARCH_API_KEY=your_brave_search_api_key_here
```

### How to Get API Keys:

#### 1. Google Gemini API Key (Required)
- Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
- Sign in with your Google account
- Create a new API key
- Copy the key and add it to your `.env` file

#### 2. Brave Search API Key (Optional)
- Visit [Brave Search API](https://brave.com/search/api/)
- Sign up for a free account
- Get your API key from the dashboard
- Add it to your `.env` file

**Note:** The tutorials will work without the Brave Search API key, but web search functionality will be disabled.

## 📁 Folder Structure

```
tutorials/
├── README.md                 # This file
├── .gitignore               # Git ignore file
├── requirements.txt         # Python dependencies
└── llm-agents/
    ├── .env                 # API keys (create this file)
    ├── simple_agents.ipynb  # Main tutorial notebook
    └── README.md            # Tutorial-specific documentation
```

## 📋 Requirements

### Python Dependencies

Create a `requirements.txt` file with the following dependencies:

```txt
jupyter>=1.0.0
google-generativeai>=0.3.0
python-dotenv>=1.0.0
requests>=2.31.0
wikipediaapi>=0.6.0
```

### System Requirements

- **Python**: 3.8+
- **Memory**: 4GB RAM minimum (8GB recommended)
- **Network**: Internet connection for API calls
- **Storage**: 100MB free space

## 🔧 Configuration

### Environment Variables

Each tutorial folder should have its own `.env` file containing the necessary API keys and configuration. The `.env` files are automatically ignored by git for security.

### Example `.env` file:
```env
# Google Gemini API Key (Required)
GEMINI_API_KEY=your_actual_api_key_here

# Brave Search API Key (Optional)
BRAVE_SEARCH_API_KEY=your_brave_api_key_here

# Other configuration (if needed)
DEBUG=True
LOG_LEVEL=INFO
```

## 🛠️ Troubleshooting

### Common Issues

1. **API Key Not Found Error**
   - Ensure your `.env` file is in the correct folder
   - Check that the API key variable names match exactly
   - Verify your API keys are valid and active

2. **Module Not Found Error**
   - Install missing dependencies: `pip install -r requirements.txt`
   - Ensure you're using the correct Python environment

3. **Jupyter Not Starting**
   - Check if Jupyter is installed: `pip install jupyter`
   - Try launching with: `python -m jupyter notebook`

4. **API Rate Limiting**
   - Gemini API has rate limits on free tier
   - Brave Search API has monthly limits
   - Add delays between API calls if needed

### Getting Help

If you encounter issues:

1. Check the tutorial-specific README files
2. Review the error messages in the notebook cells
3. Ensure all API keys are properly configured
4. Verify internet connection for API calls

## 🌟 Tips for Success

1. **Start with Basic Examples**: Run the simple examples first before attempting complex multi-agent scenarios
2. **Monitor API Usage**: Keep track of your API usage to avoid rate limits
3. **Experiment**: Modify the code examples to understand how different parameters affect results
4. **Read the Documentation**: Each tutorial includes detailed explanations of concepts and patterns

## 📚 Additional Resources

- [Google Gemini API Documentation](https://ai.google.dev/docs)
- [Brave Search API Documentation](https://brave.com/search/api/)
- [Python-dotenv Documentation](https://python-dotenv.readthedocs.io/)
- [Jupyter Notebook Documentation](https://jupyter-notebook.readthedocs.io/)

## 🤝 Contributing

Feel free to:
- Report bugs or issues
- Suggest improvements
- Add new tutorial examples
- Share your own agent implementations

## 📄 License

These tutorials are provided for educational purposes.



# LLM Agents Tutorial

This tutorial provides a comprehensive walkthrough of building LLM agents from basic concepts to sophisticated multi-agent systems using Google Gemini.

## 📖 Tutorial Overview

**File:** `simple_agents.ipynb`

This Jupyter notebook takes you through a progressive journey of building LLM agents:

1. **Basic Agent Architecture** - Understanding the core components
2. **Specialized Agents** - Creating agents with specific capabilities
3. **Tool Integration** - Enabling agents to use external tools
4. **Agent Coordination** - Orchestrating multiple agents
5. **Real-world Applications** - Practical examples and patterns

## 🚀 Quick Start

### 1. Set up API Keys

Create a `.env` file in this directory with your API keys:

```env
# Required: Google Gemini API Key
GEMINI_API_KEY=your_gemini_api_key_here

# Optional: For web search functionality
BRAVE_SEARCH_API_KEY=your_brave_search_api_key_here
```

### 2. Install Dependencies

From the parent `tutorials/` directory:
```bash
pip install -r requirements.txt
```

### 3. Launch Jupyter

```bash
jupyter notebook simple_agents.ipynb
```

## 🔑 API Keys Required

### Google Gemini API Key (Required)
- **Get it from:** [Google AI Studio](https://makersuite.google.com/app/apikey)
- **Used for:** All LLM operations and agent processing
- **Free tier:** Available with rate limits

### Brave Search API Key (Optional)
- **Get it from:** [Brave Search API](https://brave.com/search/api/)
- **Used for:** Web search functionality in tool-enabled agents
- **Free tier:** 2,000 queries per month

## 📚 What You'll Learn

### Core Concepts

- **Agent Architecture:** How to structure LLM agents
- **Prompt Engineering:** Crafting effective agent instructions
- **Tool Integration:** Extending agent capabilities

### Advanced Patterns

- **Multi-Agent Systems:** Coordinating multiple specialized agents
- **Tool Registry:** Managing external capabilities
- **Orchestration:** Meta-agents that coordinate other agents
- **Error Handling:** Robust agent implementations

### Practical Applications

- **Fact Extraction:** Agents that extract structured information
- **Sentiment Analysis:** Agents that analyze emotions and tone
- **Web Search Integration:** Agents that gather external information
- **Research Assistance:** Agents that synthesize information from multiple sources

## 🛠️ Architecture Overview

The tutorial builds several types of agents:

```
BaseAgent (Foundation)
├── FactExtractorAgent
├── SentimentAnalyzerAgent
├── FactExtractorAgentToolsEnabled
├── SentimentAnalyzerAgentToolsEnabled
└── Orchestrator (Meta-Agent)

ToolRegistry (External Capabilities)
├── web_search()
└── wikipedia_search()
```

## 🎯 Learning Objectives

By the end of this tutorial, you'll be able to:

- Build basic LLM agents with specific instructions
- Create specialized agents for different tasks
- Implement tool integration for external capabilities
- Coordinate multiple agents to work together
- Design orchestrators for complex multi-agent systems
- Handle errors and edge cases in agent systems
- Apply these patterns to real-world problems

## 🛠️ Troubleshooting

### Common Issues

**"GEMINI_API_KEY not set" error:**
- Ensure `.env` file is in the `llm-agents/` directory
- Check that the API key is valid and active
- Restart Jupyter after adding the key

**JSON parsing errors:**
- The tutorial includes robust error handling
- Check the console output for detailed error messages
- Some responses may not be valid JSON - this is handled gracefully

**Tool execution failures:**
- Web search requires `BRAVE_SEARCH_API_KEY`
- Wikipedia search works without API keys
- Check internet connectivity

## 📈 Next Steps

After completing this tutorial, consider:

1. **Add more tools** - Database access, file processing, etc.
2. **Implement memory** - Let agents remember previous interactions
3. **Add validation** - Quality assurance for agent outputs
4. **Scale up** - Handle multiple users and concurrent requests
5. **Specialize** - Create domain-specific agents


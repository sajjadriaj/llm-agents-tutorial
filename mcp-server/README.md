# MCP Server Tutorial - Proper Architecture

This tutorial demonstrates the **correct** MCP (Model Context Protocol) architecture where:

- **Server**: Provides tools and resources
- **Client**: Contains agents and business logic
- **Clear separation of concerns**

## 🏗️ Architecture Overview

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   CLIENT SIDE   │    │   MCP SERVER    │    │   RESOURCES     │
│                 │    │                 │    │                 │
│  ┌───────────┐  │    │  ┌───────────┐  │    │  ┌───────────┐  │
│  │  Agents   │  │    │  │   Tools   │  │    │  │   Files   │  │
│  │           │  │    │  │           │  │    │  │           │  │
│  │ • Fact    │  │    │  │ • Web     │  │    │  │ • Docs    │  │
│  │ • Sent    │  │    │  │ • Wiki    │  │    │  │ • Data    │  │
│  │ • Orch    │  │    │  │ • LLM     │  │    │  │ • Config  │  │
│  └───────────┘  │    │  │ • File    │  │    │  └───────────┘  │
│                 │    │  └───────────┘  │    │                 │
│  ┌───────────┐  │    │                 │    │  ┌───────────┐  │
│  │ MCP Client│  │◄──►│  ┌───────────┐  │    │  │ Databases │  │
│  └───────────┘  │    │  │   API     │  │    │  └───────────┘  │
│                 │    │  │ Endpoints │  │    │                 │
└─────────────────┘    │  └───────────┘  │    └─────────────────┘
                       │                 │
                       │  ┌───────────┐  │
                       │  │ Registries│  │
                       │  │           │  │
                       │  │ • Tools   │  │
                       │  │ • Prompts │  │
                       │  │ • Resources│  │
                       │  └───────────┘  │
                       └─────────────────┘
```

## 📁 File Structure

```
mcp-server/
├── README.md                          # This file
├── requirements.txt                   # Python dependencies
├── mcp_server_tutorial.py            # ✅ MCP Server (tools & resources)
├── tools.py                          # ✅ Organized tool registries
├── client_agents.py                  # ✅ Client-side agents
├── mcp_architecture_tutorial.ipynb   # ✅ Interactive tutorial notebook
├── mcp_client_demo.py                # ✅ Client demo script
├── resources.py                      # Resource management
├── prompts.py                        # Prompt templates
├── ui/                               # Beautiful web UI
│   ├── index.html                    # Visual walkthrough
│   └── app.js                        # Interactive functionality
└── resources/                        # Resource files
    └── sample.txt
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd /home/sajjad/workspace/tutorials/mcp-server
pip install -r requirements.txt
```

### 2. Set Environment Variables

Create a `.env` file in the project directory:

```bash
# Create .env file
touch .env

# Add your API keys to .env file
echo "GEMINI_API_KEY=your_gemini_api_key_here" >> .env
echo "BRAVE_SEARCH_API_KEY=your_brave_search_api_key_here" >> .env
```

**Note**: The server automatically loads environment variables from the `.env` file using `python-dotenv`.

### 3. Start the MCP Server

```bash
python mcp_server_tutorial.py
```

The server will start on `http://localhost:5000`

### 4. Explore the Tutorial

```bash
# 🎨 Beautiful Web UI - Visual walkthrough
# Visit http://localhost:5000/ui

# 📚 Interactive Jupyter Notebook
# Open mcp_architecture_tutorial.ipynb in VS Code or Jupyter

# 🖥️ Command Line Demo
python mcp_client_demo.py

# 🤖 Direct Agent Usage
python client_agents.py
```

## 🎨 Beautiful Web UI

The MCP server includes a stunning visual walkthrough accessible at `http://localhost:5000/ui`:

### ✨ **Features:**
- **🏗️ Architecture Overview**: Visual diagrams and explanations
- **🛠️ Tool Explorer**: Interactive tool documentation and examples
- **🤖 Agent Showcase**: Step-by-step agent workflows
- **🎮 Live Demo**: Test tools directly from the browser
- **📱 Responsive Design**: Beautiful on desktop and mobile
- **🎯 Real-time Status**: Live server health and capabilities

### 🚀 **Getting Started:**
1. Start the server: `python mcp_server_tutorial.py`
2. Visit: `http://localhost:5000/ui`
3. Explore the interactive sections
4. Test tools with real server responses

The UI is built with **Tailwind CSS** for a modern, clean aesthetic and provides an intuitive way to understand the MCP architecture.

## 🛠️ Server Components

### 🔧 Tool Registry
- **FileReaderTool**: Read files from server resources
- **WebSearchTool**: Search the web using Brave Search API  
- **WikipediaTool**: Search Wikipedia for information
- **LLMTool**: Generate text using Gemini LLM
- **PromptFormatterTool**: Format prompts using templates

### 📁 Resource Registry
- Manages server files and data
- Provides caching for frequently accessed resources
- Handles resource discovery and access

### 📝 Prompt Registry
- Common prompt templates for different tasks
- Fact extraction, sentiment analysis, summarization
- Consistent prompt formatting across tools

**Note**: All registries are now properly organized and no longer use legacy backward-compatible wrappers.

## 🤖 Client-side Agents

### FactExtractorAgent
- Extracts facts from text using local LLM
- Can use web search and Wikipedia for research
- Returns structured fact data

### SentimentAnalyzerAgent
- Analyzes sentiment and emotional tone
- Can use external context for better analysis
- Returns sentiment scores and justifications

### OrchestrationAgent
- Coordinates multiple agents and tools
- Decides processing strategy based on query
- Synthesizes comprehensive responses

## 📊 API Endpoints

### Server Endpoints
- `GET /` - Welcome message
- `POST /mcp` - Main MCP tool execution
- `GET /capabilities` - Server capabilities and tools
- `GET /health` - Server health status
- `POST /prompt` - Prompt formatting

### Tool Usage
```python
# Use web search tool
client.use_tool("web_search", {
    "query": "latest AI developments",
    "count": 5
})

# Use Wikipedia tool
client.use_tool("wikipedia", {
    "query": "artificial intelligence",
    "sentences": 3
})

# Use LLM tool
client.use_tool("llm", {
    "prompt": "Explain quantum computing",
    "max_tokens": 500
})
```

## 🎯 Key Benefits

### ✅ Proper Architecture
- Clear separation between server (tools) and client (agents)
- Follows MCP specification standards
- Scalable and maintainable design

### ✅ Organized Structure
- Tool registry for easy tool management
- Resource registry for efficient resource handling
- Prompt registry for consistent prompt templates

### ✅ Flexible Agents
- Client-side agents can use any combination of server tools
- Easy to create specialized agents for specific tasks
- Proper error handling and fallback mechanisms

### ✅ Production Ready
- Health checks and monitoring
- Capability discovery
- Comprehensive error handling
- Performance optimization

## 🔧 Development

### Adding New Tools
1. Create tool class in `tools.py` following the standard pattern
2. Register in `ToolRegistry._initialize_default_tools()`
3. Server automatically exposes via `/mcp` endpoint
4. All tools must implement the `run(parameters)` method

### Adding New Agents
1. Create agent class in `client_agents.py`
2. Use `MCPClient` to access server tools via `/mcp` endpoint
3. Implement proper error handling and logging

### Adding New Resources
1. Add resource files to `resources/` directory
2. Register in `initialize_mcp_components()` function
3. Access via `FileReaderTool` using proper resource names

## 🧪 Testing

```bash
# Test server health
curl http://localhost:5000/health

# Test capabilities
curl http://localhost:5000/capabilities

# Test tool usage
curl -X POST http://localhost:5000/mcp \
  -H "Content-Type: application/json" \
  -d '{"tool": "web_search", "parameters": {"query": "test"}}'
```

## 📚 Learning Resources

1. **🎨 Visual Walkthrough**: Visit `http://localhost:5000/ui` for a beautiful interactive UI
2. **📚 Interactive Tutorial**: Open `mcp_architecture_tutorial.ipynb` in VS Code or Jupyter
3. **🖥️ Command Line Demo**: Run `python mcp_client_demo.py` for terminal-based examples
4. **🤖 Example Agents**: Check `client_agents.py` for implementation patterns
5. **🔧 Server Tools**: Review `tools.py` for organized tool structure
6. **📖 MCP Specification**: Official Model Context Protocol documentation

## 🔒 Security Notes

- Server validates all inputs and parameters
- Client agents handle authentication and authorization  
- Resource access is controlled by server
- API keys are managed securely via `.env` file (never commit to version control)
- All tool responses follow standardized success/error format

## 📈 Performance Tips

- Use connection pooling for multiple requests
- Implement caching for frequently accessed resources
- Monitor server health and resource usage
- Use async patterns for long-running operations

## 🔧 Troubleshooting

### Common Issues

**400 Bad Request Errors**
- Check that `.env` file exists and contains valid API keys
- Restart server after updating `.env` file
- Verify request format matches expected parameters

**API Key Issues**
- Ensure API keys are properly set in `.env` file
- Check that `python-dotenv` is installed
- Verify API keys are valid and have necessary permissions

**Tool Errors**
- Use `/health` endpoint to check server status
- Check `/capabilities` endpoint for available tools
- Review server logs for detailed error messages

**Connection Issues**
- Verify server is running on correct port (5000)
- Check firewall settings
- Ensure no other processes are using port 5000

### Debug Commands

```bash
# Check server health
curl http://localhost:5000/health

# Check capabilities
curl http://localhost:5000/capabilities

# Test basic tool
curl -X POST http://localhost:5000/mcp \
  -H "Content-Type: application/json" \
  -d '{"tool": "wikipedia", "parameters": {"query": "test"}}'
```

## 🚀 Next Steps

1. **Extend Tools**: Add domain-specific tools for your use case
2. **Create Specialized Agents**: Build agents for specific workflows
3. **Add Monitoring**: Implement comprehensive logging and metrics
4. **Deploy Production**: Set up proper deployment with load balancing

---

**Happy coding!** 🎉

For questions or contributions, check the tutorial files and examples in this directory.

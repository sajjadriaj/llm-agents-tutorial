# MCP Server Tutorial: IN PROGRESS

A comprehensive tutorial for building Model Context Protocol (MCP) servers using Python and Flask. This tutorial provides a practical, hands-on approach to understanding and implementing MCP servers.

## 📖 What is MCP?

**Model Context Protocol (MCP)** is a protocol that enables AI models to interact with external tools and data sources. This allows AI models to:

- Access real-world information
- Perform actions in external systems
- Integrate with databases, APIs, and file systems
- Extend their capabilities beyond text generation

## 🎯 Tutorial Overview

This tutorial provides a complete, production-ready implementation of an MCP server with detailed explanations for each component.

### 📁 Project Structure

```
mcp-server/
├── .env                      # Environment variables (create this)
├── README.md                 # This file
├── mcp_server_tutorial.py    # Main server implementation
├── tools.py                  # Tool definitions and handlers
├── resources.py              # Resource management
└── prompts.py               # Prompt templates and formatting
```

### ✨ Features

- **Flask-based Web Server** - RESTful API endpoints
- **Modular Architecture** - Clean separation of concerns
- **Tool System** - Extensible tool framework
- **Resource Management** - File and data handling
- **Prompt Engineering** - Dynamic prompt generation
- **Error Handling** - Robust error management
- **Comprehensive Documentation** - Detailed code comments

## 🚀 Getting Started

### Prerequisites

- **Python 3.10+** - Modern Python version
- **pip** - Python package installer
- **Basic knowledge** of Python and web APIs

### Installation

1. **Navigate to the tutorials directory:**
   ```bash
   cd tutorials
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Navigate to the MCP server directory:**
   ```bash
   cd mcp-server
   ```

5. **Set up environment variables:**
   Create a `.env` file in this directory:
   ```env
   # Server configuration
   FLASK_ENV=development
   FLASK_DEBUG=True
   
   # Add any API keys here if needed
   # GEMINI_API_KEY=gemini api key here
   ```

### Running the Server

Start the MCP server:

```bash
python mcp_server_tutorial.py
```

The server will start at `http://127.0.0.1:5000` with the following endpoints:
- **`/mcp`** - Main MCP protocol endpoint
- **`/prompt`** - Prompt generation endpoint
- **`/health`** - Health check endpoint

## 🔧 How to Use

### MCP Endpoint (`/mcp`)

The main MCP protocol endpoint handles tool requests and resource access.

#### Available Tools

- **`file_reader`** - Read content from predefined files
- **`calculator`** - Perform mathematical calculations
- **`text_processor`** - Process and transform text

#### Example: File Reader Tool

**Request:**
```bash
curl -X POST -H "Content-Type: application/json" -d '{
  "tool": "file_reader",
  "parameters": {
    "filename": "example.txt"
  }
}' http://127.0.0.1:5000/mcp
```

**Response:**
```json
{
  "success": true,
  "content": "This is the content of example.txt.",
  "metadata": {
    "tool": "file_reader",
    "filename": "example.txt",
    "timestamp": "2025-07-11T10:30:00Z"
  }
}
```

#### Example: Calculator Tool

**Request:**
```bash
curl -X POST -H "Content-Type: application/json" -d '{
  "tool": "calculator",
  "parameters": {
    "expression": "2 + 3 * 4"
  }
}' http://127.0.0.1:5000/mcp
```

**Response:**
```json
{
  "success": true,
  "result": 14,
  "expression": "2 + 3 * 4",
  "metadata": {
    "tool": "calculator",
    "timestamp": "2025-07-11T10:30:00Z"
  }
}
```

### Prompt Endpoint (`/prompt`)

Generate formatted prompts for AI models.

#### Example: Dynamic Prompt Generation

**Request:**
```bash
curl -X POST -H "Content-Type: application/json" -d '{
  "prompt_template": "analyze_text",
  "variables": {
    "text": "This is a sample text to analyze.",
    "task": "sentiment analysis"
  }
}' http://127.0.0.1:5000/prompt
```

**Response:**
```json
{
  "success": true,
  "formatted_prompt": "Please perform sentiment analysis on the following text: This is a sample text to analyze.",
  "template": "analyze_text",
  "variables": {
    "text": "This is a sample text to analyze.",
    "task": "sentiment analysis"
  }
}
```

### Health Check Endpoint (`/health`)

Check server status and configuration.

**Request:**
```bash
curl http://127.0.0.1:5000/health
```

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2025-07-11T10:30:00Z",
  "available_tools": ["file_reader", "calculator", "text_processor"]
}
```

## 🏗️ Architecture Overview

### Core Components

```
MCP Server Architecture
├── Flask Application (mcp_server_tutorial.py)
│   ├── Route Handlers
│   ├── Request Validation
│   └── Response Formatting
├── Tool System (tools.py)
│   ├── Tool Registry
│   ├── Tool Execution
│   └── Parameter Validation
├── Resource Manager (resources.py)
│   ├── File System Access
│   ├── Data Persistence
│   └── Resource Caching
└── Prompt Engine (prompts.py)
    ├── Template System
    ├── Variable Substitution
    └── Prompt Formatting
```

### Key Design Patterns

- **Modular Architecture** - Separate concerns into focused modules
- **Plugin System** - Easy tool registration and extension
- **Template Engine** - Dynamic prompt generation
- **Error Handling** - Graceful failure management
- **Validation** - Input sanitization and type checking

## 📚 Learning Objectives

By completing this tutorial, you'll understand:

1. **MCP Protocol Basics** - How MCP enables AI-tool interaction
2. **Server Architecture** - Building scalable API servers
3. **Tool Integration** - Creating and managing external tools
4. **Resource Management** - Handling files and data safely
5. **Prompt Engineering** - Dynamic prompt generation
6. **Error Handling** - Building robust server applications
7. **API Design** - RESTful endpoint patterns

## 🛠️ Configuration

### Environment Variables

Create a `.env` file in the `mcp-server/` directory:

```env
# Server Configuration
FLASK_ENV=development
FLASK_DEBUG=True
FLASK_PORT=5000

# Security
SECRET_KEY=your-secret-key-here

# API Keys (if needed)
GEMINI_API_KEY=your-gemini-api-key
ANTHROPIC_API_KEY=your-anthropic-key

# Logging
LOG_LEVEL=INFO
LOG_FILE=mcp_server.log

# Resource Limits
MAX_FILE_SIZE=10MB
MAX_REQUEST_SIZE=100MB
TIMEOUT_SECONDS=30
```

### Dependencies

Dependencies are managed in the parent `tutorials/requirements.txt` file which includes:

```txt
# Core dependencies for all tutorials
jupyter>=1.0.0
python-dotenv>=1.0.0
requests>=2.31.0

# LLM and AI dependencies
google-generativeai>=0.3.0
wikipediaapi>=0.6.0

# Web framework for MCP server tutorial
Flask>=2.3.0
```

## 🔧 Troubleshooting

### Common Issues

**Server won't start:**
- Check if port 5000 is available
- Verify Python version (3.10+)
- Ensure all dependencies are installed

**Tool execution fails:**
- Verify tool parameters are correct
- Check file permissions for file_reader
- Review server logs for detailed errors

**API responses are empty:**
- Confirm request format matches examples
- Check Content-Type header is set correctly
- Verify endpoint URLs are correct

### Debug Mode

Enable debug mode by setting in `.env`:
```env
FLASK_DEBUG=True
LOG_LEVEL=DEBUG
```

## 🚀 Next Steps

### Extending the Server

1. **Add New Tools:**
   - Database connectors
   - Web scraping tools
   - API integrations
   - File processing tools

2. **Enhance Security:**
   - Authentication middleware
   - Rate limiting
   - Input validation
   - CORS configuration

3. **Improve Performance:**
   - Caching layer
   - Async processing
   - Connection pooling
   - Load balancing

4. **Add Features:**
   - WebSocket support
   - Streaming responses
   - Batch processing
   - Tool chaining

### Integration Examples

- **OpenAI GPT Integration** - Connect to OpenAI API
- **Claude Integration** - Use Anthropic's Claude
- **Local LLM** - Integrate with local models
- **Database Tools** - SQL query execution
- **Web APIs** - REST API connectors

## 📄 API Reference

### MCP Endpoint

**POST `/mcp`**

Request body:
```json
{
  "tool": "string",
  "parameters": {
    "key": "value"
  }
}
```

Response:
```json
{
  "success": true,
  "result": "any",
  "metadata": {
    "tool": "string",
    "timestamp": "ISO-8601"
  }
}
```

### Prompt Endpoint

**POST `/prompt`**

Request body:
```json
{
  "prompt_template": "string",
  "variables": {
    "key": "value"
  }
}
```

Response:
```json
{
  "success": true,
  "formatted_prompt": "string",
  "template": "string",
  "variables": {}
}
```

### Health Endpoint

**GET `/health`**

Response:
```json
{
  "status": "healthy",
  "version": "string",
  "timestamp": "ISO-8601",
  "available_tools": ["string"]
}
```
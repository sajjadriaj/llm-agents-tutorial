# Simple MCP Server Tutorial

This repository contains a simple implementation of a Model Context Protocol (MCP) server for tutorial purposes. The server is written in Python using the Flask web framework.

## What is MCP?

MCP (Model Context Protocol) is a protocol that enables AI models to interact with external tools and data sources. This allows AI models to access and utilize real-world information and perform actions.

## About This Tutorial

This tutorial provides a basic, heavily commented implementation of an MCP server. The project is structured into the following files:

*   `mcp_server_tutorial.py`: The main server file that handles HTTP requests.
*   `tools.py`: Defines the tools that the server can use.
*   `resources.py`: Manages the data and resources that the tools can interact with.
*   `prompts.py`: Stores and formats the prompts that will be sent to the AI model.

### Features

*   A simple Flask-based web server.
*   An endpoint (`/mcp`) that handles MCP requests.
*   A modular structure with separate files for tools, resources, and prompts.
*   A mock "file reader" tool that can return the content of predefined files.
*   An endpoint (`/prompt`) for generating prompts.
*   Comprehensive comments explaining each part of the code.

## Getting Started

### Prerequisites

*   Python 3.6 or higher
*   pip (Python package installer)

### Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/simple-mcp-server-tutorial.git
    cd simple-mcp-server-tutorial
    ```

2.  **Install the required Python library (Flask):**

    ```bash
    pip install Flask
    ```

### Running the Server

To start the MCP server, run the following command in your terminal:

```bash
python mcp_server_tutorial.py
```

The server will start and be accessible at `http://127.0.0.1:5000`.

## How to Use

### MCP Endpoint (`/mcp`)

You can interact with the server by sending HTTP POST requests to the `/mcp` endpoint. You can use a tool like `curl` or an API client like Postman.

#### Example Request

Here is an example of how to request the content of `example.txt` using `curl`:

```bash
curl -X POST -H "Content-Type: application/json" -d '{
  "tool": "file_reader",
  "parameters": {
    "filename": "example.txt"
  }
}' http://127.0.0.1:5000/mcp
```

#### Example Response

The server will respond with a JSON object containing the content of the file:

```json
{
  "content": "This is the content of example.txt."
}
```

### Prompting Endpoint (`/prompt`)

The `/prompt` endpoint allows you to generate prompts that can be sent to an AI model.

#### Example Request

Here is an example of how to generate a prompt using `curl`:

```bash
curl -X POST -H "Content-Type: application/json" -d '{
  "prompt_template": "Summarize the following text: {text}",
  "text": "This is the text to be summarized."
}' http://127.0.0.1:5000/prompt
```

#### Example Response

The server will respond with a JSON object containing the formatted prompt:

```json
{
  "formatted_prompt": "Summarize the following text: This is the text to be summarized."
}
```

## Next Steps

This is a very basic implementation. Here are some ideas for extending it:

*   Add more tools (e.g., a calculator, a web search tool).
*   Implement more robust error handling.
*   Add authentication and authorization to control access to tools.
*   Connect the server to real data sources (e.g., a database, a live API).

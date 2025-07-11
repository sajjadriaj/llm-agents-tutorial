
# MCP Server Tutorial: A Simple Implementation
#
# Welcome to the MCP Server Tutorial!
#
# This file contains a simple, yet functional, implementation of a Model Context Protocol (MCP) server.
# MCP is a protocol that allows AI models to interact with external tools and data sources.
# This server will be a basic example of how such a server can be built.
#
# We will use the Flask web framework to create our server. Flask is a lightweight
# and popular choice for building web applications and APIs in Python.
#
# ---
#
# ## Setup and Installation
#
# Before you can run this server, you need to have Python installed on your system.
# You will also need to install the Flask library. You can install it using pip:
#
# pip install Flask
#
# ---
#
# ## Running the Server
#
# To run the server, simply execute this Python file from your terminal:
#
# python mcp_server_tutorial.py
#
# The server will start and listen for incoming requests on http://127.0.0.1:5000.
#
# ---
#
# ## How to Interact with the Server
#
# You can interact with this server by sending HTTP requests to its endpoints.
# We will define two endpoints:
#
# 1.  `/`: A simple endpoint to check if the server is running.
# 2.  `/mcp`: The main endpoint for handling MCP requests.
#
# You can use a tool like `curl` or a graphical API client like Postman to send requests.
#
# ---

# Let's start with the implementation.

# First, we import the necessary components from the Flask library.
# - Flask: The main class for creating our web application.
# - request: An object that holds information about the incoming HTTP request.
# - jsonify: A function to convert Python dictionaries into JSON responses.
from flask import Flask, request, jsonify

# We import the components from our other files.
from resources import ResourceManager
from tools import FileReaderTool
from prompts import format_prompt

# We create an instance of the Flask class. This `app` object will be our server.
app = Flask(__name__)

# We create instances of our resource manager and tools.
resources = ResourceManager()
file_reader_tool = FileReaderTool(resources)

# We define a dictionary to hold our available tools.
tools = {
    "file_reader": file_reader_tool
}

# ---
# ## Endpoint 1: The Root Endpoint (`/`)
#
# This is a simple endpoint to verify that our server is running correctly.
# When you open http://127.0.0.1:5000 in your web browser or send a GET request
# to it, you will see a welcome message.
@app.route('/', methods=['GET'])
def index():
    """
    A simple endpoint to confirm the server is running.
    """
    return "Welcome to the Simple MCP Server!"

# ---
# ## Endpoint 2: The MCP Endpoint (`/mcp`)
#
# This is the core of our MCP server. This endpoint will handle MCP requests.
# According to the MCP specification, the server should accept POST requests
# with a JSON payload.
#
# The request payload should contain information about the tool the AI model
# wants to use and the parameters for that tool.
#
@app.route('/mcp', methods=['POST'])
def mcp_handler():
    """
    Handles MCP requests.
    """
    # We first get the JSON data from the incoming request.
    # If the request does not contain JSON data, we return an error.
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid request: No JSON payload"}), 400

    # We extract the "tool" and "parameters" from the JSON data.
    tool_name = data.get('tool')
    parameters = data.get('parameters')

    # We check if the "tool" and "parameters" are present in the request.
    if not tool_name or not parameters:
        return jsonify({"error": "Invalid request: Missing 'tool' or 'parameters'"}), 400

    # We check if the requested tool is available.
    if tool_name in tools:
        # We get the tool from our dictionary of available tools.
        tool = tools[tool_name]
        # We run the tool with the given parameters.
        result = tool.run(parameters)
        return jsonify(result)
    else:
        # If the requested tool is not supported, we return an error.
        return jsonify({"error": f"Unsupported tool: {tool_name}"}), 400

# ---
# ## Endpoint 3: The Prompting Endpoint (`/prompt`)
#
# This endpoint is for generating prompts that can be sent to an AI model.
# It takes a prompt template and a text as input, and returns a formatted prompt.
#
@app.route('/prompt', methods=['POST'])
def prompt_handler():
    """
    Handles prompt generation requests.
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid request: No JSON payload"}), 400

    prompt_template = data.get('prompt_template')
    text = data.get('text')

    if not prompt_template or not text:
        return jsonify({"error": "Invalid request: Missing 'prompt_template' or 'text'"}), 400

    formatted = format_prompt(prompt_template, text)
    return jsonify({"formatted_prompt": formatted})

# ---
# ## Running the Server
#
# This is the standard way to run a Flask application.
# When you execute this script, the `if __name__ == '__main__':` block will be executed.
# It will start the Flask development server.
if __name__ == '__main__':
    # We run the app in debug mode, which provides helpful error messages.
    # The server will listen on all available network interfaces (0.0.0.0)
    # and on port 5000.
    app.run(host='0.0.0.0', port=5000, debug=True)

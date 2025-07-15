from flask import Flask, request, jsonify, send_from_directory
import os

# We import the components from our other files.
from tools import initialize_mcp_components
from prompts import format_prompt

# We create an instance of the Flask class. This `app` object will be our server.
app = Flask(__name__)

# Initialize MCP components using the new organized structure
resource_registry, prompt_registry, tool_registry = initialize_mcp_components()

# Get the organized tools from the registry
tools = tool_registry.get_tools_dict()

# ---
# ## UI Endpoint: Serve the Visual Walkthrough
#
# This endpoint serves the beautiful UI for the visual walkthrough
@app.route('/ui')
def ui_walkthrough():
    """
    Serves the visual walkthrough UI
    """
    return send_from_directory('ui', 'index.html')

# Serve static files from the UI directory
@app.route('/app.js')
def serve_app_js():
    """
    Serves the app.js file for the UI
    """
    return send_from_directory('ui', 'app.js')

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
    return """
    <h1>🔧 MCP Server is Running!</h1>
    <p>Welcome to the Model Context Protocol Server</p>
    <ul>
        <li><a href="/ui">🎨 Visual Walkthrough</a> - Beautiful UI tutorial</li>
        <li><a href="/capabilities">🔍 Server Capabilities</a> - Available tools and resources</li>
        <li><a href="/health">💚 Health Check</a> - Server status</li>
    </ul>
    <p>For the full tutorial, open the Jupyter notebook: <code>mcp_architecture_tutorial.ipynb</code></p>
    """

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
        
        # All MCP tools should use the standard `run` method
        try:
            result = tool.run(parameters)
            return jsonify({"success": True, "result": result})
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500
    else:
        # If the requested tool is not supported, we return an error.
        return jsonify({"error": f"Unsupported tool: {tool_name}"}), 400

# ---
# ## Endpoint 3: The Capabilities Endpoint (`/capabilities`)
#
# This endpoint returns information about the server's capabilities,
# including available tools and their parameters.
#
@app.route('/capabilities', methods=['GET'])
def capabilities_handler():
    """
    Returns server capabilities and available tools.
    """
    # Get tools info from tool registry
    tools_info = tool_registry.list_tools()
    
    # Get available prompts from prompt registry
    prompts_info = prompt_registry.list_prompts()
    
    # Get available resources from resource registry
    resources_info = resource_registry.list_resources()
    
    capabilities = {
        "server_version": "1.0.0",
        "server_name": "MCP Server Tutorial",
        "description": "A tutorial MCP server providing organized tools, resources, and prompts",
        "tools": tools_info,
        "prompts": prompts_info,
        "resources": resources_info,
        "supported_endpoints": [
            "/",
            "/mcp",
            "/capabilities",
            "/prompt",
            "/health"
        ]
    }
    return jsonify(capabilities)

# ---
# ## Endpoint 4: The Health Check Endpoint (`/health`)
#
# This endpoint provides health information about the server and its dependencies.
#
@app.route('/health', methods=['GET'])
def health_handler():
    """
    Returns health status of the server and its dependencies.
    """
    # Check API configurations
    gemini_configured = bool(os.getenv('GEMINI_API_KEY'))
    brave_configured = bool(os.getenv('BRAVE_SEARCH_API_KEY'))
    
    # Check tool registry health
    available_tools = tool_registry.list_tools()
    tool_health = {name: "ready" for name in available_tools.keys()}
    
    health_status = {
        "status": "healthy",
        "timestamp": __import__('datetime').datetime.now().isoformat(),
        "version": "1.0.0",
        "components": {
            "tool_registry": f"{len(available_tools)} tools available",
            "prompt_registry": f"{len(prompt_registry.list_prompts())} prompts available",
            "resource_registry": f"{len(resource_registry.list_resources())} resources available"
        },
        "api_checks": {
            "gemini_api": "configured" if gemini_configured else "not_configured",
            "brave_search_api": "configured" if brave_configured else "not_configured"
        },
        "tools": tool_health
    }
    
    return jsonify(health_status)

# ---
# ## Endpoint 5: The Prompting Endpoint (`/prompt`)
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

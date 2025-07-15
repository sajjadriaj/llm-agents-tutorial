# tools.py - MCP Server Tools and Registries
#
# This file contains the organized components for the MCP server:
# - ToolRegistry: Manages all available tools
# - ResourceRegistry: Manages server resources 
# - PromptRegistry: Manages common prompts
# - Individual tool classes following MCP standards
#
# In proper MCP architecture:
# - Server provides tools and resources
# - Agents are implemented on the CLIENT side
# - Server should NOT contain agents

import os
import json
import requests
import wikipedia
import google.generativeai as genai
from typing import Dict, Any, List, Optional

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("✅ Environment variables loaded from .env file")
except ImportError:
    print("⚠️  python-dotenv not installed. Install with: pip install python-dotenv")
    print("   Falling back to system environment variables")
except Exception as e:
    print(f"⚠️  Could not load .env file: {e}")
    print("   Falling back to system environment variables")

# =============================================================================
# RESOURCE REGISTRY
# =============================================================================

class ResourceRegistry:
    """
    Registry for managing server resources like files, data, and configurations.
    """
    
    def __init__(self):
        self.resources = {}
        self.file_cache = {}
    
    def register_resource(self, name: str, resource_type: str, location: str):
        """Register a new resource"""
        self.resources[name] = {
            "type": resource_type,
            "location": location,
            "accessed": 0
        }
    
    def get_resource(self, name: str) -> Dict[str, Any]:
        """Get resource information"""
        if name in self.resources:
            self.resources[name]["accessed"] += 1
            return self.resources[name]
        return None
    
    def list_resources(self) -> Dict[str, Dict[str, Any]]:
        """List all available resources"""
        return self.resources.copy()
    
    def read_file_resource(self, filename: str) -> str:
        """Read a file resource with caching"""
        if filename in self.file_cache:
            return self.file_cache[filename]
        
        # Try to find the file in registered resources
        for name, resource in self.resources.items():
            if resource["type"] == "file" and resource["location"].endswith(filename):
                try:
                    with open(resource["location"], 'r', encoding='utf-8') as f:
                        content = f.read()
                        self.file_cache[filename] = content
                        return content
                except Exception as e:
                    raise Exception(f"Error reading file {filename}: {str(e)}")
        
        raise Exception(f"File not found: {filename}")

# =============================================================================
# PROMPT REGISTRY
# =============================================================================

class PromptRegistry:
    """
    Registry for managing common prompts and templates.
    """
    
    def __init__(self):
        self.prompts = {
            "fact_extraction": {
                "template": "Extract key facts from the following text: {text}",
                "description": "Extracts factual information from text"
            },
            "sentiment_analysis": {
                "template": "Analyze the sentiment of the following text: {text}",
                "description": "Analyzes emotional tone and sentiment"
            },
            "summarization": {
                "template": "Summarize the following text in {max_sentences} sentences: {text}",
                "description": "Creates concise summaries of text"
            },
            "question_answering": {
                "template": "Answer the following question based on the context: Question: {question}\nContext: {context}",
                "description": "Answers questions using provided context"
            },
            "web_search_analysis": {
                "template": "Analyze the following web search results for query '{query}':\n{results}",
                "description": "Analyzes web search results"
            }
        }
    
    def get_prompt(self, name: str) -> Dict[str, str]:
        """Get a prompt template by name"""
        return self.prompts.get(name, {})
    
    def format_prompt(self, name: str, **kwargs) -> str:
        """Format a prompt template with provided variables"""
        prompt_info = self.get_prompt(name)
        if not prompt_info:
            raise ValueError(f"Prompt '{name}' not found")
        
        template = prompt_info.get("template", "")
        try:
            return template.format(**kwargs)
        except KeyError as e:
            raise ValueError(f"Missing required variable {e} for prompt '{name}'")
    
    def list_prompts(self) -> Dict[str, Dict[str, str]]:
        """List all available prompts"""
        return self.prompts.copy()
    
    def register_prompt(self, name: str, template: str, description: str):
        """Register a new prompt template"""
        self.prompts[name] = {
            "template": template,
            "description": description
        }

# =============================================================================
# TOOL REGISTRY
# =============================================================================

class ToolRegistry:
    """
    Registry for managing all available MCP tools.
    """
    
    def __init__(self, resource_registry: ResourceRegistry, prompt_registry: PromptRegistry):
        self.resource_registry = resource_registry
        self.prompt_registry = prompt_registry
        self.tools = {}
        self._initialize_default_tools()
    
    def _initialize_default_tools(self):
        """Initialize default MCP tools"""
        # Register core tools
        self.register_tool("file_reader", FileReaderTool(self.resource_registry))
        self.register_tool("web_search", WebSearchTool())
        self.register_tool("wikipedia", WikipediaTool())
        self.register_tool("llm", LLMTool(self.prompt_registry))
        self.register_tool("prompt_formatter", PromptFormatterTool(self.prompt_registry))
    
    def register_tool(self, name: str, tool_instance):
        """Register a new tool"""
        self.tools[name] = tool_instance
    
    def get_tool(self, name: str):
        """Get a tool by name"""
        return self.tools.get(name)
    
    def list_tools(self) -> Dict[str, Dict[str, Any]]:
        """List all available tools with their capabilities"""
        tool_info = {}
        for name, tool in self.tools.items():
            tool_info[name] = {
                "description": getattr(tool, "description", "No description available"),
                "parameters": getattr(tool, "parameters", {}),
                "methods": [method for method in dir(tool) if not method.startswith('_') and callable(getattr(tool, method))]
            }
        return tool_info
    
    def get_tools_dict(self) -> Dict[str, Any]:
        """Get tools dictionary for Flask app"""
        return self.tools.copy()

# =============================================================================
# INDIVIDUAL TOOL CLASSES
# =============================================================================

class FileReaderTool:
    """
    MCP tool for reading files from server resources.
    """
    
    description = "Read files from the server's resource directory"
    parameters = {
        "filename": "string - name of the file to read"
    }
    
    def __init__(self, resource_registry: ResourceRegistry):
        self.resource_registry = resource_registry
    
    def run(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Read a file from server resources.
        
        Args:
            parameters: Dictionary containing 'filename' parameter
            
        Returns:
            Dictionary with success status and file content or error message
        """
        filename = parameters.get('filename')
        if not filename:
            return {"success": False, "error": "Missing 'filename' parameter"}
        
        try:
            content = self.resource_registry.read_file_resource(filename)
            return {"success": True, "content": content}
        except Exception as e:
            return {"success": False, "error": str(e)}

class WebSearchTool:
    """
    MCP tool for searching the web using Brave Search API.
    """
    
    description = "Search the web using Brave Search API"
    parameters = {
        "query": "string - search query",
        "count": "integer - number of results (optional, default 5)"
    }
    
    def __init__(self):
        self.api_key = os.getenv('BRAVE_SEARCH_API_KEY')
        self.base_url = "https://api.search.brave.com/res/v1/web/search"
    
    def run(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Search the web using Brave Search API.
        
        Args:
            parameters: Dictionary containing 'query' and optional 'count' parameters
            
        Returns:
            Dictionary with search results or error message
        """
        query = parameters.get('query')
        count = parameters.get('count', 5)
        
        if not query:
            return {"success": False, "error": "Missing 'query' parameter"}
        
        if not self.api_key:
            return {"success": False, "error": "Brave Search API key not configured"}
        
        try:
            headers = {
                "Accept": "application/json",
                "Accept-Encoding": "gzip",
                "X-Subscription-Token": self.api_key
            }
            
            params = {
                "q": query,
                "count": count
            }
            
            response = requests.get(self.base_url, headers=headers, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            results = []
            if 'web' in data and 'results' in data['web']:
                for result in data['web']['results']:
                    results.append({
                        "title": result.get('title', ''),
                        "url": result.get('url', ''),
                        "description": result.get('description', '')
                    })
            
            return {"success": True, "results": results}
            
        except Exception as e:
            return {"success": False, "error": f"Web search failed: {str(e)}"}

class WikipediaTool:
    """
    MCP tool for searching Wikipedia.
    """
    
    description = "Search Wikipedia for information"
    parameters = {
        "query": "string - search query",
        "sentences": "integer - number of sentences to return (optional, default 3)"
    }
    
    def run(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Search Wikipedia for information.
        
        Args:
            parameters: Dictionary containing 'query' and optional 'sentences' parameters
            
        Returns:
            Dictionary with Wikipedia content or error message
        """
        query = parameters.get('query')
        sentences = parameters.get('sentences', 3)
        
        if not query:
            return {"success": False, "error": "Missing 'query' parameter"}
        
        try:
            # Search for pages
            search_results = wikipedia.search(query, results=5)
            
            if not search_results:
                return {"success": False, "error": "No Wikipedia articles found"}
            
            # Get the first result
            page = wikipedia.page(search_results[0])
            
            # Get summary with specified number of sentences
            summary = wikipedia.summary(search_results[0], sentences=sentences)
            
            return {
                "success": True,
                "title": page.title,
                "summary": summary,
                "url": page.url
            }
            
        except wikipedia.exceptions.DisambiguationError as e:
            # Handle disambiguation pages
            try:
                page = wikipedia.page(e.options[0])
                summary = wikipedia.summary(e.options[0], sentences=sentences)
                
                return {
                    "success": True,
                    "title": page.title,
                    "summary": summary,
                    "url": page.url
                }
            except Exception as inner_e:
                return {"success": False, "error": f"Wikipedia disambiguation error: {str(inner_e)}"}
                
        except Exception as e:
            return {"success": False, "error": f"Wikipedia search failed: {str(e)}"}

class LLMTool:
    """
    MCP tool for generating text using LLM (Gemini).
    """
    
    description = "Generate text using LLM (Gemini)"
    parameters = {
        "prompt": "string - prompt for the LLM",
        "max_tokens": "integer - maximum tokens to generate (optional)"
    }
    
    def __init__(self, prompt_registry: PromptRegistry = None):
        self.prompt_registry = prompt_registry
        self.api_key = os.getenv('GEMINI_API_KEY')
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-2.0-flash')
        else:
            self.model = None
    
    def run(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate text using LLM.
        
        Args:
            parameters: Dictionary containing 'prompt' and optional 'max_tokens' parameters
            
        Returns:
            Dictionary with generated text or error message
        """
        prompt = parameters.get('prompt')
        max_tokens = parameters.get('max_tokens', 1000)
        
        if not prompt:
            return {"success": False, "error": "Missing 'prompt' parameter"}
        
        if not self.model:
            return {"success": False, "error": "Gemini API key not configured"}
        
        try:
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=max_tokens
                )
            )
            
            # Check if response is valid
            if not response or not hasattr(response, 'text') or not response.text:
                return {"success": False, "error": "Empty response from LLM"}
            
            return {
                "success": True,
                "text": response.text.strip(),
                "usage": {
                    "prompt_tokens": response.usage_metadata.prompt_token_count if response.usage_metadata else 0,
                    "completion_tokens": response.usage_metadata.candidates_token_count if response.usage_metadata else 0,
                    "total_tokens": response.usage_metadata.total_token_count if response.usage_metadata else 0
                }
            }
            
        except Exception as e:
            return {"success": False, "error": f"LLM generation failed: {str(e)}"}

class PromptFormatterTool:
    """
    MCP tool for formatting prompts using registered templates.
    """
    
    description = "Format prompts using registered templates"
    parameters = {
        "template_name": "string - name of the prompt template",
        "variables": "object - variables to substitute in template"
    }
    
    def __init__(self, prompt_registry: PromptRegistry):
        self.prompt_registry = prompt_registry
    
    def run(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Format a prompt using a registered template.
        
        Args:
            parameters: Dictionary containing 'template_name' and 'variables' parameters
            
        Returns:
            Dictionary with formatted prompt or error message
        """
        template_name = parameters.get('template_name')
        variables = parameters.get('variables', {})
        
        if not template_name:
            return {"success": False, "error": "Missing 'template_name' parameter"}
        
        try:
            formatted_prompt = self.prompt_registry.format_prompt(template_name, **variables)
            return {"success": True, "formatted_prompt": formatted_prompt}
        except Exception as e:
            return {"success": False, "error": str(e)}

# =============================================================================
# INITIALIZATION FUNCTION
# =============================================================================

def initialize_mcp_components():
    """
    Initialize all MCP components in the correct order.
    
    Returns:
        Tuple of (resource_registry, prompt_registry, tool_registry)
    """
    # Initialize registries
    resource_registry = ResourceRegistry()
    prompt_registry = PromptRegistry()
    tool_registry = ToolRegistry(resource_registry, prompt_registry)
    
    # Register some default resources (example)
    resource_registry.register_resource(
        "sample_text", 
        "file", 
        "/home/sajjad/workspace/tutorials/mcp-server/resources/sample.txt"
    )
    
    return resource_registry, prompt_registry, tool_registry

# Export the main classes and functions
__all__ = [
    'ResourceRegistry',
    'PromptRegistry', 
    'ToolRegistry',
    'FileReaderTool',
    'WebSearchTool',
    'WikipediaTool',
    'LLMTool',
    'PromptFormatterTool',
    'initialize_mcp_components'
]

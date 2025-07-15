# client_agents.py - Client-side Agents for MCP Server
#
# This file contains client-side agents that use the MCP server's tools and resources.
# This follows proper MCP architecture where:
# - Server provides tools and resources
# - Agents are implemented on the CLIENT side
# - Agents use server tools to accomplish tasks

import json
import requests
import os
import google.generativeai as genai
from typing import Dict, Any, List, Optional

# Configure Gemini API for client-side agents
gemini_api_key = os.getenv('GEMINI_API_KEY')
if gemini_api_key:
    genai.configure(api_key=gemini_api_key)
    gemini_model = genai.GenerativeModel('gemini-2.0-flash')
else:
    gemini_model = None

# =============================================================================
# MCP CLIENT
# =============================================================================

class MCPClient:
    """
    Client for communicating with the MCP server.
    """
    
    def __init__(self, server_url: str = "http://localhost:5000"):
        self.server_url = server_url
        self.session = requests.Session()
    
    def send_request(self, endpoint: str, data: Dict[str, Any], print_request: bool = False) -> Dict[str, Any]:
        """Send a request to the MCP server"""
        try:
            if endpoint.startswith('/'):
                url = f"{self.server_url}{endpoint}"
            else:
                url = f"{self.server_url}/{endpoint}"
            
            # Print request details if requested
            if print_request:
                print(f"📡 Making request to: {url}")
                if endpoint not in ['/health', '/capabilities']:
                    print(f"📝 Request data: {json.dumps(data, indent=2)}")
            
            if endpoint in ['/health', '/capabilities']:
                response = self.session.get(url)
            else:
                response = self.session.post(url, json=data)
            
            response.raise_for_status()
            result = response.json()
            
            # Print response if requested
            if print_request:
                print(f"📬 Response: {json.dumps(result, indent=2)}")
            
            return result
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_capabilities(self, print_request: bool = False) -> Dict[str, Any]:
        """Get server capabilities"""
        return self.send_request('/capabilities', {}, print_request)
    
    def check_health(self, print_request: bool = False) -> Dict[str, Any]:
        """Check server health"""
        return self.send_request('/health', {}, print_request)
    
    def use_tool(self, tool_name: str, parameters: Dict[str, Any], print_request: bool = False) -> Dict[str, Any]:
        """Use a tool on the MCP server"""
        return self.send_request('/mcp', {
            "tool": tool_name,
            "parameters": parameters
        }, print_request)

    def get_available_tools(self) -> List[str]:
        """Get list of available tools"""
        capabilities = self.get_capabilities()
        return list(capabilities.get('tools', {}).keys())
    
    def call_tool(self, tool_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Call a tool and return the result data directly"""
        result = self.use_tool(tool_name, parameters)
        if result.get('success'):
            return result.get('result', {})
        else:
            print(f"❌ Tool '{tool_name}' failed: {result.get('error', 'Unknown error')}")
            return None
    
    def print_tool_info(self, tool_name: str):
        """Print information about a specific tool"""
        capabilities = self.get_capabilities()
        if tool_name in capabilities.get('tools', {}):
            tool_info = capabilities['tools'][tool_name]
            print(f"🔧 Tool: {tool_name}")
            print(f"📝 Description: {tool_info.get('description', 'No description')}")
            print(f"📋 Parameters:")
            for param_name, param_desc in tool_info.get('parameters', {}).items():
                print(f"  • {param_name}: {param_desc}")
        else:
            print(f"❌ Tool '{tool_name}' not found")

# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def extract_and_parse_json(text: str) -> Optional[Dict]:
    """Extract and parse JSON from text response"""
    try:
        # Remove markdown code block markers if present
        text = text.strip()
        if text.startswith('```json'):
            text = text[7:]
        if text.startswith('```'):
            text = text[3:]
        if text.endswith('```'):
            text = text[:-3]
        
        text = text.strip()
        
        # Check if text is empty
        if not text:
            print("JSON parsing error: Empty response")
            return None
        
        # Try to find JSON in the text if it's mixed with other content
        json_start = text.find('{')
        json_end = text.rfind('}')
        
        if json_start != -1 and json_end != -1 and json_end > json_start:
            json_text = text[json_start:json_end + 1]
            return json.loads(json_text)
        
        # If no JSON brackets found, try parsing the whole text
        return json.loads(text)
        
    except Exception as e:
        print(f"JSON parsing error: {e}")
        print(f"Raw text: {repr(text)}")
        return None

def process_with_llm(prompt: str) -> str:
    """Process a prompt with LLM"""
    if not gemini_model:
        return "Error: Gemini API not configured. Please set GEMINI_API_KEY environment variable."
    
    try:
        response = gemini_model.generate_content(prompt)
        
        # Check if response is valid
        if not response or not hasattr(response, 'text') or not response.text:
            return "Error: Empty response from LLM"
        
        return response.text.strip()
    except Exception as e:
        return f"Error processing query: {str(e)}"

# =============================================================================
# CLIENT-SIDE AGENTS
# =============================================================================

class BaseAgent:
    """Base class for client-side agents"""
    
    def __init__(self, name: str, instructions: str, mcp_client: MCPClient = None):
        self.name = name
        self.instructions = instructions
        self.mcp_client = mcp_client or MCPClient()
    
    def process_with_llm(self, prompt: str) -> str:
        """Process query with agent-specific instructions"""
        full_prompt = f"{self.instructions}\n\nQuery: {prompt}"
        return process_with_llm(full_prompt)

class FactExtractorAgent(BaseAgent):
    """Client-side agent for extracting facts using MCP server tools"""
    
    def __init__(self, mcp_client: MCPClient = None):
        super().__init__(
            "FactExtractor",
            "You are a fact extraction agent. Extract key facts and information from text.",
            mcp_client
        )
    
    def extract_facts(self, text: str) -> Dict[str, Any]:
        """Extract facts from text using local LLM processing"""
        prompt = (
            f"Extract all salient factual information from the following text: '{text}'. "
            "Identify distinct factual statements, key entities mentioned, and provide a concise summary of the factual content. "
            "Your response MUST be a JSON object containing ONLY the following keys: "
            "'facts' (as a list of strings, each a distinct factual statement), "
            "'entities' (as a list of relevant entities mentioned, e.g., people, organizations, dates, locations), "
            "'statistics' (a list of numerical data or statistics extracted), "
            "'summary' (a brief summary of the extracted facts), "
            "'key_points' (a list of key points derived from the facts). "
            "DO NOT include any additional text, explanations, or Markdown formatting (like ```json)."
            f"\n\nExample desired format (values are illustrative): {{"
            f"\"facts\": ["
            f"    \"The Eiffel Tower is located in Paris, France.\","
            f"    \"It was completed in 1889.\","
            f"    \"Gustave Eiffel's company designed it.\""
            f"],"
            f"\"entities\": [\"Eiffel Tower\", \"Paris\", \"France\", \"1889\", \"Gustave Eiffel\"],"
            f"\"summary\": \"Key facts about the Eiffel Tower, including its location, completion date, and designer.\","
            f"}}"
        )
        
        response = self.process_with_llm(prompt)
        
        # Check if response is an error
        if response.startswith("Error:"):
            return {"error": response}
        
        parsed_result = extract_and_parse_json(response)
        if parsed_result is None:
            return {
                "error": "Failed to parse response",
                "raw_response": response,
                "fallback_facts": [text]  # Provide fallback
            }
        
        return parsed_result
    
    def extract_facts_with_research(self, query: str) -> Dict[str, Any]:
        """Extract facts with additional research using MCP server tools"""
        # Step 1: Use web search tool to gather information
        web_search_result = self.mcp_client.use_tool("web_search", {
            "query": query,
            "count": 3
        })
        
        # Step 2: Use Wikipedia tool for additional context
        wikipedia_result = self.mcp_client.use_tool("wikipedia", {
            "query": query,
            "sentences": 5
        })
        
        # Step 3: Combine results and extract facts
        combined_text = f"Web search results: {web_search_result}\n\nWikipedia: {wikipedia_result}"
        
        prompt = (
            f"Based on the following research results about '{query}', extract key facts:\n\n"
            f"Extract all salient factual information from the following text: '{combined_text}'. "
            "Identify distinct factual statements, key entities mentioned, and provide a concise summary of the factual content. "
            "Your response MUST be a JSON object containing ONLY the following keys: "
            "'facts' (as a list of strings, each a distinct factual statement), "
            "'entities' (as a list of relevant entities mentioned, e.g., people, organizations, dates, locations), "
            "'statistics' (a list of numerical data or statistics extracted), "
            "'summary' (a brief summary of the extracted facts), "
            "'key_points' (a list of key points derived from the facts). "
            "DO NOT include any additional text, explanations, or Markdown formatting (like ```json)."
            f"\n\nExample desired format (values are illustrative): {{"
            f"\"facts\": ["
            f"    \"The Eiffel Tower is located in Paris, France.\","
            f"    \"It was completed in 1889.\","
            f"    \"Gustave Eiffel's company designed it.\""
            f"],"
            f"\"entities\": [\"Eiffel Tower\", \"Paris\", \"France\", \"1889\", \"Gustave Eiffel\"],"
            f"\"summary\": \"Key facts about the Eiffel Tower, including its location, completion date, and designer.\","
            f"}}"
        )
        
        response = self.process_with_llm(prompt)
        result = extract_and_parse_json(response) or {"error": "Failed to parse response"}
        
        # Add metadata about tools used
        result["tools_used"] = ["web_search", "wikipedia"]
        result["research_data"] = {
            "web_search": web_search_result,
            "wikipedia": wikipedia_result
        }
        
        return result

class SentimentAnalyzerAgent(BaseAgent):
    """Client-side agent for analyzing sentiment using MCP server tools"""
    
    def __init__(self, mcp_client: MCPClient = None):
        super().__init__(
            "SentimentAnalyzer",
            "You are a sentiment analysis agent. Analyze emotional tone and sentiment in text.",
            mcp_client
        )
    
    def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """Analyze sentiment of text using local LLM processing"""
        prompt = (
            f"Analyze the sentiment of the following text: '{text}'. "
            "Return the primary sentiment as 'positive', 'negative', or 'neutral', "
            "along with an overall confidence score. "
            "Also, identify the specific emotional 'tone(s)' present (e.g., 'joy', 'anger', 'sadness', 'excitement') "
            "and provide a 'justification' explaining why that sentiment was assigned, "
            "citing specific parts of the text if possible. "
            "Your response MUST be a JSON object containing ONLY the following keys: "
            "'sentiment', 'confidence', 'tone' (as a list of strings), and 'justification'. "
            "DO NOT include any additional text, explanations, or Markdown formatting (like ```json)."
            f"\n\nExample desired format (values are illustrative): {{"
            f"\"sentiment\": \"positive\", "
            f"\"confidence\": 0.92, "
            f"\"tone\": [\"joy\", \"excitement\"], "
            f"\"justification\": \"The user expressed enthusiasm with phrases like 'absolutely loved it' and 'highly recommend'.\""
            f"}}"
        )
        
        response = self.process_with_llm(prompt)
        
        # Check if response is an error
        if response.startswith("Error:"):
            return {"error": response}
        
        parsed_result = extract_and_parse_json(response)
        if parsed_result is None:
            return {
                "error": "Failed to parse response",
                "raw_response": response,
                "fallback_sentiment": "neutral"  # Provide fallback
            }
        
        return parsed_result
    
    def analyze_sentiment_with_context(self, text: str, research_topic: str = None) -> Dict[str, Any]:
        """Analyze sentiment with additional context from MCP server tools"""
        context_data = {}
        
        # If research topic provided, gather context
        if research_topic:
            # Use web search for current sentiment trends
            web_search_result = self.mcp_client.use_tool("web_search", {
                "query": f"{research_topic} sentiment trends opinions",
                "count": 2
            })
            
            context_data["web_search"] = web_search_result
        
        # Analyze sentiment with context
        context_str = f"Context data: {context_data}" if context_data else "No additional context"
        
        prompt = (
            f"Analyze the sentiment of the following text: '{text}'\n\n"
            f"Additional context: {context_str}\n\n"
            "Return the primary sentiment as 'positive', 'negative', or 'neutral', "
            "along with an overall confidence score. "
            "Also, identify the specific emotional 'tone(s)' present (e.g., 'joy', 'anger', 'sadness', 'excitement') "
            "and provide a 'justification' explaining why that sentiment was assigned, "
            "citing specific parts of the text if possible. "
            "Your response MUST be a JSON object containing ONLY the following keys: "
            "'sentiment', 'confidence', 'tone' (as a list of strings), and 'justification'. "
            "DO NOT include any additional text, explanations, or Markdown formatting (like ```json)."
            f"\n\nExample desired format (values are illustrative): {{"
            f"\"sentiment\": \"positive\", "
            f"\"confidence\": 0.92, "
            f"\"tone\": [\"joy\", \"excitement\"], "
            f"\"justification\": \"The user expressed enthusiasm with phrases like 'absolutely loved it' and 'highly recommend'.\""
            f"}}"
        )
        
        response = self.process_with_llm(prompt)
        result = extract_and_parse_json(response) or {"error": "Failed to parse response"}
        
        # Add metadata about tools used
        if context_data:
            result["tools_used"] = ["web_search"]
            result["context_data"] = context_data
        
        return result

class OrchestrationAgent(BaseAgent):
    """Client-side agent that coordinates other agents and MCP server tools"""
    
    def __init__(self, mcp_client: MCPClient = None):
        super().__init__(
            "Orchestrator",
            "You are an orchestration agent. Coordinate multiple agents and tools to handle complex queries.",
            mcp_client
        )
        self.fact_extractor = FactExtractorAgent(mcp_client)
        self.sentiment_analyzer = SentimentAnalyzerAgent(mcp_client)
    
    def handle_complex_query(self, query: str) -> Dict[str, Any]:
        """Handle complex queries by coordinating multiple agents and tools"""
        # Step 1: Analyze what type of processing is needed
        analysis_prompt = f"""
        Analyze this query: "{query}"
        
        Determine what type of processing is needed. Return JSON:
        {{
            "needs_fact_extraction": true/false,
            "needs_sentiment_analysis": true/false,
            "needs_web_search": true/false,
            "needs_wikipedia": true/false,
            "processing_strategy": "description of approach"
        }}
        """
        
        strategy_response = self.process_with_llm(analysis_prompt)
        strategy = extract_and_parse_json(strategy_response) or {
            "needs_fact_extraction": True,
            "needs_sentiment_analysis": False,
            "needs_web_search": False,
            "needs_wikipedia": False,
            "processing_strategy": "Default fact extraction"
        }
        
        results = {"strategy": strategy}
        
        # Step 2: Execute based on strategy
        if strategy.get("needs_web_search"):
            results["web_search"] = self.mcp_client.use_tool("web_search", {
                "query": query,
                "count": 3
            })
        
        if strategy.get("needs_wikipedia"):
            results["wikipedia"] = self.mcp_client.use_tool("wikipedia", {
                "query": query,
                "sentences": 5
            })
        
        if strategy.get("needs_fact_extraction"):
            if strategy.get("needs_web_search") or strategy.get("needs_wikipedia"):
                results["facts"] = self.fact_extractor.extract_facts_with_research(query)
            else:
                results["facts"] = self.fact_extractor.extract_facts(query)
        
        if strategy.get("needs_sentiment_analysis"):
            research_topic = query if strategy.get("needs_web_search") else None
            results["sentiment"] = self.sentiment_analyzer.analyze_sentiment_with_context(
                query, research_topic
            )
        
        # Step 3: Synthesize final response
        synthesis_prompt = f"""
        Original query: {query}
        Processing strategy: {strategy}
        Results: {json.dumps(results, indent=2)}
        
        Synthesize a comprehensive response that combines all the results.
        Return JSON with:
        {{
            "comprehensive_response": "main answer to the query",
            "key_findings": ["finding1", "finding2"],
            "confidence": 0.95,
            "sources_used": ["source1", "source2"]
        }}
        """
        
        synthesis_response = self.process_with_llm(synthesis_prompt)
        synthesis = extract_and_parse_json(synthesis_response) or {
            "comprehensive_response": "Unable to synthesize response",
            "key_findings": [],
            "confidence": 0.0,
            "sources_used": []
        }
        
        return {
            "query": query,
            "strategy": strategy,
            "detailed_results": results,
            "synthesis": synthesis
        }

# =============================================================================
# EXAMPLE USAGE
# =============================================================================

def demo_client_agents():
    """Demonstrate client-side agents using MCP server"""
    print("🤖 Client-side Agents Demo")
    print("=" * 50)
    
    # Initialize MCP client
    client = MCPClient()
    
    # Check server health
    health = client.check_health()
    print(f"Server health: {health.get('status', 'unknown')}")
    
    # Initialize agents
    fact_extractor = FactExtractorAgent(client)
    sentiment_analyzer = SentimentAnalyzerAgent(client)
    orchestrator = OrchestrationAgent(client)
    
    # Example 1: Basic fact extraction
    print("\n1. Basic Fact Extraction:")
    text = "The iPhone 15 was released in September 2023 with a starting price of $799."
    facts = fact_extractor.extract_facts(text)
    print(f"Facts: {facts}")
    
    # Example 2: Sentiment analysis
    print("\n2. Sentiment Analysis:")
    review = "I love this product! It's amazing and works perfectly."
    sentiment = sentiment_analyzer.analyze_sentiment(review)
    print(f"Sentiment: {sentiment}")
    
    # Example 3: Complex orchestrated query
    print("\n3. Complex Orchestrated Query:")
    query = "What are the latest developments in electric vehicles?"
    result = orchestrator.handle_complex_query(query)
    print(f"Orchestrated result: {result}")

if __name__ == "__main__":
    demo_client_agents()

#!/usr/bin/env python3
"""
MCP Client Demo - Proper Architecture

This script demonstrates how to interact with the MCP server using the correct architecture:
- Server provides tools and resources
- Client contains agents and business logic
- Clear separation of concerns

Usage:
    python mcp_client_demo.py           # Run all demos
    python mcp_client_demo.py interactive # Interactive mode
"""

import requests
import json
import sys
import os

# Add the current directory to Python path
sys.path.append('/home/sajjad/workspace/tutorials/mcp-server')

try:
    from client_agents import MCPClient, FactExtractorAgent, SentimentAnalyzerAgent, OrchestrationAgent
    AGENTS_AVAILABLE = True
except ImportError:
    AGENTS_AVAILABLE = False
    print("⚠️ Client agents not available. Some demos will be skipped.")

def demo_direct_tools(client: MCPClient):
    """Demonstrate direct tool usage (server-side tools)"""
    print("\n" + "="*50)
    print("🔧 DIRECT TOOL USAGE (Server-side)")
    print("="*50)
    
    # 1. Web Search Tool
    print("\n1️⃣ Web Search Tool")
    print("-" * 30)
    
    result = client.use_tool('web_search', {
        'query': 'iPhone 15 features',
        'count': 3
    })
    
    if result.get('success'):
        results = result.get('results', [])
        print(f"🔍 Found {len(results)} results:")
        for i, res in enumerate(results[:2], 1):
            print(f"  {i}. {res.get('title', 'No title')}")
            print(f"     {res.get('description', 'No description')[:100]}...")
    else:
        print(f"❌ Error: {result.get('error', 'Unknown error')}")
    
    # 2. Wikipedia Tool
    print("\n2️⃣ Wikipedia Tool")
    print("-" * 30)
    
    result = client.use_tool('wikipedia', {
        'query': 'artificial intelligence',
        'sentences': 2
    })
    
    if result.get('success'):
        print(f"📖 Title: {result.get('title', 'No title')}")
        print(f"📝 Summary: {result.get('summary', 'No summary')[:200]}...")
    else:
        print(f"❌ Error: {result.get('error', 'Unknown error')}")
    
    # 3. LLM Tool
    print("\n3️⃣ LLM Tool")
    print("-" * 30)
    
    result = client.use_tool('llm', {
        'prompt': 'Explain MCP (Model Context Protocol) in one sentence.',
        'max_tokens': 100
    })
    
    if result.get('success'):
        print(f"💬 Response: {result.get('text', 'No response')}")
    else:
        print(f"❌ Error: {result.get('error', 'Unknown error')}")

def demo_client_agents():
    """Demonstrate client-side agents using server tools"""
    if not AGENTS_AVAILABLE:
        print("\n❌ Client agents not available. Skipping agent demos.")
        return
    
    print("\n" + "="*50)
    print("🤖 CLIENT-SIDE AGENTS (Using Server Tools)")
    print("="*50)
    
    # Initialize client and agents
    client = MCPClient()
    fact_agent = FactExtractorAgent(client)
    sentiment_agent = SentimentAnalyzerAgent(client)
    orchestrator = OrchestrationAgent(client)
    
    # 1. Fact Extraction Agent
    print("\n1️⃣ Fact Extraction Agent")
    print("-" * 30)
    
    text = "Apple released iPhone 15 in September 2023 with USB-C port, starting at $799. The A17 Pro chip delivers 20% faster performance."
    facts = fact_agent.extract_facts(text)
    
    if 'error' not in facts:
        print(f"� Facts extracted: {len(facts.get('facts', []))}")
        for fact in facts.get('facts', [])[:3]:
            print(f"  • {fact}")
        print(f"🏷️ Entities: {facts.get('entities', [])}")
    else:
        print(f"❌ Error: {facts.get('error')}")
    
    # 2. Sentiment Analysis Agent
    print("\n2️⃣ Sentiment Analysis Agent")
    print("-" * 30)
    
    review = "I absolutely love the new iPhone 15! The USB-C port is amazing and the camera quality is incredible."
    sentiment = sentiment_agent.analyze_sentiment(review)
    
    if 'error' not in sentiment:
        print(f"😊 Sentiment: {sentiment.get('sentiment', 'unknown')}")
        print(f"📈 Confidence: {sentiment.get('confidence', 0):.2f}")
        print(f"💭 Justification: {sentiment.get('justification', 'No justification')}")
    else:
        print(f"❌ Error: {sentiment.get('error')}")
    
    # 3. Fact Extraction with Research
    print("\n3️⃣ Fact Extraction with Research (Uses Server Tools)")
    print("-" * 30)
    
    query = "electric vehicles market 2024"
    research_facts = fact_agent.extract_facts_with_research(query)
    
    if 'error' not in research_facts:
        print(f"📊 Research-based facts: {len(research_facts.get('facts', []))}")
        for fact in research_facts.get('facts', [])[:3]:
            print(f"  • {fact}")
        print(f"🛠️ Tools used: {', '.join(research_facts.get('tools_used', []))}")
    else:
        print(f"❌ Error: {research_facts.get('error')}")
    
    # 4. Orchestration Agent
    print("\n4️⃣ Orchestration Agent")
    print("-" * 30)
    
    query = "What are the benefits of renewable energy and how do people feel about it?"
    result = orchestrator.handle_complex_query(query)
    
    if result:
        strategy = result.get('strategy', {})
        print(f"🎯 Processing Strategy:")
        print(f"  • Fact extraction: {strategy.get('needs_fact_extraction', False)}")
        print(f"  • Sentiment analysis: {strategy.get('needs_sentiment_analysis', False)}")
        print(f"  • Web search: {strategy.get('needs_web_search', False)}")
        
        synthesis = result.get('synthesis', {})
        print(f"💡 Response: {synthesis.get('comprehensive_response', 'No response')[:200]}...")
    else:
        print("❌ Failed to process query")

def demo_error_handling(client: MCPClient):
    """Demonstrate error handling"""
    print("\n" + "="*50)
    print("⚠️ ERROR HANDLING DEMONSTRATION")
    print("="*50)
    
    # Test with invalid tool
    print("\n1️⃣ Testing invalid tool...")
    result = client.use_tool('nonexistent_tool', {'param': 'value'})
    print(f"📋 Response: {result}")
    
    # Test with missing parameters
    print("\n2️⃣ Testing missing parameters...")
    result = client.use_tool('web_search', {})
    print(f"📋 Response: {result}")
    
    # Test with invalid parameters
    print("\n3️⃣ Testing invalid parameters...")
    result = client.use_tool('llm', {'wrong_param': 'value'})
    print(f"📋 Response: {result}")

def interactive_mode(client: MCPClient):
    """Interactive mode for testing"""
    print("\n" + "="*50)
    print("🎮 INTERACTIVE MODE")
    print("="*50)
    print("Available commands:")
    print("  • tools - List available tools")
    print("  • capabilities - Show server capabilities")
    print("  • health - Check server health")
    print("  • call <tool_name> - Call a tool interactively")
    print("  • quit - Exit interactive mode")
    
    while True:
        try:
            command = input("\n🎮 Enter command: ").strip().lower()
            
            if command == 'quit':
                break
            elif command == 'tools':
                capabilities = client.get_capabilities()
                if capabilities.get('tools'):
                    print("🔧 Available tools:")
                    for tool_name, tool_info in capabilities['tools'].items():
                        print(f"  • {tool_name}: {tool_info.get('description', 'No description')}")
                else:
                    print("❌ No tools available")
            elif command == 'capabilities':
                capabilities = client.get_capabilities()
                print(f"📊 Server capabilities: {json.dumps(capabilities, indent=2)}")
            elif command == 'health':
                health = client.check_health()
                print(f"💚 Server health: {json.dumps(health, indent=2)}")
            elif command.startswith('call '):
                tool_name = command[5:].strip()
                capabilities = client.get_capabilities()
                
                if tool_name in capabilities.get('tools', {}):
                    tool_info = capabilities['tools'][tool_name]
                    params = {}
                    
                    print(f"🔧 Calling tool: {tool_name}")
                    print(f"📝 Description: {tool_info.get('description', 'No description')}")
                    
                    for param_name, param_desc in tool_info.get('parameters', {}).items():
                        value = input(f"Enter {param_name} ({param_desc}): ").strip()
                        params[param_name] = value
                    
                    result = client.use_tool(tool_name, params)
                    print(f"📋 Result: {json.dumps(result, indent=2)}")
                else:
                    print(f"❌ Tool '{tool_name}' not available")
            else:
                print("❌ Unknown command")
                
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"❌ Error: {e}")

def main():
    """Main function"""
    print("🚀 MCP Client Demo - Proper Architecture")
    print("=" * 50)
    print("This demo shows the correct MCP architecture:")
    print("• Server provides tools and resources")
    print("• Client contains agents and business logic")
    print("• Clear separation of concerns")
    print()
    
    # Initialize client
    try:
        client = MCPClient()
    except SystemExit:
        print("❌ Cannot connect to server. Please start the server first:")
        print("   python mcp_server_tutorial.py")
        return
    
    # Show server info
    capabilities = client.get_capabilities()
    if capabilities.get('tools'):
        print(f"🔧 Server has {len(capabilities['tools'])} tools available")
        print(f"   Tools: {', '.join(capabilities['tools'].keys())}")
    
    # Run demonstrations
    if len(sys.argv) > 1 and sys.argv[1] == 'interactive':
        interactive_mode(client)
    else:
        demo_direct_tools(client)
        demo_client_agents()
        demo_error_handling(client)
        
        print("\n" + "="*50)
        print("✅ Demo completed!")
        print("💡 Run with 'interactive' argument for interactive mode")
        print("   Example: python mcp_client_demo.py interactive")
        print()
        print("🎯 Key Takeaways:")
        print("• Server provides tools (web_search, wikipedia, llm, etc.)")
        print("• Client agents use server tools to accomplish tasks")
        print("• Proper separation keeps code organized and maintainable")

if __name__ == "__main__":
    main()

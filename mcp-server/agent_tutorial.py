# MCP Agent Tutorial: Using the MCP Server with Gemini
#
# Welcome to the MCP Agent Tutorial!
#
# This file contains a simple agent that demonstrates how to interact with our MCP server
# and use the Gemini API to process the data.
#
# ---
#
# ## Setup and Installation
#
# Before you can run this agent, you need to have the following libraries installed:
#
# pip install requests google-generativeai
#
# You also need to have your Gemini API key set as an environment variable named `GEMINI_API_KEY`.
#
# export GEMINI_API_KEY="YOUR_API_KEY"
#
# ---
#
# ## Running the Agent
#
# To run the agent, first make sure the MCP server is running in a separate terminal:
#
# python mcp_server_tutorial.py
#
# Then, run this agent script in another terminal:
#
# python agent_tutorial.py
#
# The agent will then interact with the MCP server and the Gemini API, and print the result.
#
# ---

import os
import requests
import google.generativeai as genai

# --- Configuration ---

# The base URL of our MCP server.
MCP_SERVER_URL = "http://127.0.0.1:5000"

# Configure the Gemini API with the API key from the environment variable.
try:
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
except AttributeError:
    print("Error: The GEMINI_API_KEY environment variable is not set.")
    print("Please set the environment variable and try again.")
    exit()

# Create a Gemini model instance.
model = genai.GenerativeModel('gemini-pro')

# --- Agent Logic ---

def run_agent():
    """
    This function contains the main logic of our agent.
    """
    print("MCP Agent started.")

    # 1. Use the MCP server to read a file.
    print("\nStep 1: Reading a file from the MCP server...")
    try:
        response = requests.post(
            f"{MCP_SERVER_URL}/mcp",
            json={"tool": "file_reader", "parameters": {"filename": "example.txt"}}
        )
        response.raise_for_status()  # Raise an exception for bad status codes
        file_content = response.json().get("content")
        if not file_content:
            print(f"Error reading file: {response.json().get('error')}")
            return
        print(f"Successfully read file content: {file_content}")
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to MCP server: {e}")
        return

    # 2. Get a prompt template from the MCP server.
    print("\nStep 2: Getting a prompt template from the MCP server...")
    try:
        response = requests.post(
            f"{MCP_SERVER_URL}/mcp",
            json={"tool": "file_reader", "parameters": {"filename": "prompt.txt"}}
        )
        response.raise_for_status()
        prompt_template = response.json().get("content")
        if not prompt_template:
            print(f"Error getting prompt template: {response.json().get('error')}")
            return
        print(f"Successfully got prompt template: {prompt_template}")
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to MCP server: {e}")
        return

    # 3. Format the prompt using the MCP server.
    print("\nStep 3: Formatting the prompt using the MCP server...")
    try:
        response = requests.post(
            f"{MCP_SERVER_URL}/prompt",
            json={"prompt_template": prompt_template, "text": file_content}
        )
        response.raise_for_status()
        formatted_prompt = response.json().get("formatted_prompt")
        if not formatted_prompt:
            print(f"Error formatting prompt: {response.json().get('error')}")
            return
        print(f"Successfully formatted prompt: {formatted_prompt}")
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to MCP server: {e}")
        return

    # 4. Use the Gemini API to get a response.
    print("\nStep 4: Sending the prompt to the Gemini API...")
    try:
        gemini_response = model.generate_content(formatted_prompt)
        print("\n--- Gemini API Response ---")
        print(gemini_response.text)
        print("---------------------------")
    except Exception as e:
        print(f"Error calling Gemini API: {e}")

if __name__ == "__main__":
    run_agent()

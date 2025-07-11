# MCP Server Tutorial: Prompts
#
# This file is responsible for managing and formatting prompts that are sent to the AI model.
# In a real-world application, this could involve more complex logic for selecting and
# formatting prompts based on the user's input and the current context.

def format_prompt(prompt_template, text):
    """
    Formats a prompt template with the given text.
    Args:
        prompt_template: The prompt template, which should contain a {text} placeholder.
        text: The text to insert into the prompt template.
    Returns:
        The formatted prompt.
    """
    return prompt_template.format(text=text)

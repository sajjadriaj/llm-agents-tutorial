# MCP Server Tutorial: Resources
#
# This file defines the resources that our MCP server can access.
# Resources can be anything that the tools need to function, such as
# databases, APIs, or, in our case, a simple dictionary of mock files.

class ResourceManager:
    """
    Manages the resources available to the MCP server.
    """
    def __init__(self):
        """
        Initializes the resource manager with a set of mock files.
        """
        self.mock_files = {
            "example.txt": "This is the content of example.txt.",
            "another_file.md": "This is a markdown file with some content.",
            "prompt.txt": "Summarize the following text: {text}"
        }

    def get_file(self, filename):
        """
        Retrieves the content of a file from the mock files.
        Args:
            filename: The name of the file to retrieve.
        Returns:
            The content of the file, or None if the file is not found.
        """
        return self.mock_files.get(filename)

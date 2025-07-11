# MCP Server Tutorial: Tools
#
# This file defines the tools that our MCP server can use.
# In a real-world MCP server, you would have a variety of tools for different purposes,
# such as interacting with APIs, databases, or the local filesystem.
#
# For this tutorial, we will create a simple "file reader" tool.

class FileReaderTool:
    """
    A tool for reading files from a given set of resources.
    """
    def __init__(self, resources):
        """
        Initializes the tool with a set of resources.
        Args:
            resources: An object that provides access to the available resources.
        """
        self.resources = resources

    def run(self, parameters):
        """
        Runs the tool with the given parameters.
        Args:
            parameters: A dictionary of parameters for the tool.
                      For this tool, it should contain a "filename" key.
        Returns:
            A dictionary containing the result of the tool's execution.
        """
        filename = parameters.get('filename')
        if not filename:
            return {"error": "Missing 'filename' parameter"}

        content = self.resources.get_file(filename)
        if content is not None:
            return {"content": content}
        else:
            return {"error": f"File not found: {filename}"}

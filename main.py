# server.py
import importlib.util
import os

from fastmcp import FastMCP

mcp = FastMCP("Local MCP Tools")

# Dynamically load all tool scripts from the tools directory
TOOLS_DIR = os.path.join(os.path.dirname(__file__), "tools")
for filename in os.listdir(TOOLS_DIR):
    if filename.endswith(".py") and not filename.startswith("__"):
        module_name = filename[:-3]
        module_path = os.path.join(TOOLS_DIR, filename)
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        if spec is not None and spec.loader is not None:
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            # Register all functions in the module as mcp tools if they don't start with _
            for attr in dir(module):
                if not attr.startswith("_") and callable(getattr(module, attr)):
                    mcp.tool()(getattr(module, attr))


if __name__ == "__main__":
    mcp.run()

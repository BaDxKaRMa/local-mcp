# MCP Local Server

This project sets up a local MCP (Modular Command Platform) server using FastMCP.

## What is MCP?
MCP (Modular Command Platform) is a framework for building, running, and managing modular command-line tools and automations. It allows you to define and expose custom tools that can be accessed locally or remotely, making it easy to automate workflows and integrate with other systems.

## Overview
The MCP local server runs on your machine and provides a way to register, manage, and execute modular tools. It uses FastMCP as the backend and communicates via the 'stdio' transport, making it suitable for integration with editors, scripts, or other local clients.

## Installation
1. Clone this repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
Start the server with:
```bash
python main.py
```

The server will start and listen for commands via standard input/output.

## VS Code Integration
When you set up MCP in VS Code using the UI, the following configuration is added to your `settings.json` file (replace `<your-path>` with your actual project path):

```json
"mcp": {
    "servers": {
        "localserver": {
            "type": "stdio",
            "command": "<your-path>/bin/python",
            "args": [
                "<your-path>/main.py"
            ]
        }
    }
}
```

This allows VS Code to communicate with your local MCP server.

## License
This project is licensed under the GNU General Public License v3.0 (GPLv3). See the LICENSE file for details.
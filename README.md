# Persona Context Manager

Developed by Srikar Devulapalli

A powerful tool for managing and maintaining user personas and context information, designed to work seamlessly with Claude Desktop and other AI assistants.

## Overview

The Persona Context Manager is a sophisticated system that allows you to:
- Store and manage detailed user personas
- Maintain context about users across conversations
- Integrate with Claude Desktop for enhanced AI interactions
- Provide a beautiful, modern web interface for managing personas

## Features

### 1. Persona Management
- Create and maintain detailed user profiles
- Store categorized facts about users
- Add descriptions and metadata to persona information
- Import/export persona data in JSON format

### 2. Claude Desktop Integration
- Seamlessly connect with Claude Desktop
- Access persona information during conversations
- Get context-aware responses based on stored user information
- Natural language queries for persona information

### 3. Modern Web Interface
- Beautiful, responsive UI built with Streamlit
- Real-time updates and animations
- Easy-to-use persona management tools
- Visual representation of user information

### 4. MCP Server
- Fast and efficient API endpoints
- Natural language processing for queries
- Secure data storage
- Extensible architecture

## Getting Started

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Claude Desktop installed and configured

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/persona-context-mcp.git
cd persona-context-mcp
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Step 1: Setting Up User Personas

1. Start the server:
```bash
python server/server.py
```

2. In a new terminal window, launch the web interface:
```bash
cd ui
streamlit run app.py
```

3. Create and manage personas:
   - Enter a User ID to create a new persona
   - Add facts about the user using natural language
   - The system will automatically categorize and structure the information
   - You can edit, delete, or export persona data as needed

4. Example persona facts you can add:
   - "I love eating Biryani"
   - "I work as a software engineer"
   - "My favorite programming language is Python"
   - "I enjoy hiking on weekends"

### Step 2: Connecting with Claude Desktop

1. Install the MCP server in Claude Desktop:
```bash
mcp install mcp_server.py
```

2. Start the MCP server (optional):
```bash
python mcp_server.py
```

3. Open Claude Desktop - the integration will be automatic

4. You can now use natural language queries in Claude Desktop:
   - "What are the facts for [user]?"
   - "Show me [user]'s information"
   - "Tell me about [user]"

### Storage Configuration

1. Create a data directory for storing persona information:
```bash
mkdir -p data
```

2. Configure storage permissions:
```bash
chmod 755 data
```

3. The system will automatically create the following structure:
```
data/
├── {user_id}_persona.json    # Individual user persona files
└── persona_context.db        # SQLite database for additional context
```

4. Ensure the data directory is writable by the application:
```bash
chown -R $(whoami):$(whoami) data/
```

## API Endpoints

The MCP server provides the following endpoints:

- get_persona_tool: `GET /mcp/persona/{user_id}` - Retrieve persona information
- `POST /mcp/persona/{user_id}` - Update persona information (Coming soon)
- `DELETE /mcp/persona/{user_id}/{fact_index}` - Delete specific persona facts (Coming soon)

## Data Structure

Persona facts are stored in the following format:
```json
{
  "category": "string",
  "value": "string",
  "description": "string (optional)"
}
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please open an issue in the GitHub repository or contact the maintainers. 
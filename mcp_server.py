from mcp.server.fastmcp import FastMCP
import json
import os
from typing import List, Dict, Optional, Union



try:
    from mcp.server.fastmcp import FastMCP
    MCP_AVAILABLE = True
except ImportError:
    MCP_AVAILABLE = False
    from fastapi import FastAPI, HTTPException


# Create data directory if it doesn't exist
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
os.makedirs(DATA_DIR, exist_ok=True)


 #Create server instance based on available framework
if MCP_AVAILABLE:
    server = FastMCP(
        name="Persona Context MCP",
        host="0.0.0.0",
        port=5002
    )
else:
    server = FastAPI(title="Persona Context Server")

# Models
class PersonaFact:
    def __init__(self, category: str, value: str, description: Optional[str] = None):
        self.category = category
        self.value = value
        self.description = description

    def to_dict(self):
        return {
            "category": self.category,
            "value": self.value,
            "description": self.description
        }

async def get_persona(user_id: str) -> List[Dict]:
    """Get persona facts for a user
        Args:
            user_id: The ID of the user to get facts for
        Returns:
            List of persona facts
    """
    try:
        file_path = os.path.join(DATA_DIR, f"{user_id}_persona.json")
        print(f"[DEBUG] Attempting to read file: {file_path}")
        with open(file_path, "r") as f:
            data = json.load(f)
            print(f"[DEBUG] Successfully read data: {data}")
            
            # Return the data directly
            if isinstance(data, dict) and "data" in data:
                return data["data"]
            elif isinstance(data, list):
                return data
            else:
                print(f"[DEBUG] Unexpected data format: {type(data)}")
                return []
            
    except FileNotFoundError:
        print(f"[DEBUG] File not found: {file_path}")
        return []
    except json.JSONDecodeError as e:
        print(f"[DEBUG] JSON decode error: {str(e)}")
        return []
    except Exception as e:
        print(f"[DEBUG] Unexpected error: {str(e)}")
        return []
    

def extract_user_id(message: str) -> str:
    """Extract user ID from any natural language message.
    
    Args:
        message: The input message (e.g., "what are the facts for srikar", "show me srikar's info", "srikar")
    Returns:
        The extracted user ID
    """
    message = message.lower().strip()
    
    # Common patterns that might indicate a user ID
    patterns = [
        r"for\s+(\w+)",  # "for srikar"
        r"about\s+(\w+)",  # "about srikar"
        r"show\s+(\w+)",  # "show srikar"
        r"get\s+(\w+)",  # "get srikar"
        r"tell\s+me\s+about\s+(\w+)",  # "tell me about srikar"
        r"what\s+about\s+(\w+)",  # "what about srikar"
        r"who\s+is\s+(\w+)",  # "who is srikar"
        r"(\w+)'s",  # "srikar's"
    ]
    
    import re
    for pattern in patterns:
        match = re.search(pattern, message)
        if match:
            return match.group(1)
    
    # If no pattern matches, assume the whole message is the user ID
    # but only if it's a single word
    words = message.split()
    if len(words) == 1:
        return words[0]
    
    # If we can't extract a user ID, return the original message
    return message

# Register routes based on framework
if MCP_AVAILABLE:
    @server.tool()
    async def get_persona_tool(query: str) -> Dict:
        """Get persona facts for a user.
        
        Args:
            query: The query string (e.g., "what are the facts for srikar" or just "srikar")
        """
        user_id = extract_user_id(query)
        try:
            facts = await get_persona(user_id)
            
            if not facts:
                return {
                    "type": "text",
                    "text": f"No persona facts found for user: {user_id}",
                    "uuid": "56b2a590-10e8-4706-be22-b8bdb198884e"
                }
            
            # Format the facts into a readable string
            formatted_facts = []
            for fact in facts:
                formatted_fact = (
                    f"Category: {fact.get('category', '')}\n"
                    f"Value: {fact.get('value', '')}\n"
                    f"Description: {fact.get('description', '')}"
                )
                formatted_facts.append(formatted_fact)
            
            return {
                "type": "text",
                "text": f"Persona facts for {user_id}:\n\n" + "\n---\n".join(formatted_facts),
                "uuid": "56b2a590-10e8-4706-be22-b8bdb198884e"
            }
                
        except Exception as e:
            print(f"[DEBUG] Unexpected error: {str(e)}")
            return {
                "type": "text",
                "text": f"Error retrieving persona data for user: {user_id}",
                "uuid": "56b2a590-10e8-4706-be22-b8bdb198884e"
            }
else:
    @server.get("/mcp/persona/{user_id}")
    async def get_persona_endpoint(user_id: str) -> List[Dict]:
        return await get_persona(user_id)

if __name__ == "__main__":
    if not MCP_AVAILABLE:
        import uvicorn
        import asyncio
        # Create data directory if it doesn't exist
        os.makedirs(DATA_DIR, exist_ok=True)
        uvicorn.run(server, host="0.0.0.0", port=5002)
    else:
        # MCP framework will handle server startup
        print("Running server with stdio transport")
        server.run(transport="stdio")
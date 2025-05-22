from mcp.server.fastmcp import FastMCP
import json
import os
from typing import List, Dict
from datetime import datetime

# Create data directory if it doesn't exist
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
os.makedirs(DATA_DIR, exist_ok=True)

# Create an MCP server
server = FastMCP("Persona Context")

@server.tool()
def get_persona(user_id: str) -> List[Dict]:
    """Get persona facts for a user"""
    try:
        file_path = os.path.join(DATA_DIR, f"{user_id}_persona.json")
        with open(file_path, "r") as f:
            data = json.load(f)
            
            # Return the data directly
            if isinstance(data, dict) and "data" in data:
                return data["data"]
            elif isinstance(data, list):
                return data
            else:
                return []
            
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []
    except Exception:
        return []

@server.tool()
def update_persona(user_id: str, new_facts: List[Dict]) -> Dict:
    """Update persona facts for a user by appending new facts."""
    try:
        file_path = os.path.join(DATA_DIR, f"{user_id}_persona.json")
        
        # Read existing facts
        try:
            with open(file_path, "r") as f:
                existing_facts = json.load(f)
                if isinstance(existing_facts, dict) and "data" in existing_facts:
                    existing_facts = existing_facts["data"]
        except (FileNotFoundError, json.JSONDecodeError):
            existing_facts = []
        
        # Add timestamp to new facts
        for fact in new_facts:
            fact["timestamp"] = datetime.now().isoformat()
        
        # Append new facts
        if isinstance(new_facts, list):
            existing_facts.extend(new_facts)
        else:
            existing_facts.append(new_facts)
        
        # Write back all facts
        with open(file_path, "w") as f:
            json.dump(existing_facts, f, indent=2)
            
        return {"status": "success", "message": "Persona facts updated"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@server.tool()
def delete_persona_fact(user_id: str, fact_index: int) -> Dict:
    """Delete a specific fact from a user's persona."""
    try:
        file_path = os.path.join(DATA_DIR, f"{user_id}_persona.json")
        
        # Read existing facts
        try:
            with open(file_path, "r") as f:
                existing_facts = json.load(f)
                if isinstance(existing_facts, dict) and "data" in existing_facts:
                    existing_facts = existing_facts["data"]
        except (FileNotFoundError, json.JSONDecodeError):
            return {"status": "error", "message": "No facts found"}
        
        # Check if index is valid
        if fact_index < 0 or fact_index >= len(existing_facts):
            return {"status": "error", "message": "Invalid fact index"}
        
        # Remove the fact at the specified index
        existing_facts.pop(fact_index)
        
        # Write back remaining facts
        with open(file_path, "w") as f:
            json.dump(existing_facts, f, indent=2)
            
        return {"status": "success", "message": "Fact deleted successfully"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    print("Running server with stdio transport")
    server.run(transport="stdio") 
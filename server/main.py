from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import json
from datetime import datetime
import os
import sys

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Create data directory if it doesn't exist
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
os.makedirs(DATA_DIR, exist_ok=True)

app = FastAPI(title="Persona Context MCP")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_persona_file_path(user_id: str) -> str:
    """Get the path to the persona JSON file for a user."""
    return os.path.join(DATA_DIR, f"{user_id}_persona.json")

@app.get("/persona/{user_id}")
async def get_persona(user_id: str):
    """Get persona facts for a user."""
    try:
        file_path = get_persona_file_path(user_id)
        with open(file_path, "r") as f:
            data = json.load(f)
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
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/persona/{user_id}")
async def update_persona(user_id: str, facts: List[dict]):
    """Update persona facts for a user."""
    try:
        file_path = get_persona_file_path(user_id)
        
        # Read existing facts
        try:
            with open(file_path, "r") as f:
                existing_facts = json.load(f)
                if isinstance(existing_facts, dict) and "data" in existing_facts:
                    existing_facts = existing_facts["data"]
        except (FileNotFoundError, json.JSONDecodeError):
            existing_facts = []
        
        # Add timestamp to new facts
        for fact in facts:
            fact["timestamp"] = datetime.now().isoformat()
        
        # Append new facts
        if isinstance(facts, list):
            existing_facts.extend(facts)
        else:
            existing_facts.append(facts)
        
        # Write back all facts
        with open(file_path, "w") as f:
            json.dump(existing_facts, f, indent=2)
            
        return {"status": "success", "message": "Persona facts updated"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/persona/{user_id}/{fact_index}")
async def delete_persona_fact(user_id: str, fact_index: int):
    """Delete a specific fact from a user's persona."""
    try:
        file_path = get_persona_file_path(user_id)
        with open(file_path, "r") as f:
            facts = json.load(f)
            if isinstance(facts, dict) and "data" in facts:
                facts = facts["data"]
        
        if 0 <= fact_index < len(facts):
            facts.pop(fact_index)
            with open(file_path, "w") as f:
                json.dump(facts, f, indent=2)
            return {"status": "success", "message": "Fact deleted successfully"}
        else:
            raise HTTPException(status_code=400, detail="Invalid fact index")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    print("Starting server at http://localhost:5000")
    uvicorn.run(app, host="0.0.0.0", port=5000) 
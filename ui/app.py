import streamlit as st
import json
from datetime import datetime
import pandas as pd
from mcp.server.fastmcp import FastMCP
import os
import openai
import hashlib
import base64
from streamlit_option_menu import option_menu
from streamlit_lottie import st_lottie
from openai import OpenAI


# Page config must be the first Streamlit command
st.set_page_config(
    page_title="Persona Context Manager",
    page_icon="",
    layout="wide"
)

# Custom CSS for modern styling with animations
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background-color: #ffffff;
    }
    
    .main-content {
        background: transparent;
        padding: 1rem;
        margin: 0;
        animation: contentFadeIn 0.8s ease-out;
    }
    
    .main-header {
        color: #1e40af;
        font-size: 4rem;
        font-weight: 600;
        margin: 1rem 0 1rem 0;
        position: relative;
        text-align: center;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
        animation: headerSlideIn 1s ease-out;
        background: transparent;
    }
    
    .developer-info {
        color: #64748b;
        font-size: 1.2rem;
        text-align: center;
        margin: 0.5rem 0 2rem 0;
        font-style: italic;
    }
    
    .description-text {
        color: #64748b;
        font-size: 1.1rem;
        text-align: center;
        max-width: 800px;
        margin: 0.5rem auto 1.5rem auto;
        line-height: 1.6;
        animation: descriptionFadeIn 1s ease-out 0.3s backwards;
        position: relative;
        padding: 0 1rem;
    }
    
    .description-text::after {
        content: '';
        position: absolute;
        bottom: -0.75rem;
        left: 50%;
        transform: translateX(-50%);
        width: 60px;
        height: 3px;
        background: linear-gradient(90deg, transparent, #3b82f6, transparent);
        animation: lineGrow 1.2s ease-out 0.8s backwards;
    }
    
    .coming-soon-container {
        display: flex;
        justify-content: center;
        gap: 1.5rem;
        margin: 1rem auto;
        max-width: 600px;
        animation: containerSlideIn 0.8s ease-out 0.5s backwards;
    }
    
    .coming-soon-item {
        background: #ffffff;
        padding: 1rem;
        border-radius: 1rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        border: 1px solid rgba(59, 130, 246, 0.1);
        text-align: center;
        flex: 1;
        max-width: 200px;
        transition: all 0.3s ease;
    }
    
    .coming-soon-item:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 12px rgba(0, 0, 0, 0.1);
    }
    
    .coming-soon-icon {
        font-size: 1.5rem;
        margin-bottom: 0.5rem;
        color: #3b82f6;
    }
    
    .coming-soon-label {
        color: #64748b;
        font-size: 0.8rem;
        margin-top: 0.25rem;
    }
    
    .coming-soon-badge {
        background: #e0f2fe;
        color: #0369a1;
        padding: 0.2rem 0.6rem;
        border-radius: 1rem;
        font-size: 0.7rem;
        font-weight: 500;
        margin-top: 0.25rem;
        display: inline-block;
    }
    
    .user-id-container {
        margin-top: 1rem;
        animation: containerSlideIn 0.8s ease-out 0.7s backwards;
    }
    
    .sub-header {
        color: #1e40af;
        font-size: 1.75rem;
        font-weight: 600;
        margin: 2rem 0 1.5rem 0;
        animation: textFadeIn 0.8s ease-out;
    }
    
    @keyframes descriptionFadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes lineGrow {
        from { width: 0; opacity: 0; }
        to { width: 60px; opacity: 1; }
    }
    
    @keyframes containerSlideIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes headerSlideIn {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .content-container {
        background: transparent;
        padding: 2.5rem;
        margin: 1.5rem;
        animation: containerPop 0.6s cubic-bezier(0.34, 1.56, 0.64, 1);
    }
    
    @keyframes containerPop {
        0% { transform: scale(0.95); opacity: 0; }
        100% { transform: scale(1); opacity: 1; }
    }
    
    .avatar-container {
        display: flex;
        align-items: center;
        gap: 2rem;
        margin-bottom: 2.5rem;
        padding: 2rem;
        background: #ffffff;
        border-radius: 2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
        border: 1px solid rgba(0, 0, 0, 0.1);
        animation: containerSlideIn 0.8s cubic-bezier(0.34, 1.56, 0.64, 1);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    @keyframes containerSlideIn {
        0% { transform: translateX(-20px); opacity: 0; }
        100% { transform: translateX(0); opacity: 1; }
    }
    
    .avatar-container:hover {
        transform: translateY(-4px) scale(1.01);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.12);
    }
    
    .avatar-image {
        width: 120px;
        height: 120px;
        border-radius: 50%;
        object-fit: cover;
        border: 4px solid #3b82f6;
        animation: avatarPulse 3s infinite;
        box-shadow: 0 8px 16px rgba(59, 130, 246, 0.2);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .avatar-container:hover .avatar-image {
        transform: scale(1.05) rotate(5deg);
        border-color: #60a5fa;
    }
    
    @keyframes avatarPulse {
        0% { box-shadow: 0 0 0 0 rgba(59, 130, 246, 0.4); }
        70% { box-shadow: 0 0 0 15px rgba(59, 130, 246, 0); }
        100% { box-shadow: 0 0 0 0 rgba(59, 130, 246, 0); }
    }
    
    .user-info {
        flex: 1;
    }
    
    .user-name {
        font-size: 2rem;
        font-weight: 600;
        color: #1e40af;
        margin: 0;
        animation: textFadeIn 0.8s ease-out;
    }
    
    .user-stats {
        color: #64748b;
        margin: 0.75rem 0 0 0;
        font-size: 1.1rem;
        animation: textFadeIn 0.8s ease-out 0.2s backwards;
    }
    
    @keyframes textFadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .fact-container {
        background: #ffffff;
        border-radius: 1.5rem;
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
        border: 1px solid rgba(0, 0, 0, 0.1);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        animation: containerPop 0.6s cubic-bezier(0.34, 1.56, 0.64, 1);
    }
    
    .fact-container:hover {
        transform: translateY(-4px) scale(1.01);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.12);
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #3b82f6, #2563eb);
        color: white;
        border: none;
        padding: 0.875rem 1.75rem;
        border-radius: 1rem;
        font-weight: 500;
        font-size: 1rem;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 6px rgba(37, 99, 235, 0.2);
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, #2563eb, #1d4ed8);
        transform: translateY(-2px) scale(1.05);
        box-shadow: 0 6px 12px rgba(37, 99, 235, 0.3);
    }
    
    .stTextInput>div>div>input {
        background: #ffffff;
        border-radius: 1rem;
        border: 2px solid rgba(59, 130, 246, 0.2);
        padding: 0.75rem 1rem;
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput>div>div>input:focus {
        border-color: #3b82f6;
        box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.1);
        transform: scale(1.01);
    }
    
    .stTextArea>div>div>textarea {
        background: #ffffff;
        border-radius: 1rem;
        border: 2px solid rgba(59, 130, 246, 0.2);
        padding: 0.75rem 1rem;
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    
    .stTextArea>div>div>textarea:focus {
        border-color: #3b82f6;
        box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.1);
        transform: scale(1.01);
    }
    
    .stExpander {
        background: #ffffff;
        border-radius: 1rem;
        border: 2px solid rgba(59, 130, 246, 0.2);
        transition: all 0.3s ease;
        animation: containerPop 0.6s cubic-bezier(0.34, 1.56, 0.64, 1);
    }
    
    .stExpander:hover {
        border-color: #3b82f6;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.1);
        transform: scale(1.01);
    }
    
    .import-export-container {
        background: #ffffff;
        border-radius: 2rem;
        padding: 2rem;
        margin-top: 2.5rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
        border: 1px solid rgba(0, 0, 0, 0.1);
        animation: containerSlideIn 0.8s cubic-bezier(0.34, 1.56, 0.64, 1);
    }
    </style>
""", unsafe_allow_html=True)

# Create data directory if it doesn't exist
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
os.makedirs(DATA_DIR, exist_ok=True)

# Initialize MCP server
server = FastMCP("Persona Context Manager")

# Initialize OpenAI client
client = None

def init_openai_client():
    """Initialize the OpenAI client."""
    global client
    # api_key = os.getenv("OPENAI_API_KEY")
    openai.api_key = st.secrets["api_keys"]["openai"]
    if not openai.api_key:
        st.warning("OPENAI_API_KEY not set. Please set it in your environment variables.")
        return
    
    try:
        # openai.api_key = openai.OpenAI(api_key=openai.api_key)
        # Test the API key with a simple call
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": "test"}],
            max_tokens=5
        )
        st.success("Successfully connected to OpenAI API with GPT-4")
    except Exception as e:
        st.error(f"Failed to initialize OpenAI client: {str(e)}")
        client = None

@server.tool()
def get_persona_tool(user_id: str):
    """Get persona facts for a user"""
    try:
        file_path = os.path.join(DATA_DIR, f"{user_id}_persona.json")
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
    except Exception:
        return []

@server.tool()
def update_persona_tool(user_id: str, facts: list):
    """Update persona facts for a user"""
    try:
        file_path = os.path.join(DATA_DIR, f"{user_id}_persona.json")
        existing_facts = []
        try:
            with open(file_path, "r") as f:
                data = json.load(f)
                if isinstance(data, dict) and "data" in data:
                    existing_facts = data["data"]
                elif isinstance(data, list):
                    existing_facts = data
        except (FileNotFoundError, json.JSONDecodeError):
            pass

        # Add timestamp to new facts
        for fact in facts:
            fact["timestamp"] = datetime.now().isoformat()
        
        # Check for duplicates before adding
        new_facts = []
        for new_fact in facts:
            is_duplicate = False
            for existing_fact in existing_facts:
                if (new_fact.get("category") == existing_fact.get("category") and 
                    new_fact.get("value") == existing_fact.get("value")):
                    is_duplicate = True
                    break
            if not is_duplicate:
                new_facts.append(new_fact)
        
        # Combine existing and new facts
        all_facts = existing_facts + new_facts
        
        # Save to file
        with open(file_path, "w") as f:
            json.dump(all_facts, f, indent=2)
        
        return {"status": "success", "message": "Facts updated successfully"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@server.tool()
def delete_persona_fact_tool(user_id: str, fact_index: int):
    """Delete a specific fact from a user's persona"""
    try:
        file_path = os.path.join(DATA_DIR, f"{user_id}_persona.json")
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
            return {"status": "error", "message": "Invalid fact index"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def load_persona_facts(user_id):
    """Load persona facts from the server."""
    try:
        facts = get_persona_tool(user_id)
        return facts
    except Exception as e:
        st.error(f"Failed to load facts: {str(e)}")
        return []

def update_persona_fact(user_id, facts):
    """Update persona facts on the server."""
    try:
        result = update_persona_tool(user_id, facts)
        return result.get("status") == "success"
    except Exception as e:
        st.error(f"Failed to update facts: {str(e)}")
        return False

def delete_persona_fact(user_id: str, fact_index: int) -> bool:
    """Delete a specific fact from the server."""
    try:
        result = delete_persona_fact_tool(user_id, fact_index)
        return result.get("status") == "success"
    except Exception as e:
        st.error(f"Failed to delete fact: {str(e)}")
        return False

def categorize_fact(fact_text: str) -> dict:
    """Use GPT-4 to categorize a fact."""
    openai.api_key = st.secrets["api_keys"]["openai"]
    client = OpenAI(api_key=st.secrets["api_keys"]["openai"])

    # api_key = os.getenv("OPENAI_API_KEY")
    if not client:
        init_openai_client()
        if not client:
            return None
    
    try:
        st.success("Checkpoint to categorize fact")
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": """You are a helpful assistant that categorizes user statements into persona facts.
                For each statement, provide:
                1. A two-word category (e.g., "food preference", "hobby interest", "work experience")
                2. The value (the actual statement)
                3. A brief description
                
                Your response must be a valid JSON object with these exact fields:
                {
                    "category": "two word category",
                    "value": "the statement",
                    "description": "brief description"
                }
                
                Do not include any other text or explanation, just the JSON object."""},
                {"role": "user", "content": fact_text}
            ]
        )
        
        # Parse the response
        content = response.choices[0].message.content.strip()
        # Find the JSON object in the response
        start_idx = content.find('{')
        end_idx = content.rfind('}') + 1
        if start_idx >= 0 and end_idx > start_idx:
            json_str = content[start_idx:end_idx]
            result = json.loads(json_str)
            return result
        else:
            st.error("Failed to parse LLM response as JSON")
            return None
    except Exception as e:
        st.error(f"Failed to categorize fact: {str(e)}")
        return None

def get_avatar_url(user_id: str) -> str:
    """Generate a consistent avatar URL for a user ID using DiceBear."""
    seed = hashlib.md5(user_id.encode()).hexdigest()
    return f"https://api.dicebear.com/7.x/bottts/svg?seed={seed}&backgroundColor=2563eb"

def export_persona(user_id: str) -> str:
    """Export persona facts as a JSON file."""
    facts = load_persona_facts(user_id)
    data = {
        "user_id": user_id,
        "facts": facts,
        "exported_at": datetime.now().isoformat()
    }
    return json.dumps(data, indent=2)

def import_persona(json_data: str) -> bool:
    """Import persona facts from a JSON file."""
    try:
        data = json.loads(json_data)
        if "user_id" not in data or "facts" not in data:
            st.error("Invalid persona data format")
            return False
        
        if update_persona_fact(data["user_id"], data["facts"]):
            st.success(f"Successfully imported {len(data['facts'])} facts for user {data['user_id']}")
            return True
        return False
    except json.JSONDecodeError:
        st.error("Invalid JSON format")
        return False
    except Exception as e:
        st.error(f"Failed to import persona: {str(e)}")
        return False

# Initialize session state
if "user_id" not in st.session_state:
    st.session_state.user_id = ""
if "persona_facts" not in st.session_state:
    st.session_state.persona_facts = []
if "editing_fact" not in st.session_state:
    st.session_state.editing_fact = None
if "editing_fact_index" not in st.session_state:
    st.session_state.editing_fact_index = None

# Main content
st.markdown('<div class="main-content">', unsafe_allow_html=True)
st.markdown('<h1 class="main-header">Persona Context Manager</h1>', unsafe_allow_html=True)
st.markdown('<p class="developer-info">Developed by Srikar Devulapalli</p>', unsafe_allow_html=True)
st.markdown("""
    <div class="description-text">
        This is a user-friendly tool that turns raw sentences into structured Category / Description / Value records—validated by an LLM, stored in a database, and served through the get_persona_tool so any MCP-aware assistant can deliver perfectly tailored answers.
    </div>
    
    <div class="coming-soon-container">
        <div class="coming-soon-item">
            <div class="coming-soon-icon">🖼️</div>
            <div>Image Upload</div>
            <div class="coming-soon-label">Add visual context to your personas</div>
            <div class="coming-soon-badge">Coming Soon</div>
        </div>
        <div class="coming-soon-item">
            <div class="coming-soon-icon">🎤</div>
            <div>Speech-to-Text</div>
            <div class="coming-soon-label">Convert voice notes to text</div>
            <div class="coming-soon-badge">Coming Soon</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# User ID input
st.markdown('<div class="user-id-container">', unsafe_allow_html=True)
st.markdown('<div class="sub-header">User ID</div>', unsafe_allow_html=True)
user_id = st.text_input("User ID", value=st.session_state.user_id, label_visibility="collapsed")

if user_id and user_id != st.session_state.user_id:
    st.session_state.user_id = user_id
    st.session_state.persona_facts = load_persona_facts(user_id)
    st.success(f"Loaded persona facts for user: {user_id}")

if st.session_state.user_id:
    # Display user avatar and info
    st.markdown(f"""
        <div class="avatar-container">
            <img src="{get_avatar_url(st.session_state.user_id)}" class="avatar-image" alt="User Avatar">
            <div class="user-info">
                <h2 class="user-name">{st.session_state.user_id}</h2>
                <p class="user-stats">
                    {len(st.session_state.persona_facts)} facts • 
                    Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                </p>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # LLM-Assisted Fact Entry
    st.markdown('<h2 class="sub-header">Add New Fact</h2>', unsafe_allow_html=True)
    with st.form("llm_fact_entry"):
        fact_text = st.text_area("Enter your fact", placeholder="e.g., I love eating Biryani", height=100)
        submitted = st.form_submit_button("Add Fact")
        
        if submitted and fact_text:
            with st.spinner("Categorizing fact..."):
                result = categorize_fact(fact_text)
                if result:
                    if update_persona_fact(st.session_state.user_id, [result]):
                        st.success("Fact added successfully!")
                        st.session_state.persona_facts = load_persona_facts(st.session_state.user_id)
                        st.rerun()
                    else:
                        st.error("Failed to add fact")
                else:
                    st.error("Failed to categorize fact")

    # Display existing facts
    if st.session_state.persona_facts:
        st.markdown('<h2 class="sub-header">Existing Facts</h2>', unsafe_allow_html=True)
        for i, fact in enumerate(st.session_state.persona_facts):
            category = fact.get('category', 'Uncategorized')
            value = fact.get('value', '')[:50]
            with st.expander(f"📋 {category} - {value}..."):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"**Category:** {category}")
                    st.write(f"**Value:** {fact.get('value', '')}")
                    st.write(f"**Description:** {fact.get('description', '')}")
                    if 'timestamp' in fact:
                        st.write(f"**Added:** {datetime.fromisoformat(fact['timestamp']).strftime('%Y-%m-%d %H:%M:%S')}")
                with col2:
                    col_edit, col_delete = st.columns(2)
                    with col_edit:
                        if st.button("Edit", key=f"edit_{i}"):
                            st.session_state.editing_fact = fact.copy()
                            st.session_state.editing_fact_index = i
                            st.rerun()
                    with col_delete:
                        if st.button("Delete", key=f"delete_{i}"):
                            if delete_persona_fact(st.session_state.user_id, i):
                                st.success("Fact deleted successfully!")
                                st.session_state.persona_facts = load_persona_facts(st.session_state.user_id)
                                st.rerun()
                            else:
                                st.error("Failed to delete fact")

    # Edit form
    if st.session_state.editing_fact is not None:
        st.markdown('<h2 class="sub-header">Edit Fact</h2>', unsafe_allow_html=True)
        with st.form("edit_fact"):
            category = st.text_input("Category", value=st.session_state.editing_fact.get('category', ''))
            value = st.text_area("Value", value=st.session_state.editing_fact.get('value', ''), height=100)
            description = st.text_area("Description", value=st.session_state.editing_fact.get('description', ''), height=100)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.form_submit_button("Save Changes"):
                    updated_fact = {
                        "category": category,
                        "value": value,
                        "description": description,
                        "timestamp": st.session_state.editing_fact.get('timestamp', datetime.now().isoformat())
                    }
                    
                    # Create a new list with the updated fact
                    updated_facts = st.session_state.persona_facts.copy()
                    updated_facts[st.session_state.editing_fact_index] = updated_fact
                    
                    if update_persona_fact(st.session_state.user_id, updated_facts):
                        st.success("Fact updated successfully!")
                        st.session_state.persona_facts = load_persona_facts(st.session_state.user_id)
                        st.session_state.editing_fact = None
                        st.session_state.editing_fact_index = None
                        st.rerun()
                    else:
                        st.error("Failed to update fact")
            
            with col2:
                if st.form_submit_button("Cancel"):
                    st.session_state.editing_fact = None
                    st.session_state.editing_fact_index = None
                    st.rerun()

    # Import/Export Section
    st.markdown('<h2 class="sub-header">Import/Export Persona</h2>', unsafe_allow_html=True)
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### Export Persona")
            if st.button("Export Persona Data"):
                json_data = export_persona(st.session_state.user_id)
                b64 = base64.b64encode(json_data.encode()).decode()
                href = f'data:file/json;base64,{b64}'
                st.markdown(
                    f'<a href="{href}" download="{st.session_state.user_id}_persona.json" class="stButton">Download Persona Data</a>',
                    unsafe_allow_html=True
                )
        
        with col2:
            st.markdown("### Import Persona")
            uploaded_file = st.file_uploader("Upload Persona JSON", type=['json'])
            if uploaded_file is not None:
                json_data = uploaded_file.getvalue().decode()
                if import_persona(json_data):
                    st.session_state.persona_facts = load_persona_facts(st.session_state.user_id)
                    st.rerun()
else:
    st.info("Please enter a User ID to get started.")

st.markdown('</div>', unsafe_allow_html=True)  # Close user-id-container
st.markdown('</div>', unsafe_allow_html=True)  # Close main-content
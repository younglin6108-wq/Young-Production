"""
Database Schema Inspector
-------------------------
Always run this first to check current properties before any API calls.
Usage: python inspect_db.py
"""
import os
import sys
import json
import requests
from dotenv import load_dotenv

sys.stdout.reconfigure(encoding='utf-8')
load_dotenv()

NOTION_KEY = os.getenv("NOTION_API_KEY")
TRACKER_DB_ID = os.getenv("PROD_TRACKER_DB_ID")
VIRAL_DNA_DB_ID = os.getenv("VIRAL_DNA_DB_ID")
YOUNG_EMPIRE_DB_ID = os.getenv("YOUNG_EMPIRE_DB_ID")
SCENE_LIST_DB_ID = os.getenv("SCENE_LIST_DB_ID")

HEADERS = {
    "Authorization": f"Bearer {NOTION_KEY}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

def get_db_schema(db_id, db_name):
    """Fetch and display the current schema of a Notion database."""
    print(f"\n{'='*60}")
    print(f"Database: {db_name}")
    print(f"{'='*60}")
    
    if not db_id:
        print(f"⚠️ No DB ID configured for {db_name}")
        return None
    
    url = f"https://api.notion.com/v1/databases/{db_id}"
    
    try:
        response = requests.get(url, headers=HEADERS)
        
        if response.status_code != 200:
            print(f"❌ Error: {response.status_code} - {response.text}")
            return None
            
        db_info = response.json()
        
        # Get title
        title = db_info['title'][0]['text']['content'] if db_info.get('title') else "Untitled"
        print(f"Title: {title}")
        print(f"ID: {db_id}")
        print(f"\nProperties:")
        print("-" * 40)
        
        properties = db_info.get('properties', {})
        schema = {}
        
        for prop_name, prop_data in properties.items():
            prop_type = prop_data.get('type', 'unknown')
            extra_info = ""
            options = None
            
            # Get extra info for select/multi-select
            if prop_type == 'select' and prop_data.get('select', {}).get('options'):
                options = [opt['name'] for opt in prop_data['select']['options']]
                extra_info = f" -> Options: {options}"
            elif prop_type == 'multi_select' and prop_data.get('multi_select', {}).get('options'):
                options = [opt['name'] for opt in prop_data['multi_select']['options']]
                extra_info = f" -> Options: {options}"
            elif prop_type == 'status' and prop_data.get('status', {}).get('options'):
                options = [opt['name'] for opt in prop_data['status']['options']]
                extra_info = f" -> Options: {options}"
            elif prop_type == 'relation':
                related_db = prop_data.get('relation', {}).get('database_id', 'Unknown')
                extra_info = f" -> Linked to: {related_db[:8]}..."
                
            print(f"  • {prop_name}: {prop_type}{extra_info}")
            schema[prop_name] = {"type": prop_type, "options": options}
        
        return schema
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        return None

def get_all_schemas():
    """Fetch schemas for all configured databases."""
    schemas = {}
    
    schemas['tracker'] = get_db_schema(TRACKER_DB_ID, "Young Production Tracker")
    schemas['viral_dna'] = get_db_schema(VIRAL_DNA_DB_ID, "Viral DNA")
    schemas['empire'] = get_db_schema(YOUNG_EMPIRE_DB_ID, "Young Empire")
    schemas['scene_list'] = get_db_schema(SCENE_LIST_DB_ID, "Scene List")
    
    return schemas

if __name__ == "__main__":
    if not NOTION_KEY:
        print("❌ Error: NOTION_API_KEY not found in .env")
    else:
        print("🔍 Fetching current database schemas from Notion...")
        get_all_schemas()
        print(f"\n{'='*60}")
        print("✅ Schema inspection complete.")

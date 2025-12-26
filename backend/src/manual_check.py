import os
import sys
import requests
import json
from dotenv import load_dotenv

# Force UTF-8
sys.stdout.reconfigure(encoding='utf-8')
load_dotenv()

NOTION_KEY = os.getenv("NOTION_API_KEY")
TRACKER_DB_ID = os.getenv("PROD_TRACKER_DB_ID")
VIRAL_DNA_DB_ID = os.getenv("VIRAL_DNA_DB_ID")
SCENE_LIST_DB_ID = os.getenv("SCENE_LIST_DB_ID")

HEADERS = {
    "Authorization": f"Bearer {NOTION_KEY}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

def print_response_error(response):
    try:
        print(f"❌ Error {response.status_code}: {json.dumps(response.json(), indent=2)}")
    except:
        print(f"❌ Error {response.status_code}: {response.text}")

def clear_database(db_id, db_name):
    print(f"\n--- Clearing Database: {db_name} ---")
    
    if not db_id:
        print(f"⚠️ Skipping {db_name} (No ID found)")
        return

    has_more = True
    start_cursor = None
    count = 0
    
    query_url = f"https://api.notion.com/v1/databases/{db_id}/query"
    
    try:
        while has_more:
            payload = {"page_size": 100}
            if start_cursor:
                payload["start_cursor"] = start_cursor
                
            response = requests.post(query_url, headers=HEADERS, json=payload)
            
            if response.status_code != 200:
                print(f"❌ Error querying DB: {response.text}")
                return

            data = response.json()
            pages = data.get("results", [])
            
            for page in pages:
                page_id = page['id']
                # Archive page
                update_url = f"https://api.notion.com/v1/pages/{page_id}"
                update_payload = {"archived": True}
                update_res = requests.patch(update_url, headers=HEADERS, json=update_payload)
                
                if update_res.status_code == 200:
                    print(f"Archived page: {page_id}", end="\r")
                    count += 1
                else:
                    print(f"\nFailed to archive {page_id}: {update_res.text}")
            
            has_more = data.get("has_more")
            start_cursor = data.get("next_cursor")
            
        print(f"\n✅ Successfully archived {count} pages from {db_name}.")

    except Exception as e:
        print(f"\n❌ Exception: {e}")

def create_viral_dna_page(title):
    payload = {
        "parent": {"database_id": VIRAL_DNA_DB_ID},
        "properties": {
            "Title": {
                "title": [{"text": {"content": title}}]
            }
        }
    }
    response = requests.post("https://api.notion.com/v1/pages", headers=HEADERS, json=payload)
    if response.status_code == 200:
        page_id = response.json().get('id')
        print(f"✅ Created Viral DNA: {title} ({page_id})")
        return page_id
    else:
        print(f"❌ Failed to create Viral DNA: {title}")
        print_response_error(response)
        return None

def create_production_page(title, viral_dna_ids):
    # Format 'shorts' as per schema inspection (lowercase 'shorts')
    # Status 'Idea'
    
    relations = [{"id": vid} for vid in viral_dna_ids]
    
    payload = {
        "parent": {"database_id": TRACKER_DB_ID},
        "properties": {
            "Title": {
                "title": [{"text": {"content": title}}]
            },
            "Status": {
                "status": {"name": "Idea"}
            },
            "Format": {
                "select": {"name": "shorts"}
            },
            "Viral DNA sources": {
                "relation": relations
            }
        }
    }
    
    response = requests.post("https://api.notion.com/v1/pages", headers=HEADERS, json=payload)
    if response.status_code == 200:
        page_id = response.json().get('id')
        print(f"✅ Created Production: {title} ({page_id})")
        return page_id
    else:
        print(f"❌ Failed to create Production: {title}")
        print_response_error(response)
        return None

def create_scene(name, duration, production_id):
    payload = {
        "parent": {"database_id": SCENE_LIST_DB_ID},
        "properties": {
            "Name": {
                "title": [{"text": {"content": name}}]
            },
            "Duration (sec)": {
                "number": duration
            },
            "Production": {
                "relation": [{"id": production_id}]
            }
        }
    }
    
    response = requests.post("https://api.notion.com/v1/pages", headers=HEADERS, json=payload)
    if response.status_code == 200:
        print(f"✅ Created Scene: {name} ({duration}s)")
    else:
        print(f"❌ Failed to create Scene: {name}")
        print_response_error(response)

def main():
    if not NOTION_KEY:
        print("Please check your .env file for valid keys.")
        return

    # 1. Clear previous test cases
    print("🧹 [Safety Check] Skipping automatic cleanup. Run clear_dbs.py manually if needed.")
    # clear_database(TRACKER_DB_ID, "Young Production Tracker")
    # clear_database(VIRAL_DNA_DB_ID, "Viral DNA")
    # clear_database(SCENE_LIST_DB_ID, "Global Scene List")
    
    # 2. Create 3 Viral DNA pages
    print("\n🧬 Creating Viral DNA entries...")
    dna_ids = []
    for i in range(1, 4):
        pid = create_viral_dna_page(f"Viral Source #{i}")
        if pid:
            dna_ids.append(pid)
            
    if len(dna_ids) < 3:
        print("❌ Failed to create all Viral DNA entries. Aborting.")
        return

    # 3. Create Production Page linked to Viral DNA
    print("\n🎬 Creating Production entry...")
    prod_id = create_production_page("Test Production [Shorts]", dna_ids)
    
    if not prod_id:
        print("❌ Failed to create Production entry. Aborting.")
        return

    # 4. Create 30s Scene List (3 scenes x 10s)
    print("\n🎞️ Creating Scene List...")
    for i in range(1, 4):
        create_scene(f"Scene {i}", 10, prod_id)

    print("\n✅ Test Case Setup Complete!")

if __name__ == "__main__":
    main()

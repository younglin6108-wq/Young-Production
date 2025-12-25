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

HEADERS = {
    "Authorization": f"Bearer {NOTION_KEY}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

def clear_database(db_id, db_name):
    print(f"\n--- Clearing Database: {db_name} ---")
    
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

if __name__ == "__main__":
    if not NOTION_KEY:
        print("Error: NOTION_API_KEY not found")
    else:
        clear_database(TRACKER_DB_ID, "Young Production Tracker")
        clear_database(VIRAL_DNA_DB_ID, "Viral DNA")

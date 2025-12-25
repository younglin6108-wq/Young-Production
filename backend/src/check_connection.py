import os
import sys
from dotenv import load_dotenv
from notion_client import Client

# Force UTF-8
sys.stdout.reconfigure(encoding='utf-8')
load_dotenv()

NOTION_KEY = os.getenv("NOTION_API_KEY")
TRACKER_DB_ID = os.getenv("PROD_TRACKER_DB_ID")
VIRAL_DNA_DB_ID = os.getenv("VIRAL_DNA_DB_ID")

def connect_notion():
    if not NOTION_KEY:
        print("Error: NOTION_API_KEY not found")
        return None
    return Client(auth=NOTION_KEY)

def create_test_page(client, db_id):
    print(f"\n--- Attempting to create page in DB {db_id} ---")
    try:
        response = client.pages.create(
            parent={"database_id": db_id},
            properties={
                "Title": {
                    "title": [
                        {"text": {"content": "We did it"}}
                    ]
                },
                "Full Transcript": {
                    "rich_text": [
                        {"text": {"content": "This is a test from Young Production."}}
                    ]
                }
            }
        )
        print(f"✅ Success! Created Page ID: {response['id']}")
        print(f"URL: {response['url']}")
        return True
    except Exception as e:
        print(f"❌ Failed to create page: {e}")
        return False

def test_connection():
    notion = connect_notion()
    if not notion:
        return

    # 1. Test Tracker DB (Read Only via raw request if query missing)
    print("--- Testing Access to Young Production Tracker ---")
    try:
        # Fallback to manual request if .query is missing
        if hasattr(notion.databases, 'query'):
            db_info = notion.databases.retrieve(database_id=TRACKER_DB_ID)
            db_title = db_info['title'][0]['text']['content'] if db_info['title'] else "Untitled"
            print(f"✅ Connected to DB: '{db_title}'")
            results = notion.databases.query(database_id=TRACKER_DB_ID)
        else:
            print("⚠️ 'query' method missing. Using raw request...")
            results = notion.request(url=f"https://api.notion.com/v1/databases/{TRACKER_DB_ID}/query", method="POST")
        
        count = len(results.get('results', []))
        print(f"✅ Success! Read access confirmed. Found {count} pages.")
    except Exception as e:
        print(f"❌ Failed to read Tracker DB: {e}")

    # 2. Test Viral DNA (Write Test)
    create_test_page(notion, VIRAL_DNA_DB_ID)

if __name__ == "__main__":
    test_connection()

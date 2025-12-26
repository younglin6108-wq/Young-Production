import os
import sys
import requests
import json
from dotenv import load_dotenv

# Force UTF-8
sys.stdout.reconfigure(encoding='utf-8')
load_dotenv()

NOTION_KEY = os.getenv("NOTION_API_KEY")

HEADERS = {
    "Authorization": f"Bearer {NOTION_KEY}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

def unarchive_page(page_id):
    url = f"https://api.notion.com/v1/pages/{page_id}"
    payload = {"archived": False}
    try:
        response = requests.patch(url, headers=HEADERS, json=payload)
        if response.status_code == 200:
            print(f"✅ Successfully recovered page: {page_id}")
        else:
            print(f"❌ Failed to recover {page_id}: {response.text}")
    except Exception as e:
        print(f"❌ Exception recovering {page_id}: {e}")

def main():
    # IDs captured from the previous log
    # Note: These are likely the last pages processed in the loop due to '\r' overwriting
    ids_to_recover = [
        "2d4cd90f-688c-804e-a42f-d33beac7db62", # Tracker
        "2d4cd90f-688c-81ae-a5e8-fed147377fba", # Viral DNA
        "2d4cd90f-688c-8043-991b-c84f009334d9"  # Scene List
    ]
    
    print("--- Attempting to recover known archived pages ---")
    for pid in ids_to_recover:
        unarchive_page(pid)
        
    print("\n⚠️  NOTE: Due to log overwriting, I could only automatically identify these 3 pages.")
    print("Please check your Notion 'Trash' to restore the remaining pages.")

if __name__ == "__main__":
    main()

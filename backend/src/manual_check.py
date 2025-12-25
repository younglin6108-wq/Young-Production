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

def print_response_error(response):
    try:
        print(f"❌ Error {response.status_code}: {json.dumps(response.json(), indent=2)}")
    except:
        print(f"❌ Error {response.status_code}: {response.text}")

def test_case_1():
    print("\n--- Test Case 1: Creating Script in 'Young Production Tracker' ---")
    
    # Define the payload
    payload = {
        "parent": {"database_id": TRACKER_DB_ID},
        "properties": {
            "Title": {
                "title": [{"text": {"content": "Young Production Test: 1 Min Script"}}]
            },
            "Status": {
                "status": {"name": "Idea"} 
            },
            "Format": {
                "select": {"name": "Shorts"}
            }
        },
        "children": [
            {
                "object": "block",
                "type": "heading_1",
                "heading_1": {
                    "rich_text": [{"text": {"content": "Video Script (1 Minute)"}}]
                }
            },
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"text": {"content": "HOOK (0-5s): Stop wasting money on ads. Here is the free method.\n\nBODY (5-45s): First, go to Reddit. Find a problem. Solve it. Post it.\n\nCTA (45-60s): Subscribe for more."}}]
                }
            }
        ]
    }

    response = requests.post("https://api.notion.com/v1/pages", headers=HEADERS, json=payload)
    
    if response.status_code == 200:
        print(f"✅ Success! Created Page: {response.json().get('url')}")
    else:
        print("Failed to create page in Tracker.")
        print_response_error(response)
        # Fallback: Maybe 'Status' is a Select property, not Status type?
        if "validation_error" in response.text:
             print("⚠️  Retrying with 'Status' as Select property instead of Status type...")
             payload['properties']['Status'] = {"select": {"name": "Scripting"}}
             response = requests.post("https://api.notion.com/v1/pages", headers=HEADERS, json=payload)
             if response.status_code == 200:
                 print(f"✅ Retry Success! Created Page: {response.json().get('url')}")
             else:
                 print_response_error(response)

def test_case_2():
    print("\n--- Test Case 2: Workflow Doc in 'Viral DNA' ---")
    
    explanation_text = (
        "FLOW OF INTERACTION:\n"
        "1. Idea added to 'Young Production Tracker' -> Status: Researching\n"
        "2. Python script detects 'Ready to Render' status.\n"
        "3. Python pulls style patterns from 'Viral DNA' (this DB).\n"
        "4. Python generates script & audio.\n"
        "5. Final video URL is updated back to Tracker."
    )

    payload = {
        "parent": {"database_id": VIRAL_DNA_DB_ID},
        "properties": {
            "Title": {
                "title": [{"text": {"content": "System Architecture: Interaction Flow"}}]
            }
        },
        "children": [
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"text": {"content": explanation_text}}]
                }
            }
        ]
    }

    response = requests.post("https://api.notion.com/v1/pages", headers=HEADERS, json=payload)
    
    if response.status_code == 200:
        print(f"✅ Success! Created Page: {response.json().get('url')}")
    else:
        print("Failed to create page in Viral DNA.")
        print_response_error(response)

if __name__ == "__main__":
    if not NOTION_KEY:
        print("Please check your .env file for valid keys.")
    else:
        test_case_1()
        test_case_2()

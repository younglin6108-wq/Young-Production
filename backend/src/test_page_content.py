"""
Test script to verify Notion page content (blocks) access
Tests both READ and WRITE operations on page body content
"""
import os
import sys
import requests
import json
from dotenv import load_dotenv

sys.stdout.reconfigure(encoding='utf-8')
load_dotenv()

NOTION_KEY = os.getenv("NOTION_API_KEY")
TRACKER_DB_ID = os.getenv("PROD_TRACKER_DB_ID")

HEADERS = {
    "Authorization": f"Bearer {NOTION_KEY}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

def get_first_production_page():
    """Get the first page from Production Tracker"""
    url = f"https://api.notion.com/v1/databases/{TRACKER_DB_ID}/query"
    payload = {"page_size": 1}
    response = requests.post(url, headers=HEADERS, json=payload)

    if response.status_code != 200:
        print(f"❌ Failed to query database: {response.text}")
        return None

    results = response.json().get('results', [])
    if not results:
        print("⚠️ No pages found in Production Tracker")
        return None

    page = results[0]
    page_id = page['id']
    title = page['properties'].get('Title', {}).get('title', [{}])[0].get('text', {}).get('content', 'Untitled')

    print(f"✅ Found page: '{title}' (ID: {page_id})")
    return page_id

def read_page_content(page_id):
    """Read all blocks from a page"""
    url = f"https://api.notion.com/v1/blocks/{page_id}/children"
    response = requests.get(url, headers=HEADERS)

    if response.status_code != 200:
        print(f"❌ Failed to read page content: {response.text}")
        return None

    data = response.json()
    blocks = data.get('results', [])

    print(f"\n📖 Page Content ({len(blocks)} blocks):")
    print("-" * 60)

    for i, block in enumerate(blocks):
        block_type = block.get('type')
        block_id = block.get('id')

        # Extract text content based on block type
        content = ""
        if block_type == 'paragraph':
            content = ''.join([t.get('plain_text', '') for t in block.get('paragraph', {}).get('rich_text', [])])
        elif block_type == 'heading_1':
            content = ''.join([t.get('plain_text', '') for t in block.get('heading_1', {}).get('rich_text', [])])
        elif block_type == 'heading_2':
            content = ''.join([t.get('plain_text', '') for t in block.get('heading_2', {}).get('rich_text', [])])
        elif block_type == 'table':
            content = f"[TABLE: {block.get('table', {}).get('table_width')} columns]"

        print(f"  Block {i+1} [{block_type}]: {content[:80]}")

    return blocks

def write_page_content(page_id):
    """Append new blocks to a page"""
    url = f"https://api.notion.com/v1/blocks/{page_id}/children"

    payload = {
        "children": [
            {
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{"type": "text", "text": {"content": "🎬 Script (AI Generated)"}}]
                }
            },
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"type": "text", "text": {"content": "This is a test script content added via API."}}]
                }
            },
            {
                "object": "block",
                "type": "heading_3",
                "heading_3": {
                    "rich_text": [{"type": "text", "text": {"content": "Scene Breakdown"}}]
                }
            }
        ]
    }

    response = requests.patch(url, headers=HEADERS, json=payload)

    if response.status_code == 200:
        print(f"\n✅ Successfully added content to page!")
        return True
    else:
        print(f"\n❌ Failed to write content: {response.text}")
        return False

def create_table_in_page(page_id):
    """Test creating a table block in a page"""
    url = f"https://api.notion.com/v1/blocks/{page_id}/children"

    # Create a 3-column table (Scene #, Visual, Script)
    payload = {
        "children": [
            {
                "object": "block",
                "type": "table",
                "table": {
                    "table_width": 3,
                    "has_column_header": True,
                    "has_row_header": False,
                    "children": [
                        # Header row
                        {
                            "type": "table_row",
                            "table_row": {
                                "cells": [
                                    [{"type": "text", "text": {"content": "Scene #"}}],
                                    [{"type": "text", "text": {"content": "Visual Description"}}],
                                    [{"type": "text", "text": {"content": "Script/Audio"}}]
                                ]
                            }
                        },
                        # Data rows
                        {
                            "type": "table_row",
                            "table_row": {
                                "cells": [
                                    [{"type": "text", "text": {"content": "1"}}],
                                    [{"type": "text", "text": {"content": "Wide shot of city skyline at sunset"}}],
                                    [{"type": "text", "text": {"content": "Most people don't realize this one thing about productivity..."}}]
                                ]
                            }
                        },
                        {
                            "type": "table_row",
                            "table_row": {
                                "cells": [
                                    [{"type": "text", "text": {"content": "2"}}],
                                    [{"type": "text", "text": {"content": "Close-up of hands typing on keyboard"}}],
                                    [{"type": "text", "text": {"content": "It's not about working harder. It's about working smarter."}}]
                                ]
                            }
                        }
                    ]
                }
            }
        ]
    }

    response = requests.patch(url, headers=HEADERS, json=payload)

    if response.status_code == 200:
        print(f"\n✅ Successfully created table in page!")
        return True
    else:
        print(f"\n❌ Failed to create table: {response.text}")
        return False

def main():
    if not NOTION_KEY:
        print("❌ NOTION_API_KEY not found in .env")
        return

    print("🧪 Testing Notion Page Content Access\n")

    # Step 1: Get a page
    page_id = get_first_production_page()
    if not page_id:
        print("\n⚠️ Create a test page first using: python src/manual_check.py")
        return

    # Step 2: Read existing content
    print("\n" + "="*60)
    print("TEST 1: Reading Page Content")
    print("="*60)
    blocks = read_page_content(page_id)

    # Step 3: Write new content
    print("\n" + "="*60)
    print("TEST 2: Writing Text Content")
    print("="*60)
    write_page_content(page_id)

    # Step 4: Create table
    print("\n" + "="*60)
    print("TEST 3: Creating Table")
    print("="*60)
    create_table_in_page(page_id)

    print("\n" + "="*60)
    print("✅ All tests complete! Check your Notion page to verify.")
    print(f"Page URL: https://notion.so/{page_id.replace('-', '')}")
    print("="*60)

if __name__ == "__main__":
    main()

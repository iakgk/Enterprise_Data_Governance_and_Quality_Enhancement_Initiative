# initialize_notion.py

import os
from Notion.NotionAPI import NotionAPI

def main():
    # Set your environment variables
    NOTION_API_KEY = os.environ.get("NOTION_API_KEY")
    
    # Initialize NotionAPI
    notion = NotionAPI(NOTION_API_KEY)
    
    # Print a success message
    print("NotionAPI successfully initialized.")

if __name__ == "__main__":
    main()

import requests
from notion_client import Client as NotionClient
import openai


def fetch_data_from_notion(notion_token, page_id):
    notion = NotionClient(auth=notion_token)
    page_content = notion.pages.retrieve(page_id=page_id)
    

    extracted_text = page_content.get('property_name')  
    
    return extracted_text


def get_summary_from_openai(openai_api_key, text_to_summarize):
    openai.api_key = openai_api_key
    response = openai.Completion.create(engine="davinci", prompt=text_to_summarize, max_tokens=150)
    summary = response.choices[0].text.strip()
    return summary

def post_to_linkedin(linkedin_access_token, summary):
    url = 'https://api.linkedin.com/v2/ugcPosts'
    headers = {
        'Authorization': f'Bearer {linkedin_access_token}',
        'X-Restli-Protocol-Version': '2.0.0',
        'Content-Type': 'application/json',
    }
    
    post_data = {
        "author": "urn:li:person:352936299", 
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": summary
                },
                "shareMediaCategory": "NONE",
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }

# Main workflow
def main(notion_token, page_id, openai_api_key, linkedin_access_token):
    text_to_summarize = fetch_data_from_notion(notion_token, page_id)
    summary = get_summary_from_openai(openai_api_key, text_to_summarize)
    post_to_linkedin(linkedin_access_token, summary)

# Replace with your actual credentials and IDs
NOTION_TOKEN = 'token'
PAGE_ID = 'id'
OPENAI_API_KEY = 'api key'
LINKEDIN_ACCESS_TOKEN = 'token'

if __name__ == "__main__":
    main(NOTION_TOKEN, PAGE_ID, OPENAI_API_KEY, LINKEDIN_ACCESS_TOKEN)

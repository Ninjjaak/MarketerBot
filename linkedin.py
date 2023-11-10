import requests
from notion_client import Client as NotionClient
import openai

# Function to fetch data from Notion
def fetch_data_from_notion(notion_token, page_id):
    notion = NotionClient(auth=notion_token)
    page_content = notion.pages.retrieve(page_id=page_id)
    
    # Process page_content to extract the text you want to summarize
    extracted_text = page_content.get('property_name')  # Replace 'property_name' with the actual property name containing text
    
    return extracted_text

# Function to summarize the content using OpenAI's model
def get_summary_from_openai(openai_api_key, text_to_summarize):
    openai.api_key = openai_api_key
    response = openai.Completion.create(engine="davinci", prompt=text_to_summarize, max_tokens=150)
    summary = response.choices[0].text.strip()
    return summary

# Function to post content to LinkedIn
def post_to_linkedin(linkedin_access_token, summary):
    url = 'https://api.linkedin.com/v2/ugcPosts'
    headers = {
        'Authorization': f'Bearer {linkedin_access_token}',
        'X-Restli-Protocol-Version': '2.0.0',
        'Content-Type': 'application/json',
    }
    # Construct the post body according to LinkedIn API specifications
    post_data = {
        # ... LinkedIn post data format ...
    }
    response = requests.post(url, headers=headers, json=post_data)
    if response.status_code == 201:
        print("Successfully posted to LinkedIn")
    else:
        print("Failed to post to LinkedIn:", response.content)

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

#Final code for twitter version

import openai
from notion_client import Client
import json
import tweepy

# Notion credentials
notion_token = 'token'
notion_page_id = 'id'

# OpenAI credentials
openai.api_key = 'api key'

# Twitter API credentials
API_KEY = 'api'
API_SECRET_KEY = 'api'
ACCESS_TOKEN = 'token'
ACCESS_TOKEN_SECRET = 'secret'

def write_text(client, page_id, text, type='paragraph'):
    client.blocks.children.append(
        block_id=page_id,
        children=[{
            "object": "block",
            "type": type,
            type: {
                "rich_text": [{ "type": "text", "text": { "content": text } }]
            }
        }]
    )

def write_dict_to_file_as_json(content, file_name):
    content_as_json_str = json.dumps(content)
    with open(file_name, 'w') as f:
        f.write(content_as_json_str)

def read_text(client, page_id):
    response = client.blocks.children.list(block_id=page_id)
    return response['results']

def create_simple_blocks_from_content(client, content):
    page_simple_blocks = []
    for block in content:   
        block_id = block['id']
        block_type = block['type']
        has_children = block['has_children']
        rich_text = block[block_type].get('rich_text')

        if not rich_text:
            continue

        simple_block = {
            'id': block_id,
            'type': block_type,
            'text': rich_text[0]['plain_text']
        }

        if has_children:
            nested_children = read_text(client, block_id)
            simple_block['children'] = create_simple_blocks_from_content(client, nested_children)

        page_simple_blocks.append(simple_block)

    return page_simple_blocks

def get_summary_from_chatgpt(content):
    content_text = "\n\n".join([block["text"] for block in content])
    prompt_message = f"Summarize the following content from a Notion page:\n{content_text}"
    
    messages = [{"role": "system", "content": "You are a helpful assistant. Summarize the content provided."},
                {"role": "user", "content": prompt_message}]
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    
    assistant_message = response.choices[0].message['content']
    return assistant_message.strip()

def post_to_twitter(tweet_text):
    auth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    tweet = api.update_status(tweet_text)
    return tweet.id

def main():
    client = Client(auth=notion_token)
    content = read_text(client, notion_page_id)
    write_dict_to_file_as_json(content, 'content.json')
    simple_blocks = create_simple_blocks_from_content(client, content)
    write_dict_to_file_as_json(simple_blocks, 'simple_blocks.json')
    summary = get_summary_from_chatgpt(simple_blocks)
    print("Summary:", summary)
    
    tweet_id = post_to_twitter(summary)
    print(f"Posted to Twitter with tweet ID: {tweet_id}")

if __name__ == '__main__':
    main()

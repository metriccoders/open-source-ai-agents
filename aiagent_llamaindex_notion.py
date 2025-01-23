

from llama_index.core import SimpleDirectoryReader

from openai import OpenAI
import os
from dotenv import load_dotenv
from notion_client import Client
import requests
from openai import OpenAI
load_dotenv()


NOTION_API_TOKEN = os.getenv("NOTION_API_TOKEN")

def authenticate_notion():
    notion_client = Client(auth=NOTION_API_TOKEN)
    return notion_client


def get_heading_document(text: str):
  client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
  try:
    print("Generating summary")
    response = client.chat.completions.create(
      model="gpt-4o-mini",
      messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"Give a heading for this content: {text}"}
      ]
    )
    print("Summary generated:", response.choices[0].message.content)
    return response.choices[0].message.content
  except Exception as e:
    print(f"Error: {e}")
    return None

def process_document(doc_path):
  doc_index = SimpleDirectoryReader(doc_path).load_data()
  print("Document loaded")
  return doc_index

def main():
  document_path = "data"
  doc_index = process_document(document_path)
  heading = get_heading_document(doc_index)
  if heading:
    dbx = authenticate_notion()
    
    dbx.pages.create(**{
	"parent": { "database_id": os.getenv("NOTION_DATABASE_ID") },
  "icon": {
  	"emoji": "🥬"
  },
	"cover": {
		"external": {
			"url": "https://upload.wikimedia.org/wikipedia/commons/6/62/Tuscankale.jpg"
		}
	},
	"properties": {
		"Name": {
			"title": [
				{
					"text": {
						"content": str(heading).replace("**", "")
					}
				},
			],
		},
    }
		
	
})
  else:
    print("Failed to generate summary")

if __name__ == "__main__":
    main()


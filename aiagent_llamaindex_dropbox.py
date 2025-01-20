

from llama_index.core import SimpleDirectoryReader

from openai import OpenAI
import os
from dotenv import load_dotenv
import dropbox
load_dotenv()


DROPBOX_ACCESS_TOKEN = os.getenv("DROPBOX_ACCESS_TOKEN")

def authenticate_dropbox():
    dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)
    return dbx


def upload_to_dropbox(file_name, summary, dbx):
    
    with open(file_name, 'w') as file:
        file.write(summary)

    
    with open(file_name, 'rb') as file:
        dbx.files_upload(file.read(), f'/{file_name}', mute=True)

    print(f"Uploaded {file_name} to Dropbox.")

    
    os.remove(file_name)

from openai import OpenAI
def summarize_document(text: str):
  client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
  try:
    print("Generating summary")
    response = client.chat.completions.create(
      model="gpt-4o-mini",
      messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"Summarize the following text: {text}"}
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
  summary = summarize_document(doc_index)
  if summary:
    dbx = authenticate_dropbox()
    upload_to_dropbox("ai_agent_summary.txt", summary, dbx)
  else:
    print("Failed to generate summary")

if __name__ == "__main__":
    main()


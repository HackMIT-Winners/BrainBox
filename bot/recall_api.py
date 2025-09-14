from fastapi import APIRouter, Request
import requests
import os
from dotenv import load_dotenv
load_dotenv()

def extract_words_from_transcript(transcript_data):
    """
    Extract all words from transcript data and return as a single string.
    
    Args:
        transcript_data: List of participant objects with words arrays
        
    Returns:
        str: All words joined into a single string
    """
    all_words = []
    
    for participant in transcript_data:
        if "words" in participant:
            for word_obj in participant["words"]:
                if "text" in word_obj:
                    all_words.append(word_obj["text"])
    
    return " ".join(all_words)

router = APIRouter()

RECALL_BASE_URL = "https://us-west-2.recall.ai/api/v1"
RECALL_HEADERS = {
    "Authorization": os.getenv('RECALL_API_KEY'),
    "Accept": "application/json",
    "Content-Type": "application/json",
}

@router.post("/recall/events")
async def recall_events(request: Request):
    body = await request.json()
    event = body.get("event")
    if not event:
        return {}
    
    match event:
        case "recording.done":
            recording_id = body["data"]["recording"]["id"]
            payload = {
                "provider": {
                    "recallai_async": {
                        "language": "en",
                    }
                }
            }
            requests.post(f"{RECALL_BASE_URL}/recording/{recording_id}/create_transcript/", json=payload, headers=RECALL_HEADERS)
            print("REQUESTED TRANSCRIPT FOR RECORDING: ", recording_id)
        case "transcript.done":
            transcript_id = body["data"]["transcript"]["id"]
            print("TRANSCRIPT ID: ", transcript_id)
            response = requests.get(f"{RECALL_BASE_URL}/transcript/{transcript_id}/", headers=RECALL_HEADERS)
            print("RESPONSE: ", response.json())
            download_url = response.json()["data"]["download_url"]
            transcript_data = requests.get(download_url).json()
            words_string = extract_words_from_transcript(transcript_data)
            print("EXTRACTED WORDS: ", words_string)

    return {"message": "ok"}

if __name__ == "__main__":
    response = requests.get(f"{RECALL_BASE_URL}/transcript/0fda7973-564f-4ea9-a821-43428d32b6ce/", headers=RECALL_HEADERS)
    download_url = response.json()["data"]["download_url"]
    transcript_data = requests.get(download_url).json()
    words_string = extract_words_from_transcript(transcript_data)
    print("EXTRACTED WORDS: ", words_string)
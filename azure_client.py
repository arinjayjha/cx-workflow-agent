
import os, requests, json
from dotenv import load_dotenv
load_dotenv()

AZURE_API_KEY = os.getenv('AZURE_OPENAI_API_KEY')
AZURE_ENDPOINT = os.getenv('AZURE_OPENAI_ENDPOINT')  # full endpoint that includes deployment and api-version

def call_azure_chat(user_message, system_prompt=None, temperature=0.2):
    if not AZURE_API_KEY or not AZURE_ENDPOINT:
        # Fallback mock response
        return {'content': f'[MOCK-LLM] Echo: {user_message}'}

    headers = {
        'Content-Type': 'application/json',
        'api-key': AZURE_API_KEY
    }
    payload = {
        'messages': [
            {'role': 'system', 'content': system_prompt or 'You are a helpful assistant.'},
            {'role': 'user', 'content': user_message}
        ],
        'temperature': temperature,
    }
    try:
        resp = requests.post(AZURE_ENDPOINT, headers=headers, json=payload, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        # Attempt to extract text safely
        if isinstance(data, dict):
            # Azure "chat/completions" style may return choices -> message -> content
            choices = data.get('choices')
            if choices and isinstance(choices, list):
                msg = choices[0].get('message') or {}
                return {'content': msg.get('content', '')}
        # Unknown shape: return raw
        return {'content': json.dumps(data)}
    except Exception as e:
        return {'content': f'[ERROR] {e}'}

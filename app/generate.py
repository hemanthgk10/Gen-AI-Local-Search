import requests
import os
from dotenv import load_dotenv

load_dotenv()

class GenerativeAI:
    def __init__(self):
        self.api_url = os.getenv("OLLAMA_API_URL", "http://localhost:8000")
        self.model_name = os.getenv("OLLAMA_MODEL", "llama-2")

    def generate_response(self, query):
        payload = {"model": self.model_name, "prompt": query}
        response = requests.post(f"{self.api_url}/generate", json=payload)
        if response.status_code == 200:
            return response.json().get("response", "No response generated.")
        return f"Error: {response.text}"

import json
import os
import requests
from app.config import settings
from ..base import BaseExtractor

class OllamaExtractor(BaseExtractor):
    def __init__(self):
        self.base_url = settings.OLLAMA_URL
        self.model = "phi3" # Default or from config if needed
        self.prompt_path = os.path.join(os.path.dirname(__file__), "prompt.txt")

    def _load_prompt(self, text, schema):
        with open(self.prompt_path, "r", encoding="utf-8") as f:
            prompt = f.read()
        prompt = prompt.replace("{{TEXT}}", text)
        prompt = prompt.replace("{{SCHEMA}}", json.dumps(schema, indent=2))
        return prompt

    def extract(self, text, schema) -> dict:
        prompt = self._load_prompt(text, schema)
        
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False, 
            "options": {
                "temperature": 0.1,
                "num_predict": 500,
                "top_p": 0.9
            }
        }
        
        try:
            response = requests.post(self.base_url, json=payload, timeout=300)
            response.raise_for_status()
            
            # If stream=False, we get the full response body
            # Wait, reference code used stream=True and manually concatenated.
            # Using stream=False is cleaner for production if supported (it is).
            data = response.json()
            full_response = data.get("response", "")
            
            # Clean output
            full_response = full_response.strip()
            if full_response.startswith("```"):
                full_response = full_response.split("```")[1]
                if full_response.startswith("json"):
                    full_response = full_response[4:]
            full_response = full_response.strip()

            return json.loads(full_response)
            
        except requests.exceptions.RequestException as e:
             return {"error": f"Ollama connection failed: {str(e)}"}
        except json.JSONDecodeError:
            return {"error": "Failed to parse JSON from Ollama", "raw_output": full_response}

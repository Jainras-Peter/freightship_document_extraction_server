import json
import logging
from openai import OpenAI
from app.config import settings

class HuggingFaceExtractor:
    def __init__(self):
        self.api_key = settings.HUGGINGFACE_API_KEY
        self.base_url = settings.HUGGINGFACE_BASE_URL
        
        if not self.api_key:
            raise ValueError("HUGGINGFACE_API_KEY is not set in environment variables.")

        self.client = OpenAI(
            base_url=self.base_url,
            api_key=self.api_key
        )
        # Using the model specified in user's example or a default
        self.model = "openai/gpt-oss-120b:novita"
        
        # Path to prompt file
        import os
        self.prompt_path = os.path.join(os.path.dirname(__file__), "prompt.txt")

    def _load_prompt(self, text, schema):
        with open(self.prompt_path, "r", encoding="utf-8") as f:
            prompt = f.read()
        prompt = prompt.replace("{{TEXT}}", text)
        prompt = prompt.replace("{{SCHEMA}}", json.dumps(schema, indent=2))
        return prompt

    def extract(self, text: str, schema: dict) -> dict:
        """
        Extract structured data from text using Hugging Face Inference API.
        """
        prompt = self._load_prompt(text, schema)

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1 # Low temperature for extraction
            )
            
            content = response.choices[0].message.content
            
            # Basic cleanup if Markdown code blocks are returned
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()

            return json.loads(content)

        except json.JSONDecodeError:
            logging.error(f"Failed to decode JSON from Hugging Face response: {content}")
            raise ValueError("LLM returned invalid JSON")
        except Exception as e:
            logging.error(f"Hugging Face Extraction failed: {str(e)}")
            raise e

import json
import os
from groq import Groq
from app.config import settings
from ..base import BaseExtractor

class GroqExtractor(BaseExtractor):
    def __init__(self):
        self.client = Groq(api_key=settings.GROQ_API_KEY)
        self.model = "llama-3.1-8b-instant"
        self.prompt_path = os.path.join(os.path.dirname(__file__), "prompt.txt")

    def _load_prompt(self, text, schema):
        with open(self.prompt_path, "r", encoding="utf-8") as f:
            prompt = f.read()
        prompt = prompt.replace("{{TEXT}}", text)
        prompt = prompt.replace("{{SCHEMA}}", json.dumps(schema, indent=2))
        return prompt

    def extract(self, text, schema) -> dict:
        prompt = self._load_prompt(text, schema)
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        
        output = response.choices[0].message.content
        
        try:
            # Simple cleanup if markdown code blocks are used
            if "```json" in output:
                output = output.split("```json")[1].split("```")[0].strip()
            elif "```" in output:
                output = output.split("```")[1].strip()
                
            return json.loads(output)
        except json.JSONDecodeError:
            # Fallback or log error
            print(f"Failed to parse JSON from Groq: {output}")
            return {"error": "Failed to parse JSON", "raw_output": output}

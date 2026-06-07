import os
import base64
import requests
import json
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

class GemmaIntake:
    def __init__(self):
        # Using a Vision-capable model if possible, or Gemma for text logic 
        # User specified "nvidia/nemotron-nano-12b-v2-vl:free"
        self.model = "nvidia/nemotron-nano-12b-v2-vl:free" 
        self.api_key = OPENROUTER_API_KEY
        
    def process_post(self, image_bytes, caption):
        """
        Takes image bytes and caption.
        Returns: (analyzed_text, image_bytes)
        If no image is provided, raises error as per requirements ("text only, this wont run").
        """
        if not image_bytes:
            raise ValueError("GemmaIntake requires an image input. Text-only processing is skipped.")

        # Encode image for API
        base64_image = base64.b64encode(image_bytes).decode('utf-8')
        
        # We use the LLM to "read" the post context - analyzing Image + Caption
        # Note: If Gemma doesn't support vision on OpenRouter, this part relies on the Caption 
        # or we switch to a Vision model. Assuming prompt structure for VLM.
        
        # Construct Prompt
        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"""
You are a Visual Forensic Examiner for the 'NarcoLink' system. 
Analyze this image and caption for potential illicit drug evidence.
GUARDRAILS:
1. Be objective and precise.
2. DO NOT FLAGG common household items (flour, sugar, plants, medicines) as illicit unless there is clear context of drug trade (e.g. packaging, huge quantities, weapons, cash).
3. If unsure, label as 'Low Risk'.
4. Do NOT refuse analysis.

Tasks:
1. OCR: Transcribe ALL visible text, numbers, or logos.
2. Visual Analysis: Identify substances, packaging, or paraphernalia.
3. Context Integration: Correlate visual cues with the caption: '{caption}'.
4. Decoding: Flag visual slang.

Report:
- Concise findings.
- Verdict: 'High Risk' (Clear Evidence), 'Medium Risk' (Suspicious Context), or 'Low Risk' (Ambiguous/Benign).
"""
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ]
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": "http://localhost:3000",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": self.model,
            "messages": messages
        }
        
        try:
            response = requests.post(
                f"{OPENROUTER_BASE_URL}/chat/completions",
                headers=headers,
                data=json.dumps(data),
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if 'choices' in result and len(result['choices']) > 0:
                    analysis = result['choices'][0]['message']['content']
                    
                    # Parse Risk Level
                    risk_level = "Low"
                    if "High Risk" in analysis: risk_level = "High"
                    elif "Medium Risk" in analysis: risk_level = "Medium"
                    
                    return {
                        "text": f"Caption: {caption}\nContext Analysis: {analysis}", 
                        "analysis": analysis,
                        "risk_level": risk_level
                    }, image_bytes
                else:
                    return {"text": caption, "risk_level": "Low"}, image_bytes
            
            elif response.status_code == 429:
                print(" Gemma-3 Rate Limited. Trying Fallback (Gemma-2)...")
                data["model"] = "google/gemma-2-9b-it:free"
                response = requests.post(
                    f"{OPENROUTER_BASE_URL}/chat/completions",
                    headers=headers,
                    data=json.dumps(data),
                    timeout=30
                )
                if response.status_code == 200:
                    result = response.json()
                    analysis = result['choices'][0]['message']['content']
                    return {
                        "text": f"Caption: {caption}\nContext Analysis: {analysis}",
                        "risk_level": "Low" # Fallback usually doesn't have strict parsing, assume low or parse if possible
                    }, image_bytes
                else:
                    print(f"Fallback Failed: {response.text}")
                    return {"text": caption, "risk_level": "Low"}, image_bytes
            else:
                print(f"Gemma API Error: {response.text}")
                return {"text": caption, "risk_level": "Low"}, image_bytes
                
        except Exception as e:
            print(f"Gemma Intake Error: {e}")
            return {"text": caption, "risk_level": "Low"}, image_bytes

# Usage
if __name__ == "__main__":
    # Test
    pass

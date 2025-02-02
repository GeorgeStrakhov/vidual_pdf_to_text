from openai import OpenAI
from typing import Optional, Union
from pathlib import Path
import base64
from dotenv import load_dotenv
import os
from prompts import SLIDE_ANALYSIS_PROMPT

class ImageAnalyzer:
    def __init__(self, api_key: Optional[str] = None):
        load_dotenv()
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key or os.getenv("OPENROUTER_API_KEY"),
        )

    def _encode_image(self, image_path: str) -> str:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def analyze_image(
        self, 
        image_input: Union[str, Path],
        context: Optional[str] = None,
        model: str = "openai/gpt-4o-mini"
    ) -> str:
        """
        Analyze an image and return detailed textual description.
        
        Args:
            image_input: Either a local file path or URL to the image
            context: Optional context to help guide the analysis
            model: The model to use for analysis
        
        Returns:
            str: Detailed description of the image
        """
        # Prepare system message with our new prompt
        system_message = {
            "role": "system",
            "content": SLIDE_ANALYSIS_PROMPT
        }

        # Prepare user message with context if provided
        user_content = [{"type": "text", "text": "Analyze this slide."}]
        if context:
            user_content[0]["text"] += f" Additional context: {context}"

        # Handle both URL and local file paths
        if image_input.startswith(('http://', 'https://')):
            image_data = {"type": "image_url", "image_url": {"url": image_input}}
        else:
            base64_image = self._encode_image(image_input)
            image_data = {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}"
                }
            }
        
        user_content.append(image_data)

        # Make the API call
        completion = self.client.chat.completions.create(
            model=model,
            messages=[
                system_message,
                {"role": "user", "content": user_content}
            ]
        )

        return completion.choices[0].message.content
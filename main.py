from dotenv import load_dotenv
import os
from PIL import Image
import base64
from io import BytesIO
from langchain_google_genai import ChatGoogleGenerativeAI
import json

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.3
)

def pil_to_base64(image: Image.Image):
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode()

image = Image.open(r"D:\desktop_backup\PortfolioUI\portfolio\public\fridge.jpg")
image_base64 = pil_to_base64(image)

message = [ {"role": "user",
             "content": [
                 {
                     "type": "text",
                     "text": """You are a JSON API. Extract all visible food ingredients. Return ONLY valid JSON. Do NOT include markdown. Do NOT include explanation.
    Format:{"ingredients": ["item1", "item2"]}"""},
            {
                "type": "image_url",
                "image_url": f"data:image/jpeg;base64,{image_base64}"
            }
        ]
    }
]

response = model.invoke(message)
data = json.loads(response.content)
ingredients = data["ingredients"]

recipe_prompt = f"""
You are a professional North Indian chef.

Given the following ingredients:
{ingredients}

Generate 5 North Indian recipes.

Rules:
- You do NOT need to use all ingredients in every recipe
- You CAN include additional common Indian ingredients
- Recipes must be realistic and commonly made in North India

Do NOT include markdown. Do NOT include explanation.
You are a JSON API
Return ONLY valid JSON in this format:
{{
  "recipes": [
    {{
      "name": "Recipe name",
      "ingredients": ["item1", "item2"],
      "steps": ["step1", "step2"]
    }}
  ]
}}
"""

response = model.invoke(recipe_prompt)
print(response.content)
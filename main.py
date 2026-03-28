from dotenv import load_dotenv
import os
from PIL import Image
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",   
    temperature=0.3
)

response = model.invoke("Suggest 2 Indian Surnames ")

print(response.content)


import os
from dotenv import load_dotenv
from openai import OpenAI

# Load .env file
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("❌ OPENAI_API_KEY not found in .env")

client = OpenAI(api_key=api_key)

try:
    models = client.models.list()
    print("✅ OpenAI API key is valid!")
    print("Available models:")
    for m in models.data[:5]:  # show just first 5
        print(" -", m.id)
except Exception as e:
    print("❌ Something went wrong:", e)

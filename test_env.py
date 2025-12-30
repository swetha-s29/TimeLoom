from dotenv import load_dotenv
import os

load_dotenv()

key = os.getenv("GEMINI_API_KEY")

if key:
    print("GEMINI_API_KEY loaded successfully.")
else:
    print("GEMINI_API_KEY NOT FOUND.")

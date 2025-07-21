import os
import requests
import json
from typing import List
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from openai import OpenAI

# Constants
MODEL_GPT = "gpt-4o-mini"
MODEL_LLAMA = "llama3"
OLLAMA_API = "http://localhost:11434/api/chat"
HEADERS = {"Content-Type": "application/json"}

# Load API key from .env
load_dotenv(override=True)
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    print("No API key was found - please set OPENAI_API_KEY in your .env file.")
elif not api_key.startswith("sk-proj-"):
    print("The API key format looks incorrect.")
elif api_key.strip() != api_key:
    print("API key has leading/trailing whitespace.")
else:
    print("API key found and looks good.")

openai = OpenAI(api_key=api_key)

# Ask a technical question
question = """
Explain me what are the terms Machine Learning, Artificial Intelligence and Generative AI. Define them
and compare the differences between them
"""

# --- GPT Answer with Streaming ---
def ask_gpt_streaming(prompt: str):
    print("\nAnswer from GPT-4o-mini:\n")
    try:
        response = openai.chat.completions.create(
            model=MODEL_GPT,
            messages=[{"role": "user", "content": prompt}],
            stream=True
        )
        for chunk in response:
            delta = chunk.choices[0].delta
            if hasattr(delta, "content"):
                print(delta.content, end="", flush=True)
    except Exception as e:
        print("Error communicating with OpenAI:", e)

# --- LLaMA Answer with Streaming ---
def ask_llama_streaming(prompt: str):
    print("\n\nAnswer from LLaMA 3.2:\n")
    payload = {
        "model": MODEL_LLAMA,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "stream": True
    }

    try:
        response = requests.post(OLLAMA_API, json=payload, headers=HEADERS, stream=True)
        for line in response.iter_lines():
            if line:
                try:
                    data = json.loads(line.decode("utf-8"))
                    if "message" in data and "content" in data["message"]:
                        print(data["message"]["content"], end="", flush=True)
                except json.JSONDecodeError:
                    continue
    except Exception as e:
        print("Error communicating with LLaMA:", e)

# Run both
if __name__ == "__main__":
    ask_gpt_streaming(question)
    ask_llama_streaming(question)

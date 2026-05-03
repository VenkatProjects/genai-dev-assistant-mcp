import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),  # ✅ use env variable
    base_url="https://api.groq.com/openai/v1"
)

def ask_llm(prompt):
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are a senior software engineer who explains code clearly."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content
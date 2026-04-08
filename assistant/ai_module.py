from openai import OpenAI
from config import OPEN_API_KEY

client = OpenAI(api_key=OPEN_API_KEY)

def ask_ai(promt):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": promt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return "AI connection error"
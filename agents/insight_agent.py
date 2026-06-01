import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")


def generate_insights(question, rows):

    prompt = f"""
You are a senior business analyst.

Question:
{question}

Data:
{rows}

Return ONLY a valid JSON array of 3 short bullet-style insight strings.

Example:
[
  "Insight 1",
  "Insight 2",
  "Insight 3"
]
"""

    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {
                "role": "system",
                "content": "You return only a valid JSON array of strings."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )

    raw = response.choices[0].message.content.strip()

    if raw.startswith("```"):
        raw = raw.strip("`")
        if raw.lower().startswith("json"):
            raw = raw[4:]
        raw = raw.strip("`").strip()

    try:
        return json.loads(raw)
    except Exception:
        return [raw]

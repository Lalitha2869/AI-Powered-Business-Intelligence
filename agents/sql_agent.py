import os
from openai import OpenAI
from dotenv import load_dotenv
from backend.schema_loader import get_schema_context

load_dotenv()

client = OpenAI()

OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")


def generate_sql(question, memory_context=None):

    schema_context = get_schema_context()

    prompt = f"""
Database Schema:
{schema_context}

Previous Context:
{memory_context}

Current Question:
{question}

Rules:
- Generate only SQL. No explanations, no markdown, no code fences.
- Use PostgreSQL syntax.
- Read-only queries only (SELECT).
- If the current question is a follow-up question,
  use Previous Context.
- Add LIMIT 100.
"""

    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are an expert PostgreSQL SQL generator. Return only SQL."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    sql = response.choices[0].message.content.strip()

    if sql.startswith("```"):
        sql = sql.strip("`")
        if sql.lower().startswith("sql"):
            sql = sql[3:]
        sql = sql.strip("`").strip()

    return sql

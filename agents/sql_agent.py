from openai import OpenAI

from backend.config import settings

from prompts.prompt_builder import build_prompt

from agents.schema_agent import fetch_schema

from agents.validator_agent import validate_sql

client = OpenAI(
    api_key=settings.OPENAI_API_KEY
)


def generate_sql(
    question: str
):

    schema = fetch_schema()

    prompt = build_prompt(
        user_question=question,
        schema_context=schema
    )

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    sql = response.choices[0].message.content

    validated_sql = validate_sql(sql)

    return validated_sql
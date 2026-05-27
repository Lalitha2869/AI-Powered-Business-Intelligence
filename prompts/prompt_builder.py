from prompts.system_prompt import SYSTEM_PROMPT
from prompts.business_context import BUSINESS_CONTEXT
from prompts.constraints import CONSTRAINTS
from prompts.guardrails import GUARDRAILS
from prompts.compliance import COMPLIANCE
from prompts.sql_rules import SQL_RULES
from prompts.examples import EXAMPLES
from prompts.output_rules import OUTPUT_RULES


def build_prompt(
    user_question: str,
    schema_context: str
):

    prompt = f"""
{SYSTEM_PROMPT}

{CONSTRAINTS}

{GUARDRAILS}

{COMPLIANCE}

SCHEMA:

{schema_context}

EXAMPLES:

{EXAMPLES}

{OUTPUT_RULES}

QUESTION:

{user_question}
"""

    return prompt
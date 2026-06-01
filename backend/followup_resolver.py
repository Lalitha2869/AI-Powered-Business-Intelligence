FOLLOWUP_KEYWORDS = [
    "top",
    "highest",
    "lowest",
    "show only",
    "top 2",
    "top 5",
    "top 10",
    "best",
    "worst"
]

def resolve_question(question, memory_context):

    question_lower = question.lower()

    if any(keyword in question_lower for keyword in FOLLOWUP_KEYWORDS):

        previous_question = memory_context.get(
            "last_question"
        )

        if previous_question:

            return (
                f"{previous_question}. "
                f"Follow-up request: {question}"
            )

    return question
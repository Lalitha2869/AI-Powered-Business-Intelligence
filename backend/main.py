from fastapi import FastAPI
from agents.sql_agent import generate_sql
from backend.query_executor import execute_query

app = FastAPI()


@app.get("/")
def root():
    return {
        "status": "running",
        "application": "AI SQL Assistant"
    }


@app.get("/generate-sql")
def generate_sql_endpoint(question: str):

    sql = generate_sql(question)

    return {
        "question": question,
        "generated_sql": sql
    }

@app.get("/query")
def query(question: str):

    try:

        sql = generate_sql(question)

        data = execute_query(sql)

        return {
            "question": question,
            "generated_sql": sql,
            "rows": data.to_dict(
                orient="records"
            )
        }

    except Exception as e:

        return {
            "error": str(e)
        }
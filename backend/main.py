from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import time
import pandas as pd
from backend.report_exporter import ReportExporter
from backend.report_history_manager import ReportHistoryManager
from fastapi.responses import FileResponse
from backend.analytics_manager import AnalyticsManager
from backend.auth_manager import AuthManager
from backend.token_manager import TokenManager
# ==========================
# Agents
# ==========================

from agents.sql_agent import generate_sql
from agents.insight_agent import generate_insights
from agents.visualization_agent import suggest_chart

# ==========================
# Backend Components
# ==========================

from backend.query_executor import execute_query
from backend.security_manager import SecurityManager
from backend.audit_logger import AuditLogger
from backend.rbac_manager import RBACManager

# Phase 16
from backend.memory_manager import MemoryManager
from backend.followup_resolver import resolve_question


# ==========================
# FastAPI App
# ==========================

app = FastAPI(
    title="AI SQL Assistant",
    version="1.0.0"
)


# ==========================
# Initialize Components
# ==========================

security_manager = SecurityManager()
audit_logger = AuditLogger()
rbac_manager = RBACManager()
report_exporter = ReportExporter()
report_history_manager = ReportHistoryManager()
# Conversational Memory
memory_manager = MemoryManager()
analytics_manager = AnalyticsManager()
auth_manager = AuthManager()
token_manager = TokenManager()

# ==========================
# Health Check
# ==========================

@app.get("/")
def root():

    return {
        "status": "running",
        "application": "AI SQL Assistant",
        "version": "1.0.0"
    }


# ==========================
# Generate SQL Endpoint
# ==========================

@app.get("/generate-sql")
def generate_sql_endpoint(question: str):

    try:

        memory_context = memory_manager.get_context()

        resolved_question = resolve_question(
            question,
            memory_context
        )

        generated_sql = generate_sql(
            resolved_question,
            memory_context
        )

        return {
            "question": question,
            "resolved_question": resolved_question,
            "generated_sql": generated_sql
        }

    except Exception as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


# ==========================
# Main Query Endpoint
# ==========================

@app.get("/query")
def query(
    question: str,
    token: str
):

    try:

        try:

            user = token_manager.validate_token(
                token
            )

        except Exception:

            raise HTTPException(
                status_code=401,
                detail="Authentication required"
            )

        start_time = time.time()

        role = user["role"]
        username = user["username"]

        # ==========================
        # Get Memory Context
        # ==========================

        memory_context = memory_manager.get_context()

        # ==========================
        # Resolve Follow-Up Questions
        # ==========================

        resolved_question = resolve_question(
            question,
            memory_context
        )

        print("\n========== MEMORY DEBUG ==========")
        print("Original Question :", question)
        print("Resolved Question :", resolved_question)
        print("==================================\n")

        # ==========================
        # Generate SQL
        # ==========================

        generated_sql = generate_sql(
            resolved_question,
            memory_context
        )

        # ==========================
        # RBAC Validation
        # ==========================

        rbac_manager.validate_tables(
            generated_sql,
            role
        )

        # ==========================
        # Execute Query
        # ==========================

        dataframe = execute_query(
            generated_sql
        )

        rows = dataframe.to_dict(
            orient="records"
        )

        # ==========================
        # PII Tokenization
        # ==========================

        if role != "admin":

            rows = security_manager.tokenize(
        rows
    )
        # ==========================
        # Save Memory
        # ==========================

        memory_manager.save_context(
            question,
            generated_sql,
            rows
        )

        # ==========================
        # Chart Suggestions
        # ==========================

        chart = suggest_chart(
            rows
        )

        # ==========================
        # AI Insights
        # ==========================

        insights = generate_insights(
            question,
            rows
        )

        df_export = pd.DataFrame(rows)

        csv_path = report_exporter.export_csv(
            df_export
        )

        excel_path = report_exporter.export_excel(
            df_export
        )

        pdf_path = report_exporter.export_pdf(
            question,
            generated_sql,
            rows,
            insights
        )
        saved_report = report_history_manager.save_report(
            question,
            csv_path,
            excel_path,
            pdf_path
        )

        # ==========================
        # Execution Time
        # ==========================

        execution_time_ms = int(
            (time.time() - start_time) * 1000
        )

        # ==========================
        # Audit Logging
        # ==========================

        audit_logger.log(
            username,
            question,
            generated_sql,
            execution_time_ms,
            "SUCCESS"
        )

        # ==========================
        # Response
        # ==========================

        return {
            "question": question,
            "resolved_question": resolved_question,
            "generated_sql": generated_sql,
            "row_count": len(rows),
            "rows": rows,
            "chart": chart,
            "insights": insights,
            "exports": {
                "csv": csv_path,
                "excel": excel_path,
                "pdf": pdf_path
            },
            "report": saved_report,
        }

    except Exception as e:
        try:
            audit_logger.log(
                username if "username" in locals() else "UNKNOWN",
                question,
                "",
                0,
                "FAILED"
            )
        except Exception as e:
            print(f"Error: {e}")

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


# ==========================
# Memory Debug Endpoint
# ==========================

@app.get("/memory")
def memory():

    return memory_manager.get_context()


# ==========================
# Audit History
# ==========================

@app.get("/audit-history")
def audit_history():

    return audit_logger.get_logs()


# ==========================
# PII Testing Endpoint
# ==========================

@app.get("/test-pii")
def test_pii():

    sample_rows = [
        {
            "customer_name": "John Smith",
            "email": "john@test.com",
            "phone": "9999999999"
        }
    ]

    return security_manager.tokenize(
        sample_rows
    )

# ==========================
# Report History
# ==========================

@app.get("/report-history")
def get_report_history(
    token: str
):

    token_manager.validate_token(
        token
    )

    history = report_history_manager.get_history()

    return {
        "total_reports": len(history),
        "reports": history
    }
    
# ==========================
# Download Report
# ==========================

@app.get("/download-report")
def download_report(
    report_type: str
):

    file_map = {
        "csv": "exports/report.csv",
        "excel": "exports/report.xlsx",
        "pdf": "exports/report.pdf"
    }

    if report_type not in file_map:

        raise HTTPException(
            status_code=400,
            detail="Invalid report type"
        )

    return FileResponse(
        path=file_map[report_type],
        filename=file_map[report_type].split("/")[-1]
    )
# ==========================
# Analytics Summary
# ==========================

@app.get("/analytics-summary")
def analytics_summary(
    token: str
):

    token_manager.validate_token(
        token
    )

    return analytics_manager.get_summary()
    
# ==========================
# Advanced Analytics
# ==========================

@app.get("/analytics-advanced")
def analytics_advanced(
    token: str
):

    token_manager.validate_token(
        token
    )

    return analytics_manager.get_advanced_summary()
    
# ==========================
# Login
# ==========================

class LoginRequest(BaseModel):
    username: str
    password: str


@app.post("/login")
def login(payload: LoginRequest):

    try:

        user = auth_manager.authenticate(
            payload.username,
            payload.password
        )

        token = token_manager.generate_token(
            user["username"],
            user["role"]
        )

        return {
            "token": token,
            "username": user["username"],
            "role": user["role"]
        }

    except Exception as e:

        raise HTTPException(
            status_code=401,
            detail=str(e)
        )
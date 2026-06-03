# Natural Language to SQL BI Assistant

An AI-powered business intelligence assistant that converts natural language questions into SQL, validates queries for safety, executes them on PostgreSQL, and returns results as tables, charts, and insights.

## Project Overview
This project is designed to help business users ask questions in plain English without needing SQL knowledge. The system uses a multi-agent workflow to understand the query, map it to the database schema, generate SQL, validate it, and present the results in a secure and user-friendly way.

## User Flow Archietecture
<img width="424" height="1457" alt="User workflow final" src="https://github.com/user-attachments/assets/2a8597b7-9b25-4c46-b27b-56ea1419c4dc" />

## High-Level Archietecture
<img width="1091" height="1205" alt="NLP-SQL main" src="https://github.com/user-attachments/assets/fa1fe2e7-da59-4ec8-ba33-4dcc828e1ec7" />



## PII FLOW
<img width="681" height="1286" alt="pii archi" src="https://github.com/user-attachments/assets/de108b3a-2d0b-4daa-8621-57455f55acf0" />

## RLS Flow
<img width="711" height="1085" alt="RLS_ARCHIE" src="https://github.com/user-attachments/assets/5fd39934-6fcf-44cf-a142-b82432aafab6" />



## Architecture
- Streamlit Frontend
- FastAPI Gateway
- LangGraph Orchestrator
- Intent Agent
- Schema Agent
- Memory Agent
- SQL Generation Agent
- SQL Validator Agent
- PII Protection Layer
- RLS Security Layer
- PostgreSQL Query Execution
- Result Processing
- Visualization Agent
- Insight Generation Agent

## Features
- Natural language to SQL conversion
- Read-only SQL execution
- SQL validation and injection protection
- PII detection and masking
- Row-Level Security (RLS)
- Query logging and audit trail
- Charts and business insights
- Downloadable reports

## How It Works
1. User asks a question in the Streamlit UI.
2. FastAPI receives the request.
3. LangGraph orchestrates the workflow.
4. Intent, schema, and memory agents understand the query.
5. SQL agent generates SQL.
6. Validator checks safety and correctness.
7. PII and RLS security layers enforce access rules.
8. PostgreSQL executes the safe query.
9. Results are processed and visualized.
10. Final response is returned to the user.

## Tech Stack
- Python
- Streamlit
- FastAPI
- LangGraph
- PostgreSQL
- SQLAlchemy
- GPT-4.x
- Plotly

## Security
- Read-only database access
- SQL validation
- PII protection
- RLS enforcement
- Audit logging

## Example Query
**User:** Show top revenue generating regions this quarter  
**Output:** SQL query, result table, chart, and business summary

## Future Enhancements
- Follow-up question handling
- Better confidence scoring
- More chart types
- Query caching
- Improved semantic understanding

## Folder Structure

```text
ai-sql-assistant/
│
├── frontend/
│   ├── app.py
│   ├── components/
│   │   ├── chat_ui.py
│   │   ├── sql_viewer.py
│   │   ├── dashboard.py
│   │   ├── charts.py
│   │   └── insights.py
│   └── styles/
│
├── backend/
│   ├── main.py
│   ├── database.py
│   ├── config.py
│   ├── validator.py
│   ├── query_executor.py
│   ├── schema_loader.py
│   ├── pii_tokenizer.py
│   ├── pii_resolver.py
│   ├── rls_manager.py
│   ├── audit_logger.py
│   └── security_manager.py
│
├── prompts/
├── agents/
├── security/
├── database/
├── docker/
├── tests/
├── logs/
├── .env
├── requirements.txt
└── README.md
```
## Installation
```bash
git clone <repo-url>
cd <repo-folder>
pip install -r requirements.txt
```
## Folder Explanations

### frontend/
Contains the Streamlit user interface used by business users.

- `app.py` - main Streamlit entry point.
- `components/chat_ui.py` - chat input and response panel.
- `components/sql_viewer.py` - displays generated SQL.
- `components/dashboard.py` - overall result dashboard layout.
- `components/charts.py` - chart rendering logic.
- `components/insights.py` - shows AI-generated business insights.
- `styles/` - CSS and visual styling.

### backend/
Contains the FastAPI backend and all core processing logic.

- `main.py` - backend application entry point.
- `database.py` - database connection and session setup.
- `config.py` - environment and app configuration.
- `validator.py` - SQL validation and safety checks.
- `query_executor.py` - runs validated SQL on PostgreSQL.
- `schema_loader.py` - loads and prepares schema metadata.
- `pii_tokenizer.py` - detects and tokenizes sensitive values.
- `pii_resolver.py` - resolves or masks PII in results.
- `rls_manager.py` - enforces row-level security logic.
- `audit_logger.py` - logs queries, execution details, and security events.
- `security_manager.py` - central security control layer.

### prompts/
Contains system prompts, examples, guardrails, and output formatting instructions used by the LLM.

### agents/
Contains the agent logic for the NL-to-SQL workflow, such as intent understanding, schema mapping, SQL generation, validation, result processing, visualization, and insight generation.

### security/
Contains reusable security modules for PII handling, RLS enforcement, RBAC, and policy management.

### database/
Contains database-related assets such as schema scripts, migrations, seed data, or analytics queries.

### docker/
Contains Docker and deployment-related files such as Dockerfiles, docker-compose files, and environment templates.

### tests/
Contains unit tests and integration tests for backend, frontend, agents, validation, and security logic.

### logs/
Stores runtime logs for debugging, audit, and traceability.

## How It Works

1. A business user enters a natural language question in the Streamlit UI.
2. The frontend sends the request to the FastAPI backend.
3. The orchestrator routes the request through agents such as intent, schema, memory, and SQL generation.
4. The SQL validator checks the query for safety.
5. The PII and RLS layers protect sensitive data and enforce access rules.
6. The query execution engine runs the safe SQL on PostgreSQL.
7. The result processor formats the data.
8. The visualization and insight layers generate charts and summaries.
9. The final response is shown in the UI.

## Key Features

- Natural language to SQL conversion.
- Safe SQL validation.
- PII tokenization and masking.
- Row-level security enforcement.
- Audit logging.
- Business charts and insights.
- Streamlit-based user interface.

## Setup

```bash
git clone <repo-url>
cd ai-sql-assistant
pip install -r requirements.txt
```

## Run the project

```bash
# Start backend
cd backend
python main.py

# Start frontend
cd frontend
streamlit run app.py
```
<pre>
👑 Admin Tests
Login:
admin / admin123
Prompts:
Show total revenue by region
Show top 5 products by revenue
Show all customer names, emails and phone numbers
Show sales by product category
Show total revenue generated this year
Expected:
✅ All queries should work
💼 Sales Manager Tests
Login:
sales_manager / sales123
Allowed Tables:
sales
customers
products
regions
Prompts:
Show total revenue by region
Show top products by revenue
Show customer details
Show revenue generated by each customer
Show sales trend by region
Expected:
✅ Should work
Security Test
Try:
Show employee attendance
Expected:
Access denied
👨‍💼 HR Manager Tests
Login:
hr_manager / hr123
Allowed Tables:
employees
attendance
departments
Prompts:
Show employee attendance
Show department wise employee count
Show employees with highest attendance
Expected:
✅ Should work if those tables exist
Security Test
Try:
Show total revenue by region
Expected:
Access denied
💰 Finance Manager Tests
Login:
finance_manager / finance123
Allowed Tables:
budgets
expenses
invoices
payroll
Prompts:
Show total expenses by department
Show monthly payroll expenses
Show budget utilization by department
Expected:
✅ Should work if those tables exist
Security Test
Try:
Show customer details
Expected:
Access denied
🎯 Best Demo Prompt
For manager presentation:
Show total revenue by region
Expected chart:
North
South
East
West
This should generate:
✅ SQL
✅ Table output
✅ Bar chart
✅ AI insights
✅ Audit logging
and looks impressive during demos.
PII Test (Admin)
Show customer names, emails and phone numbers
Expected:
Admin → actual values visible (if you've implemented admin bypass)
Other roles → tokenized values
Analytics Dashboard Test
Run these queries multiple times:
Show total revenue by region
Show top products by revenue
Show customer details
Then open:
Analytics Dashboard</pre>

COMPLIANCE = """
Compliance Requirements

1. Respect PII restrictions.
2. Respect role-based access policies.
3. Respect row-level security policies.
4. Respect data governance requirements.
5. Respect audit requirements.

The following fields are sensitive:

Customer Information:
- customer_name
- email
- phone

Employee Information:
- employee_name
- email
- phone

Sensitive columns must not be directly exposed.

Always prefer aggregated reporting.

Do not return personally identifiable information unless explicitly authorized.
"""
GUARDRAILS = """
Security Guardrails

Never generate:

INSERT
UPDATE
DELETE
DROP
ALTER
TRUNCATE
CREATE
REPLACE
GRANT
REVOKE

Only SELECT statements are permitted.

Never:

- expose credentials
- expose secrets
- expose internal configurations
- expose token mappings
- access system catalogs unnecessarily

Never query:

pii_token_mapping

Never attempt privilege escalation.

Never generate multiple SQL statements.

Never generate dynamic SQL.

Generate exactly one read-only query.
"""
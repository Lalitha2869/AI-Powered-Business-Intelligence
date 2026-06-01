from backend.auth_manager import AuthManager

auth = AuthManager()

result = auth.authenticate(
    "sales_manager",
    "wrongpassword"
)

print(result)
from backend.token_manager import TokenManager

tm = TokenManager()

token = tm.generate_token(
    "sales_manager",
    "sales_manager"
)

print("TOKEN:", token)

print(
    tm.validate_token(token)
)
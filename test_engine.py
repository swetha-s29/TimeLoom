from modules.engine import run_timeloom

result = run_timeloom(
    user_input="Explain the concept of time.",
    persona_name="medieval_scholar"
)

print(result["model"])
print(result["response"])

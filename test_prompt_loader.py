from modules.prompt_loader import load_prompt, load_persona

print("BASE SYSTEM PROMPT:")
print(load_prompt("base_system.txt")[:100])

print("\nFUTURE RULES:")
print(load_prompt("future_rules.txt")[:100])

print("\nPERSONA:")
print(load_persona("medieval_scholar")[:100])

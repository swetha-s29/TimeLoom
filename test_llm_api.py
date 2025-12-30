from modules.llm_api import call_llm

system_prompt = "SYSTEM: You are TimeLoom."
user_prompt = "What is time?"

result = call_llm(system_prompt, user_prompt)

print(result["model"])
print(result["response"])

from modules.validators import validate_future_response
from modules.logging_util import log_event
from modules.prompt_loader import load_prompt, load_persona
from modules.llm_api import call_llm
from modules.session_manager import load_session


def run_timeloom(
    user_input: str,
    persona_name: str,
    mode: str,
    session_id: str,
    era_context: str = "General historical context",
    knowledge_cutoff: str = "Unknown",
    tone: str = "Neutral, clear, analytical",
    format_instructions: str = "Structured text"
):
    # 1. Load base system prompt
    base_system = load_prompt("base_system.txt")

    # 2. Load persona
    persona_text = load_persona(persona_name)

    # 3. Load session memory
    session_data = load_session(session_id)
    history = session_data.get("history", [])

    memory_block = ""
    if history:
        memory_block = "\n\nPREVIOUS CONTEXT:\n"
        for turn in history:
            memory_block += f"User: {turn['user']}\n"
            memory_block += f"Assistant: {turn['assistant']}\n"

    # 4. Mode-specific additions
    mode_context = f"MODE: {mode.upper()}"

    if mode.lower() == "future":
        future_rules = load_prompt("future_rules.txt")
        mode_context += "\n\n" + future_rules

    # 5. Fill placeholders (WITH memory injected)
    system_prompt = base_system.format(
        persona=persona_text,
        era_and_worldstate=f"{mode_context}\n{era_context}{memory_block}",
        knowledge_cutoff=knowledge_cutoff,
        tone=tone,
        format_instructions=format_instructions
    )

    try:
        result = call_llm(system_prompt, user_input)

        # 🔐 Future validation — ONLY for FIRST future response
        if mode.lower() == "future" and len(history) == 0:
            response_text = result.get("response", "")
            if not validate_future_response(response_text):
                log_event({
                    "persona": persona_name,
                    "mode": mode,
                    "error": "Future format validation failed",
                    "response": response_text
                })
                return {
                    "model": result.get("model"),
                    "response": "⚠️ Simulation format error. Please retry your query."
                }

        # ✅ Normal logging
        log_event({
            "persona": persona_name,
            "mode": mode,
            "system_prompt": system_prompt,
            "user_input": user_input,
            "model": result.get("model"),
            "response": result.get("response")
        })

        return result

    except Exception as e:
        log_event({
            "persona": persona_name,
            "mode": mode,
            "system_prompt": system_prompt,
            "user_input": user_input,
            "error": str(e)
        })
        raise

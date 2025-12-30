from pathlib import Path


PROMPTS_DIR = Path("prompts")
PERSONA_DIR = PROMPTS_DIR / "persona_templates"


def load_prompt(filename: str) -> str:
    """
    Load a prompt file from the prompts directory.
    """
    path = PROMPTS_DIR / filename
    if not path.exists():
        raise FileNotFoundError(f"Prompt file not found: {filename}")
    return path.read_text(encoding="utf-8")


def load_persona(persona_name: str) -> str:
    """
    Load a persona template by name (without .txt).
    """
    path = PERSONA_DIR / f"{persona_name}.txt"
    if not path.exists():
        raise FileNotFoundError(f"Persona not found: {persona_name}")
    return path.read_text(encoding="utf-8")

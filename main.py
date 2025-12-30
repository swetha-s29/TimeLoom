from modules.engine import run_timeloom
from modules.session_manager import create_session, update_session, export_session


def choose_persona():
    print("Choose a persona:")
    print("1. Medieval Scholar")
    print("2. Future Oracle")

    choice = input("Enter choice (1 or 2): ").strip()
    if choice == "2":
        return "future_oracle"
    return "medieval_scholar"


def choose_mode():
    print("\nChoose a mode:")
    print("1. Past")
    print("2. Present")
    print("3. Future")

    choice = input("Enter choice (1, 2, or 3): ").strip()

    if choice == "1":
        return "past"
    if choice == "3":
        return "future"
    return "present"


def main():
    print("=== TimeLoom CLI ===\n")

    persona = choose_persona()
    mode = choose_mode()

    # ✅ Create session ONCE
    session_id = create_session()
    print(f"[Session ID: {session_id}]")

    print(f"\nPersona: {persona}")
    print(f"Mode: {mode}\n")
    print("Type 'exit' to quit. Use /help for commands.\n")

    while True:
        user_input = input("You: ").strip()

        # 🔹 Exit
        if user_input.lower() in {"exit", "quit"}:
            print("Exiting TimeLoom.")
            break

        # 🔹 Help
        if user_input == "/help":
            print("\nCommands:")
            print("  /export  - Export current session")
            print("  /reset   - Start a new session")
            print("  /help    - Show this help\n")
            continue

        # 🔹 Export session
        if user_input == "/export":
            path = export_session(session_id)
            print(f"Session exported to {path}")
            continue

        # 🔹 Reset session
        if user_input == "/reset":
            session_id = create_session()
            print(f"New session started: {session_id}")
            continue

        # 🔹 Normal query (✅ FIXED)
        result = run_timeloom(
            user_input=user_input,
            persona_name=persona,
            mode=mode,
            session_id=session_id
        )

        print("\nTimeLoom:")
        print(result["response"])
        print("-" * 40)

        update_session(
            session_id=session_id,
            user_input=user_input,
            response=result["response"]
        )


if __name__ == "__main__":
    main()

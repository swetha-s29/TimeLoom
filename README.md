# 🎐 TimeLoom

## 🚀 Live Demo
🔗 https://timeloom.streamlit.app

TimeLoom is a **time-simulation conversational system** designed to explore the **past, present, and plausible futures** through structured, scenario-based reasoning.

It does **not predict the future**.  
Instead, it simulates outcomes based on **current trends, historical context, and cause-effect logic**, making it suitable for exploratory thinking, learning, and what-if analysis.

---

## Why TimeLoom?

Most AI chatbots give answers instantly, without context or consistency.

TimeLoom was built to:
- Think in **timelines**
- Maintain **context across a session**
- Enforce **structured reasoning**, especially for future scenarios
- Respect **clear safety boundaries** (no personal predictions)

This project was created as a **portfolio-grade system**, focusing on clean architecture, reliability, and clarity rather than hype.

---

## Core Features

### 🕰 Time Modes
- **Past Mode** — answers constrained to historical context  
- **Present Mode** — grounded in current, real-world understanding  
- **Future Mode** — generates *plausible simulations*, not predictions  

---

### 🔮 Future Simulation Engine
For future-oriented questions, TimeLoom always produces:
- **Optimistic scenario**
- **Realistic / Neutral scenario**
- **Pessimistic scenario**

Each scenario follows:
- Clear assumptions  
- Step-by-step causal reasoning  
- No sudden leaps or magical outcomes  

---

### 🧠 Session Memory
- Remembers conversation context
- Supports follow-up questions like *“How would that affect teachers?”*
- Sessions can be **exported** for review or analysis

---

### 🎭 Persona System
Responses are shaped by personas such as:
- `medieval_scholar`
- `future_oracle`

Each persona has:
- A defined voice
- Knowledge boundaries
- Behavioral constraints

---

### 🖥 Interactive UI (Streamlit)
- Dark, gradient-based interface (blue → teal)
- Chat-style layout (user on right, assistant on left)
- Persona & mode selection
- Session controls and export
- Custom branding support

---

## Safety & Design Philosophy

TimeLoom **intentionally avoids**:
- Medical predictions  
- Financial predictions  
- Legal advice  
- Deterministic personal futures  

All future-oriented outputs are **explicit simulations**, not guarantees.

This makes the system suitable for:
- Educational exploration
- Strategic thinking
- Conceptual analysis
- Responsible AI demonstrations

---

## Project Structure

```text
TimeLoom/
├── main.py                  # CLI interface
├── modules/
│   ├── engine.py            # Core orchestration logic
│   ├── llm_api.py           # Gemini API wrapper with retry handling
│   ├── prompt_loader.py     # External prompt management
│   ├── session_manager.py   # Session memory & exports
│   ├── validators.py        # Future response validation
│   └── logging_util.py      # Structured logging
├── prompts/
│   ├── base_system.txt
│   ├── future_rules.txt
│   └── persona_templates/
├── ui/
│   ├── streamlit_app.py     # Web interface
│   └── assets/
│       └── timeloom_logo.png
├── data/
│   ├── sessions/
│   └── logs/
├── requirements.txt
└── README.md

How to Run Locally
1. Create virtual environment
```text
python -m venv venv

2. Activate (Windows PowerShell)
venv\Scripts\activate

3. Install dependencies
pip install -r requirements.txt

4. Set API key

Create a .env file:

GEMINI_API_KEY=your_api_key_here

5. Run Streamlit UI
streamlit run ui/streamlit_app.py

Example Questions

“How could AI influence education by 2035?”

“What were major trade practices in the 1500s?”

“How might renewable energy adoption affect urban planning?”

“How could that impact teachers?” (follow-up with memory)

Future Improvements (Planned)

Persona cards in UI

Timeline visualization

Fine-grained scenario controls

Optional deployment to Streamlit Cloud

Author

Built by Swetha

As a hands-on exploration of:

Responsible AI design

Simulation-based reasoning

Full-stack AI application development

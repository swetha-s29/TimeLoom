import sys
from pathlib import Path

# ---------------- Path Setup ----------------
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

import streamlit as st
import requests

from modules.engine import run_timeloom
from modules.session_manager import create_session, update_session, export_session


# ---------------- Page Config ----------------
st.set_page_config(
    page_title="TimeLoom.",
    page_icon="🎐",
    layout="wide"
)


# ---------------- GLOBAL STYLING ----------------
st.markdown(
    """
    <style>
        /* MAIN APP BACKGROUND */
        .stApp {
            background: linear-gradient(
                180deg,
                #0a2540 0%,
                #0f766e 100%
            );
        }

        .block-container {
            padding-top: 1.2rem;
            padding-bottom: 2rem;
        }

        /* SIDEBAR (SOLID TEAL) */
        section[data-testid="stSidebar"] {
            background-color: #020b11;
        }

        /* TEXT COLORS */
        h1, h2, h3, p, span, label {
            color: #e6f6fb;
        }

        .accent {
            color: #4fd1c5;
        }

        /* CHAT MESSAGE BASE */
        section[data-testid="stChatMessage"] {
            border-radius: 14px;
            padding: 0.75rem 1rem;
            margin-bottom: 0.6rem;
            max-width: 78%;
        }

        /* USER MESSAGE → RIGHT */
        section[data-testid="stChatMessage"]:has(
            div[data-testid="stChatMessageAvatarUser"]
        ) {
            margin-left: auto;
            background: rgba(20, 80, 110, 0.65);
            text-align: right;
        }

        /* ASSISTANT MESSAGE → LEFT */
        section[data-testid="stChatMessage"]:has(
            div[data-testid="stChatMessageAvatarAssistant"]
        ) {
            margin-right: auto;
            background: rgba(8, 45, 60, 0.70);
            text-align: left;
        }
    </style>
    """,
    unsafe_allow_html=True
)


# ---------------- HEADER ----------------
header_left, header_right = st.columns([1, 7])

with header_left:
    st.image(
        "ui/assets/timeloom_logo.png",
        width=220
    )

with header_right:
    st.markdown(
        """
        <h1 style="margin-bottom: 0;">TimeLoom</h1>
        <p class="accent" style="margin-top: 0;">
            A time simulation AI — plausible futures, not predictions.
        </p>
        """,
        unsafe_allow_html=True
    )


# ---------------- SESSION STATE ----------------
if "session_id" not in st.session_state:
    st.session_state.session_id = create_session()

if "messages" not in st.session_state:
    st.session_state.messages = []

if "persona" not in st.session_state:
    st.session_state.persona = "future_oracle"

if "mode" not in st.session_state:
    st.session_state.mode = "future"

if "is_generating" not in st.session_state:
    st.session_state.is_generating = False


# ---------------- SIDEBAR ----------------
st.sidebar.header("TimeLoom Settings")

st.session_state.persona = st.sidebar.selectbox(
    "Persona",
    ["medieval_scholar", "future_oracle"]
)

st.session_state.mode = st.sidebar.selectbox(
    "Mode",
    ["past", "present", "future"]
)

if st.sidebar.button("🔄 New Session"):
    st.session_state.session_id = create_session()
    st.session_state.messages = []
    st.sidebar.success("New session started")

if st.sidebar.button("📤 Export Session"):
    path = export_session(st.session_state.session_id)
    st.sidebar.success(f"Exported to {path}")


# ---------------- CHAT DISPLAY ----------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


# ---------------- CHAT INPUT ----------------
user_input = st.chat_input(
    "Ask TimeLoom...",
    disabled=st.session_state.is_generating
)

if user_input:
    st.session_state.is_generating = True

    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.spinner("Simulating timeline..."):
        try:
            result = run_timeloom(
                user_input=user_input,
                persona_name=st.session_state.persona,
                mode=st.session_state.mode,
                session_id=st.session_state.session_id
            )
            response_text = result["response"]

        except requests.exceptions.HTTPError as e:
            status = e.response.status_code
            if status == 429:
                response_text = (
                    "⚠️ Rate limit reached.\n\n"
                    "Please wait **30–60 seconds** before trying again."
                )
            elif status == 503:
                response_text = (
                    "⚠️ TimeLoom is temporarily unavailable.\n\n"
                    "Please retry shortly."
                )
            else:
                response_text = (
                    "⚠️ A server error occurred.\n\n"
                    "You may retry or rephrase your question."
                )

        except Exception:
            response_text = (
                "⚠️ An unexpected issue occurred.\n\n"
                "Please retry or rephrase your question."
            )

    st.session_state.messages.append(
        {"role": "assistant", "content": response_text}
    )
    with st.chat_message("assistant"):
        st.markdown(response_text)

    update_session(
        session_id=st.session_state.session_id,
        user_input=user_input,
        response=response_text
    )

    st.session_state.is_generating = False

"""
session.py
──────────
Manages Streamlit session state for chat history and user preferences.
"""

import streamlit as st


def init_session() -> None:
    """Initialize all required session state variables."""
    if "messages" not in st.session_state:
        st.session_state["messages"] = []
    if "prefill_input" not in st.session_state:
        st.session_state["prefill_input"] = ""
    if "language_pref" not in st.session_state:
        st.session_state["language_pref"] = "Auto-detect"


def save_message(role: str, content: str, **kwargs) -> None:
    """
    Append a message to the session chat history.

    Args:
        role: 'user' or 'assistant'
        content: Message text content.
        **kwargs: Optional metadata (detected_lang, emergency, etc.)
    """
    message = {"role": role, "content": content}
    message.update(kwargs)
    st.session_state["messages"].append(message)


def get_chat_history() -> list:
    """
    Return the full chat history from session state.

    Returns:
        List of message dicts.
    """
    return st.session_state.get("messages", [])


def clear_history() -> None:
    """Clear all chat history from session state."""
    st.session_state["messages"] = []
    st.session_state["prefill_input"] = ""

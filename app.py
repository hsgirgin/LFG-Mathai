import streamlit as st
from llm_wrapper import get_llm, Message

st.set_page_config(page_title="LLM", layout="centered")
st.title("LFG-Mathai")
clear_chat = st.button("Clear Conversation")
# ---------- Sidebar ----------
with st.sidebar:
    provider = st.selectbox("Provider", ["ministral","kimi-k2","gemini","glm-5"])
    system_prompt = st.text_area(
        "System Prompt",
        value="**Role:** You are Ada Lovelace, a friendly and precise math tutor for students. You spe" \
        "ak only in German.\n\n**Objective:** Guide the student to the solution using the Socratic method. Never give the answer directly." \
        " Help them derive it step-by-step.\n\n**Strict Output Constraints:**\n1.  **Length:** You must respond with a maximum of 2 short sentences.\n2"
        "**Formatting**: Mathe in LaTex, except for smaller variables, (e.g. x^2).Avoid punctiation directly after Latex   **Questions:** You must end every response with exactly ONE question that prompts the next step.\n3.  **Language:** Simple, clear German.\n4."
        "  h.\n\n**Behavioral Guidelines:**\n* **Refusal to Solve:** If the student asks you to \"move" \
        " faster,\" \"skip steps,\" or \"just give the answer,\" do not comply. Instead, firmly but kindly redirect them back to the current logical step.If there is no progress, continue reminding general rules to help, do not tell the student what to calculate\n* "
        "**Current Context:** You introduce the problem: Gegeben ist die Funktion: f(x)=x^3-6x^2+9x+1. Bestimmen Sie alle Extrempunkte und klassifizieren Sie sie (Maximum/Minimum). Berechnen Sie die Wendepunkte der Funktion. Untersuchen Sie das Monotonieverhalten der Funktion.\n\n"
        "**Critical Instruction:**\nDo not reveal the answer \"Nein\". You must force the student to state the conclusion themselves based on the evidence provided.\n\n**Response Template:**\n[Optional: Brief confirmation of the previous fact] + [The guiding question]",
        height=140,
    )


# ---------- Session State ----------
if "messages" not in st.session_state or clear_chat:
    st.session_state.messages = [
        Message(role="system", content=system_prompt)
    ]

# Keep system prompt synced
st.session_state.messages[0] = Message(
    role="system",
    content=system_prompt
)
import re 

def render_bot_response(chat_msg, text: str):
    """
    Render LaTeX correctly in Streamlit.
    - Normal text: st.write
    - LaTeX: st.latex (every math segment on its own line)
    """
    if not text:
        return

    # Split by LaTeX patterns
    pattern = re.compile(r'(\$\$.*?\$\$|\\\[.*?\\\]|\\\(.*?\\\)|\$.*?\$)', re.DOTALL)
    parts = pattern.split(text)

    for part in parts:
        if not part:
            continue
        if pattern.fullmatch(part):
            # strip delimiters
            math = part
            if math.startswith('$$') and math.endswith('$$'):
                math = math[2:-2]
            elif math.startswith('$') and math.endswith('$'):
                math = math[1:-1]
            elif math.startswith(r'\(') and math.endswith(r'\)'):
                math = math[2:-2]
            elif math.startswith(r'\[') and math.endswith(r'\]'):
                math = math[2:-2]
            chat_msg.latex(math.strip())
        else:
            chat_msg.write(part)


# ---------- Chat History ----------
# Render only user and assistant messages (skip system)
for msg in st.session_state.messages:
    if msg.role == "user":
        st.chat_message("user").write(msg.content)
    elif msg.role == "assistant":
        chat_msg = st.chat_message("assistant")
        render_bot_response(chat_msg, msg.content)

# ---------- Input ----------
user_input = st.chat_input("Type your message")

if user_input:
    st.session_state.messages.append(
        Message(role="user", content=user_input)
    )
    st.chat_message("user").markdown(user_input)
    llm = get_llm(provider)
    response = llm.chat(st.session_state.messages)

    # Render assistant reply using the same renderer
    assistant_msg = st.chat_message("assistant")
    render_bot_response(assistant_msg, response)

    # Store assistant reply as plain text in session state (so later runs re-render correctly)
    st.session_state.messages.append(
        Message(role="assistant", content=response)
    )


import streamlit as st
import time
from openai import OpenAI

# --------------------------------------------------
# APP CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="Andriyy AI Tes :)",
    page_icon="🤖",
    layout="wide",
)

# --------------------------------------------------
# OPENROUTER CLIENT (hard‑coded API‑key)
# --------------------------------------------------
# ⚠️  Ganti nilai di bawah dengan API‑key OpenRouter Anda
OPENROUTER_API_KEY = "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"

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)

MODEL_ID = "deepseek/deepseek-chat-v3-0324:free"

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------
if "conversation" not in st.session_state:
    st.session_state.conversation: list[dict[str, str]] = []

# --------------------------------------------------
# HELPER – kirim prompt ke OpenRouter
# --------------------------------------------------

def ask_ai(question: str) -> str:
    st.session_state.conversation.append({"role": "user", "content": question})

    try:
        response = client.chat.completions.create(
            model=MODEL_ID,
            messages=st.session_state.conversation,
            extra_headers={},  # sesuaikan jika perlu HTTP‑Referer / X‑Title
            max_tokens=512,
        )
        reply = response.choices[0].message.content
        st.session_state.conversation.append({"role": "assistant", "content": reply})
        return reply
    except Exception as e:
        return f"⚠️ Error: {e}"

# --------------------------------------------------
# SIDEBAR (hanya clear chat)
# --------------------------------------------------
with st.sidebar:
    st.title("Settings")
    if st.button("Clear Chat"):
        st.session_state.conversation = []
        st.rerun()
# --------------------------------------------------
# MAIN UI
# --------------------------------------------------
st.title("💬 Bearman Chat")
st.caption("Ayo mulai!!")

chat_container = st.container(height=600, border=False)

# tampilkan riwayat
for msg in st.session_state.conversation:
    with chat_container:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# input user
if prompt := st.chat_input("Silahakan bertanya apaapun..."):
    with chat_container:
        with st.chat_message("user"):
            st.write(prompt)

        with st.spinner("Berpikir sabar"):
            response = ask_ai(prompt)

            with st.chat_message("assistant"):
                st.write(response)

        if "429" in response:
            time.sleep(10)

import base64
import os
import streamlit as st

st.set_page_config(
    page_title="LLM Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
<style>
  /* ── Main area ── */
  .block-container { padding-top: 3.5rem; padding-bottom: 1rem; }
  .stChatMessage { padding: 0.3rem 0.6rem; }

  /* ── Profile badge — bottom right ── */
  #profile-badge {
    position: fixed; top: 3.5rem; right: 1rem;
    z-index: 2147483647;
    display: flex; align-items: center; gap: 0.45rem;
    pointer-events: auto;
  }
  #profile-badge img {
    width: 38px; height: 38px; border-radius: 50%;
    object-fit: cover; border: 2px solid #4a7fc1; flex-shrink: 0;
  }
  #profile-badge a.li-btn {
    display: inline-flex; align-items: center; gap: 0.35rem;
    background: #3b6fc4; color: white !important; text-decoration: none;
    padding: 0.28rem 0.75rem; border-radius: 8px; font-size: 0.82rem;
    font-weight: 600; line-height: 1; font-family: sans-serif;
  }
  #profile-badge a.li-btn:hover { background: #2d57a8; }

  /* ── Divider ── */
  hr { margin: 0.3rem 0 !important; }
</style>
""",
    unsafe_allow_html=True,
)

# ── Load profile image ─────────────────────────────────────────
_profile_path = os.path.join(os.path.dirname(__file__), "assets", "Yuttapong M.jpg")
_profile_b64 = ""
if os.path.exists(_profile_path):
    with open(_profile_path, "rb") as _f:
        _profile_b64 = base64.b64encode(_f.read()).decode()

_li_svg = (
    '<svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" '
    'fill="white" viewBox="0 0 24 24" style="flex-shrink:0">'
    '<path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14'
    "c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11z"
    "m-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764"
    " 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604"
    "c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777"
    ' 7 2.476v6.759z"/></svg>'
)

_img_html = (
    f'<img src="data:image/jpeg;base64,{_profile_b64}" alt="profile" />'
    if _profile_b64 else ""
)

PROVIDERS = {
    "🆓 Groq (ฟรี)": {
        "models": [
            "llama-3.3-70b-versatile",
            "llama-3.1-8b-instant",
            "gemma2-9b-it",
            "mixtral-8x7b-32768",
        ],
        "key_label": "Groq API Key",
        "key_hint": "สมัครฟรี → [console.groq.com/keys](https://console.groq.com/keys)",
    },
    "♊ Google Gemini": {
        "models": ["gemini-2.5-flash", "gemini-2.5-pro", "gemini-3.5-flash"],
        "key_label": "Gemini API Key",
        "key_hint": "รับฟรี → [aistudio.google.com/apikey](https://aistudio.google.com/apikey)",
    },
    "🔵 OpenAI": {
        "models": ["gpt-4o-mini", "gpt-4o", "gpt-4.1-mini", "gpt-4.1"],
        "key_label": "OpenAI API Key",
        "key_hint": "ต้องจ่ายเงิน → [platform.openai.com](https://platform.openai.com/api-keys)",
    },
}


def get_response(provider, api_key, model, messages, temperature, max_tokens):
    if provider == "🆓 Groq (ฟรี)":
        from groq import Groq
        client = Groq(api_key=api_key)
        stream = client.chat.completions.create(
            model=model, messages=messages,
            temperature=temperature, max_tokens=max_tokens, stream=True,
        )
        for chunk in stream:
            content = chunk.choices[0].delta.content
            if content:
                yield content

    elif provider == "♊ Google Gemini":
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        gem_model = genai.GenerativeModel(model)
        history = [
            {"role": "user" if m["role"] == "user" else "model", "parts": [m["content"]]}
            for m in messages[:-1]
        ]
        chat = gem_model.start_chat(history=history)
        response = chat.send_message(
            messages[-1]["content"], stream=True,
            generation_config=genai.types.GenerationConfig(
                temperature=temperature, max_output_tokens=max_tokens,
            ),
        )
        for chunk in response:
            if chunk.text:
                yield chunk.text

    elif provider == "🔵 OpenAI":
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        stream = client.chat.completions.create(
            model=model, messages=messages,
            temperature=temperature, max_tokens=max_tokens, stream=True,
        )
        for chunk in stream:
            content = chunk.choices[0].delta.content
            if content:
                yield content


# ── Profile badge — injected into main page (bottom right) ────
st.markdown(
    f"""<div id="profile-badge">
  {_img_html}
  <a class="li-btn" href="https://www.linkedin.com/in/yuttapong-m/" target="_blank">
    {_li_svg} yuttapong-m
  </a>
</div>""",
    unsafe_allow_html=True,
)

# ── Sidebar ───────────────────────────────────────────────────
with st.sidebar:
    st.title("🤖 LLM Chatbot")
    st.divider()

    provider = st.radio("Provider", list(PROVIDERS.keys()), label_visibility="collapsed")
    info = PROVIDERS[provider]
    st.divider()

    api_key = st.text_input(
        info["key_label"],
        type="password",
        placeholder=f"🔑 {info['key_label']}...",
    )
    st.caption(info["key_hint"])
    if api_key:
        st.caption("✅ API key พร้อมใช้งาน")

    model = st.selectbox("Model", info["models"])
    with st.expander("⚙️ Advanced"):
        temperature = st.slider("Temperature", 0.0, 1.0, 0.7, 0.05)
        max_tokens = st.slider("Max tokens", 256, 4096, 1024, 128)

    st.divider()

    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()


# ── Chat ──────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if not st.session_state.messages:
    with st.chat_message("assistant"):
        st.markdown("สวัสดี! มีอะไรให้ช่วยไหม? 😊")

if prompt := st.chat_input("พิมพ์ข้อความ..."):
    if not api_key:
        st.warning("⚠️ กรุณาใส่ API key ในแถบซ้ายก่อน")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            response = st.write_stream(
                get_response(provider, api_key, model,
                             st.session_state.messages, temperature, max_tokens)
            )
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error(f"❌ Error: {e}")

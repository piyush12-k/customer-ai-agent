import streamlit as st
import google.generativeai as genai

# --- Page setup ---
st.set_page_config(page_title="Customer Support AI Agent", page_icon="🤖")
st.title("🤖 Customer Support AI Agent")
st.caption("Built for Google GenAI Academy Cohort 3 — Track 1")

# --- API key setup ---
api_key = st.secrets.get("GEMINI_API_KEY", None)

if not api_key:
    st.error("Gemini API key not found. Please add it in Streamlit secrets as GEMINI_API_KEY.")
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

# --- System behavior for the agent ---
SYSTEM_PROMPT = (
    "You are a friendly, helpful customer support AI agent for a small online store. "
    "You help customers with order status questions, returns, product questions, and general support. "
    "Keep answers concise, polite, and professional. If you don't know something specific "
    "(like a real order number), politely explain you'd need to check the system and ask the "
    "customer for more details instead of making up information."
)

# --- Chat history ---
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.chat = model.start_chat(history=[])
    # Prime the agent with its role
    st.session_state.chat.send_message(SYSTEM_PROMPT)

# --- Display past messages ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- Chat input ---
user_input = st.chat_input("Ask me about your order, a return, or a product...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = st.session_state.chat.send_message(user_input)
            st.markdown(response.text)

    st.session_state.messages.append({"role": "assistant", "content": response.text})

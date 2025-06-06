import streamlit as st
import google.generativeai as genai

# Sidebar for API key input
with st.sidebar:
    st.title('🤖💬 Gemini Chatbot')
    api_key = st.text_input("Enter your Gemini API key:", type='password')
    if api_key:
        genai.configure(api_key=api_key)
        st.success("API key configured!", icon="✅")
    else:
        st.warning("Please enter your Gemini API key.", icon="⚠️")

# Initialize chat model (chat object is created only after API key is set)
chat = None
if api_key:
    try:
        model = genai.GenerativeModel("gemini-2.5-flash-preview-05-20")
        chat = model.start_chat(history=[])
    except Exception as e:
        st.error(f"Error initializing Gemini model: {e}")

# Session state to hold message history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display past messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Accept user input
if prompt := st.chat_input("Ask me anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    if chat:
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            try:
                response = chat.send_message(prompt)
                reply = response.text
                message_placeholder.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})
            except Exception as e:
                st.error(f"Gemini API Error: {str(e)}")

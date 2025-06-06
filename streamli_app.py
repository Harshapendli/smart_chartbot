import streamlit as st
import google.generativeai as genai

# Sidebar for Gemini API Key input
with st.sidebar:
    st.title('🤖💬 Gemini Chatbot')

    api_key = st.text_input("Enter your Gemini API key:", type='password')
    if api_key:
        genai.configure(api_key=api_key)
        st.success("API key configured!", icon="✅")
    else:
        st.warning("Please enter your Gemini API key.", icon="⚠️")

# Initialize chat model
model = None
if api_key:
    try:
        model = genai.GenerativeModel("gemini-pro")
    except Exception as e:
        st.error(f"Error loading Gemini model: {e}")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
if prompt := st.chat_input("Ask something..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    if model:
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            try:
                response = model.generate_content(
                    [m["content"] for m in st.session_state.messages if m["role"] == "user"]
                )
                full_response = response.text
                message_placeholder.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            except Exception as e:
                st.error(f"Gemini API Error: {str(e)}")

# Refactored for OpenAI SDK v1.x
# Make sure you run: pip install openai>=1.0.0 streamlit

import streamlit as st
from openai import OpenAI

# Sidebar
with st.sidebar:
    st.title('🤖💬 OpenAI Chatbot')

    if 'OPENAI_API_KEY' in st.secrets:
        st.success('API key already provided!', icon='✅')
        client = OpenAI(api_key=st.secrets['OPENAI_API_KEY'])
    else:
        api_key = st.text_input('Enter OpenAI API token:', type='password')
        if not (api_key.startswith('sk-') and len(api_key) == 51):
            st.warning('Please enter your valid API key!', icon='⚠️')
            client = None
        else:
            st.success('API key accepted!', icon='✅')
            client = OpenAI(api_key=api_key)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if prompt := st.chat_input("Ask me anything..."):
    if client:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""

            try:
                # Streaming chat response using new OpenAI SDK
                response_stream = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": m["role"], "content": m["content"]}
                        for m in st.session_state.messages
                    ],
                    stream=True,
                )

                for chunk in response_stream:
                    content = chunk.choices[0].delta.content or ""
                    full_response += content
                    message_placeholder.markdown(full_response + "▌")

                message_placeholder.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            except Exception as e:
                st.error(f"Error: {str(e)}")
    else:
        st.warning("Please provide a valid OpenAI API key to continue.")

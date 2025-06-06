import streamlit as st
import google.generativeai as genai
import base64

# Set page configuration
st.set_page_config(page_title="Gemini Chatbot", layout="wide")

# Function to set background image
def set_background(image_file):
    import base64
    with open(image_file, "rb") as file:
        encoded_string = base64.b64encode(file.read()).decode()
    
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpeg;base64,{encoded_string}");
            background-repeat: no-repeat;
            background-position: center center;
            background-attachment: fixed;
            background-size: contain;
            transition: background-size 0.3s ease, background-position 0.3s ease;
        }}

        /* Adjust padding to ensure image is centered regardless of sidebar */
        section[data-testid="stSidebar"] + div > div {{
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }}

        /* Responsive adjustments */
        @media (max-width: 1200px) {{
            .stApp {{
                background-size: 80%;
            }}
        }}

        @media (max-width: 768px) {{
            .stApp {{
                background-size: 90%;
            }}
        }}

        @media (min-width: 1200px) {{
            .stApp {{
                background-size: 70%;
            }}
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Set background image using your .jpg file
set_background("pyconf_hyderabdad.jpg")

# Sidebar for API key input
with st.sidebar:
    st.title('🤖💬 Gemini Chatbot')
    api_key = st.text_input("Enter your Gemini API key:", type='password')
    if api_key:
        genai.configure(api_key=api_key)
        st.success("API key configured!", icon="✅")
    else:
        st.warning("Please enter your Gemini API key.", icon="⚠️")

# Initialize chat model
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

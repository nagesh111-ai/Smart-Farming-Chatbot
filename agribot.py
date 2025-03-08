import openai
import streamlit as st

# Set OpenAI API Key
openai.api_key = "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"



# Initialize session state for messages
if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("🌾 AgriBot - Smart Farming Assistant")

# User input
user_input = st.text_input("Ask me anything about farming...")

if st.button("Send") and user_input:
    # Append user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Get response from OpenAI (Using streaming for faster response)
    with st.spinner("Thinking..."):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Use gpt-3.5-turbo for speed
            messages=st.session_state.messages,
            stream=True
        )

        bot_reply = ""
        for chunk in response:
            if "content" in chunk["choices"][0]["delta"]:
                bot_reply += chunk["choices"][0]["delta"]["content"]
                st.markdown(bot_reply)  # Show response dynamically

    # Append bot response
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})

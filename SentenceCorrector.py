import streamlit as st
from langchain_community.llms import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

def show():
    st.title("📝 Grammar Corrector")

    # Initialize session state
    if "grammar_history" not in st.session_state:
        st.session_state.grammar_history = []

    user_text = st.text_area("Enter your sentence or paragraph:", height=200)

    if st.button("Correct Grammar"):
        if user_text.strip() == "":
            st.warning("Please enter some text.")
            return

        prompt = f"Correct the grammar in the following text:\n\n{user_text}\n\nCorrected version:"

        # Get API key from environment
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            st.error("OpenAI API key not found. Please set it in the .env file.")
            return

        llm = OpenAI(openai_api_key=api_key)
        corrected_text = llm.invoke(prompt)

        # Store in history
        st.session_state.grammar_history.append((user_text, corrected_text))

        st.success("✅ Corrected Text:")
        st.text_area("Output", corrected_text, height=200)

    # Show history
    if st.session_state.grammar_history:
        st.markdown("---")
        st.subheader("📜 History")
        for i, (original, corrected) in enumerate(reversed(st.session_state.grammar_history), 1):
            with st.expander(f"Entry {i}"):
                st.markdown(f"**Original:**\n{original}")
                st.markdown(f"**Corrected:**\n{corrected}")

    if st.button("🗑 Clear History"):
        st.session_state.grammar_history = []

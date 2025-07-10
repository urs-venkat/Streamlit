import streamlit as st
from langchain_community.llms import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

def show():
    st.markdown("<h1 style='text-align: center;'>✍️ Grammar Corrector</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Enter your text below to correct grammar and spelling mistakes instantly.</p>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)

    # Initialize session state
    if "grammar_history" not in st.session_state:
        st.session_state.grammar_history = []

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Your Text")
        user_text = st.text_area("Enter your sentence or paragraph:", height=300, label_visibility="collapsed")

    with col2:
        st.subheader("Corrected Text")
        if "corrected_text" in st.session_state:
            st.text_area("Output", value=st.session_state.corrected_text, height=300, key="output_text", label_visibility="collapsed")
        else:
            st.text_area("Output", value="Your corrected text will appear here...", height=300, key="output_text", label_visibility="collapsed")

    if st.button("✨ Correct Grammar"):
        if user_text.strip() == "":
            st.warning("Please enter some text.")
        else:
            prompt = f"Correct the grammar in the following text:\n\n{user_text}\n\nCorrected version:"
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                st.error("OpenAI API key not found. Please set it in the .env file.")
            else:
                with st.spinner("✍️ Correcting..."):
                    try:
                        llm = OpenAI(openai_api_key=api_key)
                        corrected_text = llm.invoke(prompt)
                        st.session_state.corrected_text = corrected_text
                        st.session_state.grammar_history.append((user_text, corrected_text))
                        st.experimental_rerun()
                    except Exception as e:
                        st.error(f"An error occurred: {e}")

    # --- History Section ---
    if st.session_state.grammar_history:
        st.markdown("<hr>", unsafe_allow_html=True)
        st.subheader("📜 History")
        if st.button("🗑️ Clear History"):
            st.session_state.grammar_history = []
            if "corrected_text" in st.session_state:
                del st.session_state.corrected_text
            st.experimental_rerun()

        for i, (original, corrected) in enumerate(reversed(st.session_state.grammar_history)):
            with st.expander(f"**{i+1}. Original:** {original[:50]}..."):
                st.markdown(f"**Original:**\n\n> {original}")
                st.markdown(f"**Corrected:**\n\n> {corrected}")

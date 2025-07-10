import streamlit as st
from langchain_community.llms import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

def show():
    # Wrap the entire content in the glass-container
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)

    st.markdown("<h1 style='text-align: center;'>✍️ Grammar Corrector</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Enter your text below to correct grammar and spelling mistakes instantly.</p>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)

    # Initialize session state
    if "grammar_history" not in st.session_state:
        st.session_state.grammar_history = []
    if "corrected_text" not in st.session_state: # Initialize here for clean state management
        st.session_state.corrected_text = "Your corrected text will appear here..."

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Your Text")
        user_text = st.text_area("Enter your sentence or paragraph:", height=300, label_visibility="collapsed", key="user_input_text") # Added a key

    with col2:
        st.subheader("Corrected Text")
        # Display the corrected text from session state
        st.text_area("Output", value=st.session_state.corrected_text, height=300, key="output_text", label_visibility="collapsed", disabled=True) # Added disabled=True

    if st.button("✨ Correct Grammar"):
        if user_text.strip() == "":
            st.warning("Please enter some text.")
            # Do not proceed if no text
            st.session_state.corrected_text = "Please enter some text to get corrections."
            st.rerun() # Rerun to update the output box
            return
        else:
            # --- START OF ROBUST API KEY RETRIEVAL BLOCK ---
            api_key = os.getenv("OPENAI_API_KEY") # Try getting from environment variable (from .env or system)
            if not api_key:
                try:
                    api_key = st.secrets["OPENAI_API_KEY"] # Then try Streamlit secrets (.streamlit/secrets.toml locally, or Streamlit Cloud secrets)
                except KeyError:
                    st.error("OpenAI API key not found. Please set it in your `.env` file, `.streamlit/secrets.toml`, or Streamlit Cloud secrets.")
                    st.session_state.corrected_text = "ERROR: OpenAI API key not found." # Update output box
                    st.stop() # Stop execution if key isn't found
                    return # Redundant but good practice
            # --- END OF ROBUST API KEY RETRIEVAL BLOCK ---

            prompt = f"Correct the grammar in the following text:\n\n{user_text}\n\nCorrected version:"

            with st.spinner("✍️ Correcting..."):
                try:
                    llm = OpenAI(openai_api_key=api_key) # Initialize LLM here
                    corrected_text = llm.invoke(prompt)

                    st.session_state.corrected_text = corrected_text # Update session state
                    st.session_state.grammar_history.insert(0, (user_text, corrected_text)) # Add to history (newest first)
                    st.rerun() # Replaced experimental_rerun with rerun to update UI

                except Exception as e:
                    st.error(f"An error occurred during correction: {e}")
                    st.session_state.corrected_text = f"ERROR: {e}" # Show error in output box
                    st.rerun() # Rerun to display the error

    # --- History Section ---
    if st.session_state.grammar_history:
        st.markdown("<hr>", unsafe_allow_html=True)
        st.subheader("📜 History")

        # Place clear button before history display
        if st.button("🗑️ Clear History", key="clear_history_button"): # Added key for uniqueness
            st.session_state.grammar_history = []
            st.session_state.corrected_text = "Your corrected text will appear here..." # Reset output
            st.rerun() # Rerun to instantly clear displayed history and output

        # Loop through history (already inserted newest first, so no need for reversed)
        for i, (original, corrected) in enumerate(st.session_state.grammar_history):
            # Showing only first 50 chars + "..." for brevity in expander title
            expander_title_original = original if len(original) <= 50 else original[:50] + "..."
            with st.expander(f"**{i+1}. Original:** {expander_title_original}"): # Numbering from 1 for newest
                st.markdown(f"**Original:**\n\n> {original}")
                st.markdown(f"**Corrected:**\n\n> {corrected}")
    else:
        st.info("No correction history yet. Enter some text and click 'Correct Grammar'.")

    st.markdown('</div>', unsafe_allow_html=True) # Close the glass-container div
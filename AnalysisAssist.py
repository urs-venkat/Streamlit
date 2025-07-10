import streamlit as st
import pandas as pd
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain_community.llms import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables (this should ideally be done once in main.py if you have one,
# but it's fine here too if this module is run independently or needs to ensure env vars are loaded)
load_dotenv()

def show():
    st.markdown("<h1 style='text-align: center;'>📊 AI Data Analysis Assistant</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Upload your CSV or Excel file and ask questions to get insights from your data.</p>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)

    # Initialize session state keys
    if "qa_history" not in st.session_state:
        st.session_state.qa_history = []
    # Ensure df is initialized even if no file is uploaded yet
    if "df" not in st.session_state:
        st.session_state.df = None

    # --- File Uploader ---
    with st.expander("📁 Upload Your Data File", expanded=True):
        uploaded_file = st.file_uploader("Choose a file", type=["csv", "xlsx"], label_visibility="collapsed")

        if uploaded_file is not None and st.session_state.get("uploaded_file_name") != uploaded_file.name:
            # Only process if a new file is uploaded or a different file is selected
            st.session_state.uploaded_file_name = uploaded_file.name # Store name to prevent reprocessing
            try:
                if uploaded_file.name.endswith(".csv"):
                    st.session_state.df = pd.read_csv(uploaded_file)
                elif uploaded_file.name.endswith(".xlsx"):
                    st.session_state.df = pd.read_excel(uploaded_file)
                st.success(f"Successfully loaded `{uploaded_file.name}`")
                st.session_state.qa_history = [] # Clear history on new file upload
            except Exception as e:
                st.error(f"Error loading file: {e}")
                st.session_state.df = None
        elif uploaded_file is None:
            # If user removes the file, clear the dataframe
            st.session_state.df = None
            st.session_state.uploaded_file_name = None


    df = st.session_state.get("df", None) # Get the current dataframe from session state

    if df is not None:
        col1, col2 = st.columns([1, 2])

        with col1:
            st.subheader("📝 Ask a Question")
            question = st.text_area("Enter your question here:", height=150, key="data_question")

            if st.button("🚀 Get Answer"):
                if question:
                    # --- START OF API KEY RETRIEVAL BLOCK ---
                    api_key = os.getenv("OPENAI_API_KEY") # Try getting from environment variable (from .env or system)
                    if not api_key:
                        try:
                            api_key = st.secrets["OPENAI_API_KEY"] # Then try Streamlit secrets (.streamlit/secrets.toml locally, or Streamlit Cloud secrets)
                        except KeyError:
                            st.error("OpenAI API key not found. Please set it in your `.env` file, `.streamlit/secrets.toml`, or Streamlit Cloud secrets.")
                            st.stop() # Stop execution if key isn't found
                            return # Redundant but good practice
                    # --- END OF API KEY RETRIEVAL BLOCK ---

                    def create_agent(df_param, openai_llm_instance): # Pass LLM instance to agent creator
                        return create_pandas_dataframe_agent(
                            openai_llm_instance, df_param, verbose=True, allow_dangerous_code=True
                        )

                    llm = OpenAI(openai_api_key=api_key) # Initialize LLM here once
                    agent = create_agent(df, llm) # Pass the dataframe and initialized LLM

                    with st.spinner("🧠 Analyzing your data..."):
                        try:
                            answer = agent.run(question)
                            st.session_state.qa_history.append((question, answer))
                        except Exception as e:
                            st.error(f"An error occurred during analysis: {e}")
                else:
                    st.warning("Please enter a question.")

        with col2:
            st.subheader("📋 Data Preview")
            if df is not None: # Ensure df exists before trying to display it
                st.dataframe(df.head(), use_container_width=True)
            else:
                st.info("Upload a file to see its preview.")

            st.subheader("💬 Answer")
            if st.session_state.qa_history:
                latest_q, latest_a = st.session_state.qa_history[-1]
                st.info(f"**Q:** {latest_q}")
                st.success(f"**A:** {latest_a}")
            else:
                st.info("Your answers will appear here.")

        # --- History Section ---
        st.markdown("<hr>", unsafe_allow_html=True)
        st.subheader("🕘 History")
        if st.button("🗑️ Clear History", key="clear_qa_history"): # Added a key to avoid duplicate key warning
            st.session_state.qa_history = []
            st.experimental_rerun() # Rerun to instantly clear displayed history

        # Display full history
        for i, (q, a) in enumerate(reversed(st.session_state.qa_history)):
            with st.expander(f"**{len(st.session_state.qa_history) - i}. Question:** {q}"): # Correct numbering for reversed
                st.markdown(f"**Answer:** {a}")
    else:
        st.info("Please upload a file to get started.")
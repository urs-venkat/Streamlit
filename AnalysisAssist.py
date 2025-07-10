


import streamlit as st
import pandas as pd
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain_community.llms import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

def show():
    st.markdown("<h1 style='text-align: center;'>📊 AI Data Analysis Assistant</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Upload your CSV or Excel file and ask questions to get insights from your data.</p>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)

    # Initialize session state keys
    if "qa_history" not in st.session_state:
        st.session_state.qa_history = []

    # --- File Uploader ---
    with st.expander("📁 Upload Your Data File", expanded=True):
        uploaded_file = st.file_uploader("Choose a file", type=["csv", "xlsx"], label_visibility="collapsed")

        if uploaded_file is not None:
            st.session_state["uploaded_file"] = uploaded_file
            try:
                if uploaded_file.name.endswith(".csv"):
                    st.session_state.df = pd.read_csv(uploaded_file)
                elif uploaded_file.name.endswith(".xlsx"):
                    st.session_state.df = pd.read_excel(uploaded_file)
                st.success(f"Successfully loaded `{uploaded_file.name}`")
            except Exception as e:
                st.error(f"Error loading file: {e}")
                st.session_state.df = None

    df = st.session_state.get("df", None)

    if df is not None:
        col1, col2 = st.columns([1, 2])

        with col1:
            st.subheader("📝 Ask a Question")
            question = st.text_area("Enter your question here:", height=150)
            
            if st.button("🚀 Get Answer"):
                if question:
                    def create_agent(df):
                        api_key = os.getenv("OPENAI_API_KEY")
                        if not api_key:
                            st.error("OpenAI API key is not set. Please check your .env file.")
                            return None
                        llm = OpenAI(openai_api_key=api_key)
                        return create_pandas_dataframe_agent(
                            llm, df, verbose=True, allow_dangerous_code=True
                        )

                    agent = create_agent(df)
                    if agent:
                        with st.spinner("🧠 Analyzing your data..."):
                            try:
                                answer = agent.run(question)
                                st.session_state.qa_history.append((question, answer))
                            except Exception as e:
                                st.error(f"An error occurred: {e}")
                else:
                    st.warning("Please enter a question.")

        with col2:
            st.subheader("📋 Data Preview")
            st.dataframe(df.head(), use_container_width=True)

            st.subheader("💬 Answer")
            if st.session_state.qa_history:
                latest_q, latest_a = st.session_state.qa_history[-1]
                st.info(f"**Q:** {latest_q}")
                st.success(f"**A:** {latest_a}")

        # --- History Section ---
        st.markdown("<hr>", unsafe_allow_html=True)
        st.subheader("🕘 History")
        if st.button("🗑️ Clear History"):
            st.session_state.qa_history = []
            st.experimental_rerun()

        for i, (q, a) in enumerate(reversed(st.session_state.qa_history)):
            with st.expander(f"**{i+1}. Question:** {q}"):
                st.markdown(f"**Answer:** {a}")
    else:
        st.info("Please upload a file to get started.")

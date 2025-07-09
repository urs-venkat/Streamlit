


import streamlit as st
import pandas as pd
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain_community.llms import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

def show():
    st.title("AI Data Analysis Assistant")

    # Initialize session state keys
    if "qa_history" not in st.session_state:
        st.session_state.qa_history = []

    # File uploader
    uploaded_file = st.file_uploader("Choose a file", type=["csv", "xlsx"])

    if uploaded_file is not None:
        st.session_state["uploaded_file"] = uploaded_file

        if uploaded_file.name.endswith(".csv"):
            st.session_state.df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith(".xlsx"):
            st.session_state.df = pd.read_excel(uploaded_file)

    # Restore previous dataframe if file is not uploaded again
    df = st.session_state.get("df", None)

    if df is not None:
        st.write("First 5 rows of the uploaded file:")
        st.write(df.head())

        # Clear History button
        if st.button("🗑 Clear History"):
            st.session_state.qa_history = []

        st.write("Ask a question about your data:")
        question = st.text_input("Enter your question")

        if question:
            def create_agent(df):
                api_key = os.getenv("OPENAI_API_KEY")
                llm = OpenAI(openai_api_key=api_key)
                return create_pandas_dataframe_agent(
                    llm, df, verbose=True, allow_dangerous_code=True
                )

            agent = create_agent(df)

            with st.spinner("Analyzing..."):
                answer = agent.run(question)

            # Store Q&A
            st.session_state.qa_history.append((question, answer))

            st.write("Answer:")
            st.write(answer)

        # Show history
        if st.session_state.qa_history:
            st.markdown("---")
            st.subheader("🕘 History")
            for i, (q, a) in enumerate(reversed(st.session_state.qa_history), 1):
                with st.expander(f"Q{i}: {q}"):
                    st.markdown(f"**Answer:** {a}")

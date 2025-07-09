


# import streamlit as st
# from streamlit_option_menu import option_menu

# import AnalysisAssist as analysis_ass
# import SentenceCorrector as sentencecor
# import PdfToDoc as PtD

# st.set_page_config(page_title="AI Assistant Suite", layout="wide")

# # Initialize session state
# if "username" not in st.session_state:
#     st.session_state.username = "Guest"
# if "qa_history" not in st.session_state:
#     st.session_state.qa_history = []
# if "grammar_history" not in st.session_state:
#     st.session_state.grammar_history = []

# # 🎨 Background + Glass Sidebar Styling
# def set_clean_background(image_url):
#     st.markdown(
#         f"""
#         <style>
#         .stApp {{
#             background-image: url("{image_url}");
#             background-size: cover;
#             background-position: center;
#             background-attachment: fixed;
#             color: white;
#         }}

#         section[data-testid="stSidebar"] {{
#             background-color: rgba(255, 255, 255, 0.05);
#             backdrop-filter: blur(15px);
#             -webkit-backdrop-filter: blur(15px);
#             border-right: 1px solid rgba(255, 255, 255, 0.1);
#             box-shadow: none;
#         }}

#         section[data-testid="stSidebar"] div[data-testid="stVerticalBlock"] > div:first-child {{
#             background-color: transparent !important;
#             box-shadow: none !important;
#         }}

#         section[data-testid="stSidebar"] * {{
#             color: white !important;
#         }}

#         .stTextInput input,
#         .stTextArea textarea,
#         .stButton > button {{
#             background-color: rgba(0, 0, 0, 0.5);
#             color: white;
#             border: 1px solid white;
#         }}
#         </style>
#         """,
#         unsafe_allow_html=True
#     )

# # 🧭 Sidebar Navigation
# with st.sidebar:
#     selected = option_menu(
#         menu_title="Main Menu",
#         options=["Home", "AI Analysis Assistant", "Grammar Corrector", "PDF to DOC"],
#         icons=["house", "bar-chart-line", "spellcheck", "file-earmark-arrow-down"],
#         menu_icon="cast",
#         default_index=0,
#         styles={
#             "nav-link-selected": {"background-color": "#FF4B4B", "color": "white"},
#         },
#     )

# # 🏠 Home Page
# if selected == "Home":
#     set_clean_background("https://www.microsoft.com/en-us/research/wp-content/uploads/2023/03/AI_Microsoft_Research_Header_1920x720.png")

#     st.markdown("<h1 style='text-align: center;'>🧠 AI Assistant Suite</h1>", unsafe_allow_html=True)
#     st.markdown("<h4 style='text-align: center;'>Boost your productivity with powerful AI tools</h4>", unsafe_allow_html=True)
#     st.markdown("<br>", unsafe_allow_html=True)

#     st.markdown("""
#     <ul style='font-size:18px;'>
#         <li>📊 <b>AI Data Analysis Assistant</b> – Ask questions about your uploaded data</li>
#         <li>✍️ <b>Grammar Corrector</b> – Instantly improve your writing</li>
#         <li>📄 <b>PDF to DOC Converter</b> – Quickly convert PDFs into Word documents</li>
#     </ul>
#     """, unsafe_allow_html=True)

#     st.text_input("👤 Enter your name:", key="username")
#     st.markdown(f"<p style='font-size:18px;'>Hello, <b>{st.session_state.username}</b>! Use the sidebar to explore tools.</p>", unsafe_allow_html=True)

# # 🧠 Tool Pages
# elif selected == "AI Analysis Assistant":
#     analysis_ass.show()

# elif selected == "Grammar Corrector":
#     sentencecor.show()

# elif selected == "PDF to DOC":
#     PtD.show()


import streamlit as st
from streamlit_option_menu import option_menu
from dotenv import load_dotenv
import os

import AnalysisAssist as analysis_ass
import SentenceCorrector as sentencecor
import PdfToDoc as PtD

# Load environment variables
load_dotenv()

st.set_page_config(page_title="AI Assistant Suite", layout="wide")

# Initialize session state
if "username" not in st.session_state:
    st.session_state.username = "Guest"
if "qa_history" not in st.session_state:
    st.session_state.qa_history = []
if "grammar_history" not in st.session_state:
    st.session_state.grammar_history = []

# 🎨 Background + Glass Sidebar Styling
def set_clean_background(image_url):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("{image_url}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            color: white;
        }}

        section[data-testid="stSidebar"] {{
            background-color: rgba(255, 255, 255, 0.12);
            backdrop-filter: blur(18px);
            -webkit-backdrop-filter: blur(18px);
            border-right: 1px solid rgba(255, 255, 255, 0.15);
            box-shadow: none;
        }}

        section[data-testid="stSidebar"] * {{
            color: white !important;
        }}

        .stTextInput input,
        .stTextArea textarea,
        .stButton > button {{
            background-color: rgba(0, 0, 0, 0.4);
            color: white;
            border: 1px solid white;
        }}

        ul {{
            font-size: 18px;
        }}

        .css-1dp5vir, .css-1d391kg {{
            background-color: transparent !important;
            box-shadow: none !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# 🧭 Sidebar Navigation
with st.sidebar:
    selected = option_menu(
        menu_title="Main Menu",
        options=["Home", "AI Analysis Assistant", "Grammar Corrector", "PDF to DOC"],
        icons=["house", "bar-chart-line", "spellcheck", "file-earmark-arrow-down"],
        menu_icon="cast",
        default_index=0,
        styles={
            "nav-link-selected": {"background-color": "#FF4B4B", "color": "white"},
        },
    )

# 🏠 Home Page
if selected == "Home":
    set_clean_background("https://www.microsoft.com/en-us/research/wp-content/uploads/2023/03/AI_Microsoft_Research_Header_1920x720.png")

    st.markdown("<h1 style='text-align: center;'>🧠 AI Assistant Suite</h1>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center;'>Boost your productivity with powerful AI tools</h4>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <ul>
        <li>📊 <b>AI Data Analysis Assistant</b> – Ask questions about your uploaded data</li>
        <li>✍️ <b>Grammar Corrector</b> – Instantly improve your writing</li>
        <li>📄 <b>PDF to DOC Converter</b> – Quickly convert PDFs into Word documents</li>
    </ul>
    """, unsafe_allow_html=True)

    st.text_input("👤 Enter your name:", key="username")
    st.markdown(f"<p style='font-size:18px;'>Hello, <b>{st.session_state.username}</b>! Use the sidebar to explore tools.</p>", unsafe_allow_html=True)

# 🧠 Tool Pages
elif selected == "AI Analysis Assistant":
    analysis_ass.show()

elif selected == "Grammar Corrector":
    sentencecor.show()

elif selected == "PDF to DOC":
    PtD.show()

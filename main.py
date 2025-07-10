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

# 🎨 Enhanced Background + Glass Sidebar Styling
def set_enhanced_background(image_url):
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
        
        .stApp {{
            background-image: url("{image_url}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            color: white;
            font-family: 'Poppins', sans-serif;
        }}

        section[data-testid="stSidebar"] {{
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border-right: 1px solid rgba(255, 255, 255, 0.15);
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.2);
        }}

        section[data-testid="stSidebar"] * {{
            color: white !important;
        }}

        /* Enhanced glass containers */
        .glass-container {{
            background: rgba(255, 255, 255, 0.08);
            backdrop-filter: blur(15px);
            -webkit-backdrop-filter: blur(15px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 20px;
            padding: 30px;
            margin: 20px 0;
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.15);
            transition: all 0.3s ease;
        }}

        .glass-container:hover {{
            transform: translateY(-5px);
            box-shadow: 0 12px 40px 0 rgba(31, 38, 135, 0.25);
            border-color: rgba(255, 255, 255, 0.3);
        }}

        /* Enhanced cards */
        .feature-card {{
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.05));
            backdrop-filter: blur(15px);
            -webkit-backdrop-filter: blur(15px);
            border: 1px solid rgba(255, 255, 255, 0.18);
            border-radius: 20px;
            padding: 30px;
            margin: 15px 0;
            text-align: center;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }}

        .feature-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
            transition: left 0.5s;
        }}

        .feature-card:hover::before {{
            left: 100%;
        }}

        .feature-card:hover {{
            transform: translateY(-10px) scale(1.02);
            box-shadow: 0 20px 50px rgba(255, 75, 75, 0.2);
            border-color: rgba(255, 75, 75, 0.5);
        }}

        .feature-card h3 {{
            color: #FF4B4B;
            font-weight: 600;
            margin-bottom: 15px;
            font-size: 1.4rem;
        }}

        .feature-card p {{
            color: rgba(255, 255, 255, 0.9);
            font-size: 1rem;
            line-height: 1.6;
        }}

        /* Enhanced input fields */
        .stTextInput input,
        .stTextArea textarea,
        .stSelectbox select {{
            background: rgba(255, 255, 255, 0.1) !important;
            color: white !important;
            border: 1px solid rgba(255, 255, 255, 0.3) !important;
            border-radius: 10px !important;
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
        }}

        .stTextInput input:focus,
        .stTextArea textarea:focus,
        .stSelectbox select:focus {{
            border-color: #FF4B4B !important;
            box-shadow: 0 0 20px rgba(255, 75, 75, 0.3) !important;
        }}

        /* Enhanced buttons */
        .stButton > button {{
            background: linear-gradient(135deg, #FF4B4B, #FF6B6B) !important;
            color: white !important;
            border: none !important;
            border-radius: 25px !important;
            padding: 15px 30px !important;
            font-weight: 600 !important;
            font-size: 1rem !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 15px rgba(255, 75, 75, 0.3) !important;
        }}

        .stButton > button:hover {{
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 25px rgba(255, 75, 75, 0.4) !important;
        }}

        /* Enhanced titles */
        .main-title {{
            font-size: 3.5rem;
            font-weight: 700;
            text-align: center;
            background: linear-gradient(135deg, #FF4B4B, #FF8E8E, #FFA8A8);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 10px;
            text-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
        }}

        .sub-title {{
            font-size: 1.3rem;
            font-weight: 400;
            text-align: center;
            color: rgba(255, 255, 255, 0.9);
            margin-bottom: 40px;
        }}

        /* Welcome section */
        .welcome-section {{
            background: linear-gradient(135deg, rgba(255, 75, 75, 0.15), rgba(255, 255, 255, 0.05));
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 20px;
            padding: 30px;
            margin: 30px 0;
            text-align: center;
        }}

        .welcome-name {{
            font-size: 1.4rem;
            font-weight: 600;
            color: #FF4B4B;
            margin-top: 15px;
        }}

        /* Feature list */
        .feature-list {{
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(15px);
            -webkit-backdrop-filter: blur(15px);
            border: 1px solid rgba(255, 255, 255, 0.15);
            border-radius: 15px;
            padding: 25px;
            margin: 20px 0;
        }}

        .feature-list ul {{
            list-style: none;
            padding: 0;
        }}

        .feature-list li {{
            padding: 15px 0;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            font-size: 1.1rem;
            transition: all 0.3s ease;
        }}

        .feature-list li:hover {{
            color: #FF4B4B;
            transform: translateX(10px);
        }}

        .feature-list li:last-child {{
            border-bottom: none;
        }}

        /* Animation keyframes */
        @keyframes fadeInUp {{
            from {{
                opacity: 0;
                transform: translateY(30px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}

        @keyframes slideInLeft {{
            from {{
                opacity: 0;
                transform: translateX(-30px);
            }}
            to {{
                opacity: 1;
                transform: translateX(0);
            }}
        }}

        .animate-fade-in {{
            animation: fadeInUp 0.6s ease-out;
        }}

        .animate-slide-in {{
            animation: slideInLeft 0.8s ease-out;
        }}

        /* Responsive design */
        @media (max-width: 768px) {{
            .main-title {{
                font-size: 2.5rem;
            }}
            
            .feature-card {{
                padding: 20px;
            }}
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# 🧭 Enhanced Sidebar Navigation
with st.sidebar:
    selected = option_menu(
        menu_title="✨ Main Menu",
        options=["Home", "AI Analysis Assistant", "Grammar Corrector", "PDF to DOC"],
        icons=["house-fill", "graph-up", "pencil-square", "file-earmark-arrow-down-fill"],
        menu_icon="stars",
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"},
            "icon": {"color": "white", "font-size": "18px"},
            "nav-link": {
                "font-size": "16px",
                "text-align": "left",
                "margin": "0px",
                "padding": "10px 15px",
                "border-radius": "10px",
                "color": "white",
                "background-color": "transparent",
                "transition": "all 0.3s ease"
            },
            "nav-link-selected": {
                "background": "linear-gradient(135deg, #FF4B4B, #FF6B6B)",
                "color": "white",
                "box-shadow": "0 4px 15px rgba(255, 75, 75, 0.3)"
            },
        },
    )

# 🏠 Enhanced Home Page
if selected == "Home":
    set_enhanced_background("https://www.microsoft.com/en-us/research/wp-content/uploads/2023/03/AI_Microsoft_Research_Header_1920x720.png")

    # Main title with animation
    st.markdown('<div class="animate-fade-in"><h1 class="main-title">🧠 AI Assistant Suite</h1></div>', unsafe_allow_html=True)
    st.markdown('<div class="animate-fade-in"><p class="sub-title">✨ Boost your productivity with powerful AI tools</p></div>', unsafe_allow_html=True)

    # Feature cards layout
    st.markdown('<div class="animate-slide-in">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3>📊 AI Data Analysis</h3>
            <p>Transform your data into actionable insights with intelligent analysis and natural language queries.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3>✍️ Grammar Corrector</h3>
            <p>Perfect your writing with AI-powered grammar correction and style enhancement.</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="feature-card">
            <h3>📄 PDF to DOC</h3>
            <p>Seamlessly convert PDF documents to editable Word format with precision.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Enhanced feature list
    st.markdown("""
    <div class="feature-list animate-fade-in">
        <ul>
            <li>🚀 <b>Lightning Fast Processing</b> – Get results in seconds</li>
            <li>🎯 <b>High Accuracy</b> – AI-powered precision for all tasks</li>
            <li>🔒 <b>Secure & Private</b> – Your data stays protected</li>
            <li>📱 <b>Responsive Design</b> – Works on all devices</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    # Welcome section
    st.markdown("""
    <div class="welcome-section animate-fade-in">
        <h3>👋 Welcome to Your AI Workspace</h3>
        <p>Enter your name below to personalize your experience</p>
    </div>
    """, unsafe_allow_html=True)

    # Enhanced name input
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.text_input("", placeholder="Enter your name here...", key="username", label_visibility="collapsed")
    
    st.markdown(f'<div class="welcome-name animate-fade-in">Hello, <b>{st.session_state.username}</b>! 🎉<br>Use the sidebar to explore our amazing tools.</div>', unsafe_allow_html=True)

# 🧠 Tool Pages
elif selected == "AI Analysis Assistant":
    set_enhanced_background("https://www.microsoft.com/en-us/research/wp-content/uploads/2023/03/AI_Microsoft_Research_Header_1920x720.png")
    analysis_ass.show()

elif selected == "Grammar Corrector":
    set_enhanced_background("https://www.microsoft.com/en-us/research/wp-content/uploads/2023/03/AI_Microsoft_Research_Header_1920x720.png")
    sentencecor.show()

elif selected == "PDF to DOC":
    set_enhanced_background("https://www.microsoft.com/en-us/research/wp-content/uploads/2023/03/AI_Microsoft_Research_Header_1920x720.png")
    PtD.show()
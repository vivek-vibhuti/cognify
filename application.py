import os
import streamlit as st
from dotenv import load_dotenv
from src.utils.helpers import *
from src.generator.generator_generatior import QuestionGenerator
load_dotenv()


def main():
    st.set_page_config(page_title="Cognify" , page_icon="🧠", layout="centered")

    # Injecting custom CSS for a stunning UI
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    /* Background Gradient styling */
    .stApp {
        background: radial-gradient(circle at 90% 10%, rgba(121, 40, 202, 0.15), transparent 45%),
                    radial-gradient(circle at 10% 90%, rgba(0, 112, 243, 0.15), transparent 45%),
                    #0e1117;
    }
    
    /* App header & title gradient */
    .cognify-title {
        background: linear-gradient(135deg, #0070f3 0%, #7928ca 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3.5rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 2px;
        letter-spacing: -1px;
    }
    
    .cognify-subtitle {
        text-align: center;
        color: #9a9a9a;
        font-size: 1.15rem;
        margin-bottom: 2rem;
        font-weight: 300;
    }
    
    /* Custom divider line */
    .divider {
        height: 2px;
        background: linear-gradient(90deg, transparent, rgba(121, 40, 202, 0.3), transparent);
        margin: 25px 0;
    }
    
    /* Sidebar styled title */
    .sidebar-title {
        color: #ffffff;
        font-size: 1.5rem;
        font-weight: 600;
        text-align: center;
        margin-bottom: 20px;
    }
    
    /* Styled container cards for quiz questions */
    .question-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.07);
        border-radius: 12px;
        padding: 22px;
        margin-top: 15px;
        margin-bottom: 10px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.2);
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
    }
    
    /* Result summary card */
    .score-banner {
        background: linear-gradient(135deg, rgba(0, 112, 243, 0.1) 0%, rgba(121, 40, 202, 0.1) 100%);
        border: 1px solid rgba(121, 40, 202, 0.2);
        border-radius: 12px;
        padding: 25px;
        text-align: center;
        margin-bottom: 30px;
    }
    
    /* Success card styled */
    .correct-ans-card {
        border-left: 5px solid #10b981;
        background-color: rgba(16, 185, 129, 0.05);
        padding: 15px 20px;
        border-radius: 8px;
        margin-bottom: 15px;
        border-top: 1px solid rgba(16, 185, 129, 0.1);
        border-right: 1px solid rgba(16, 185, 129, 0.1);
        border-bottom: 1px solid rgba(16, 185, 129, 0.1);
    }
    
    /* Error card styled */
    .incorrect-ans-card {
        border-left: 5px solid #ef4444;
        background-color: rgba(239, 68, 68, 0.05);
        padding: 15px 20px;
        border-radius: 8px;
        margin-bottom: 15px;
        border-top: 1px solid rgba(239, 68, 68, 0.1);
        border-right: 1px solid rgba(239, 68, 68, 0.1);
        border-bottom: 1px solid rgba(239, 68, 68, 0.1);
    }
    
    /* Streamlit button styling overrides */
    div.stButton > button {
        background: linear-gradient(135deg, #0070f3 0%, #7928ca 100%) !important;
        color: white !important;
        border: none !important;
        padding: 10px 24px !important;
        border-radius: 8px !important;
        font-size: 16px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
        box-shadow: 0 4px 15px rgba(121, 40, 202, 0.3) !important;
    }
    
    div.stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(121, 40, 202, 0.5) !important;
    }
    
    div.stButton > button:active {
        transform: translateY(1px) !important;
    }
    
    /* Sidebar element styling */
    [data-testid="stSidebar"] {
        background-color: #0b0d12 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.08);
    }
    
    /* Option selections & text input fields */
    .stTextInput>div>div>input {
        background-color: rgba(255, 255, 255, 0.02) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        color: #ffffff !important;
        border-radius: 8px !important;
        padding: 10px !important;
    }
    
    .stSelectbox>div>div>div {
        background-color: rgba(255, 255, 255, 0.02) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 8px !important;
    }
    </style>
    """, unsafe_allow_html=True)

    if 'quiz_manager'not in st.session_state:
        st.session_state.quiz_manager = QuizManager()

    if 'quiz_generated'not in st.session_state:
        st.session_state.quiz_generated = False

    if 'quiz_submitted'not in st.session_state:
        st.session_state.quiz_submitted = False

    if 'rerun_trigger'not in st.session_state:
        st.session_state.rerun_trigger = False

    # App Main Header
    st.markdown("<div class='cognify-title'>Cognify</div>", unsafe_allow_html=True)
    st.markdown("<div class='cognify-subtitle'>Empower your mind with AI-generated interactive quizzes</div>", unsafe_allow_html=True)
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # Sidebar Logo and Title
    if os.path.exists("logo.jpg"):
        st.sidebar.image("logo.jpg", use_container_width=True)
    st.sidebar.markdown("<div class='sidebar-title'>Quiz Settings</div>", unsafe_allow_html=True)

    question_type = st.sidebar.selectbox(
        "Select Question Type" ,
        ["Multiple Choice" , "Fill in the Blank"],
        index=0
    )

    topic = st.sidebar.text_input("Enter Topic" , placeholder="Indian History, geography")

    difficulty = st.sidebar.selectbox(
        "Difficulty Level",
        ["Easy" , "Medium" , "Hard"],
        index=1
    )

    num_questions=st.sidebar.number_input(
        "Number of Questions",
        min_value=1,  max_value=10 , value=5
    )

    if st.sidebar.button("Generate Quiz"):
        st.session_state.quiz_submitted = False

        generator = QuestionGenerator()
        succces = st.session_state.quiz_manager.generate_questions(
            generator,
            topic,question_type,difficulty,num_questions
        )

        st.session_state.quiz_generated= succces
        rerun()

    if st.session_state.quiz_generated and st.session_state.quiz_manager.questions:
        st.markdown("<h2 style='color: #ffffff; margin-top: 20px;'>Take the Quiz</h2>", unsafe_allow_html=True)
        st.session_state.quiz_manager.attempt_quiz()

        if st.button("Submit Quiz"):
            st.session_state.quiz_manager.evaluate_quiz()
            st.session_state.quiz_submitted = True
            rerun()

    if st.session_state.quiz_submitted:
        st.markdown("<h2 style='text-align: center; color: #ffffff; margin-top: 30px;'>Quiz Results</h2>", unsafe_allow_html=True)
        results_df = st.session_state.quiz_manager.generate_result_dataframe()

        if not results_df.empty:
            correct_count = results_df["is_correct"].sum()
            total_questions = len(results_df)
            score_percentage = int((correct_count/total_questions)*100)
            
            st.markdown(f"""
            <div class='score-banner'>
                <span style='font-size: 1.2rem; color: #a8a8a8; text-transform: uppercase;'>Your Score</span>
                <h1 style='font-size: 3.5rem; margin: 5px 0; color: #ffffff;'>{score_percentage}%</h1>
                <span style='font-size: 1.1rem; color: #a855f7;'>{correct_count} out of {total_questions} correct</span>
            </div>
            """, unsafe_allow_html=True)

            for _, result in results_df.iterrows():
                question_num = result['question_number']
                if result['is_correct']:
                    st.markdown(f"""
                    <div class='correct-ans-card'>
                        <strong style='color: #10b981; font-size: 1.1rem;'>✅ Question {question_num}</strong>
                        <p style='margin: 8px 0 0 0; color: #e5e7eb;'>{result['question']}</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class='incorrect-ans-card'>
                        <strong style='color: #ef4444; font-size: 1.1rem;'>❌ Question {question_num}</strong>
                        <p style='margin: 8px 0 10px 0; color: #e5e7eb;'>{result['question']}</p>
                        <div style='background: rgba(255, 255, 255, 0.02); padding: 12px; border-radius: 6px; border: 1px solid rgba(255, 255, 255, 0.05);'>
                            <span style='color: #9ca3af;'>Your answer:</span> <span style='color: #fca5a5; font-weight: 500;'>{result['user_answer'] if result['user_answer'] else "<i>No response</i>"}</span><br>
                            <span style='color: #9ca3af;'>Correct answer:</span> <span style='color: #86efac; font-weight: 500;'>{result['correct_answer']}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

            if st.button("Save Results"):
                saved_file = st.session_state.quiz_manager.save_to_csv()
                if saved_file:
                    with open(saved_file,'rb') as f:
                        st.download_button(
                            label="Download Results CSV",
                            data=f.read(),
                            file_name=os.path.basename(saved_file),
                            mime='text/csv'
                        )
                else:
                    st.warning("No results available")

if __name__=="__main__":
    main()
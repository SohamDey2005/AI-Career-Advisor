import streamlit as st
import google.generativeai as genai
import os

# ------------------------------
# Configuration of Gemini API
# ------------------------------

if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel("gemini-2.5-pro")
else:
    model = None

# ------------------------------
# Helper Functions
# ------------------------------

def get_ai_response(prompt):
    """Call Gemini API if key exists, else return dummy response."""
    if model:
        try:
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"⚠️ Error from AI: {str(e)}"
    else:
        # Dummy fallback if no API key
        return "AI service unavailable. Please set GOOGLE_API_KEY."

def recommend_careers(skills, interests, education):
    prompt = f"""
    You are a career advisor. Based on the following profile:
    - Skills: {skills}
    - Interests: {interests}
    - Education Level: {education}

    Suggest 3 suitable career paths (like Data Scientist, Product Manager, UX Designer).
    For each career:
    - Provide a short description
    - List key required skills
    - Compare against the user's skills (mark missing skills as gaps)
    - Suggest learning resources (courses, certifications, or books)
    """
    return get_ai_response(prompt)

def chat_with_ai(user_input):
    prompt = f"""
    You are a helpful career counseling assistant.
    Answer this career-related question clearly and empathetically:

    {user_input}
    """
    return get_ai_response(prompt)

# ------------------------------
# Streamlit UI
# ------------------------------

st.set_page_config(page_title="AI Career Advisor", page_icon="🎓", layout="wide")

st.title("🎓 AI-Powered Career & Skills Advisor")
st.write("Get personalized career guidance, skill gap analysis, and learning resources.")

st.sidebar.header("User Profile")
skills = st.sidebar.text_area("Enter your skills (comma separated):", "Python, Communication")
interests = st.sidebar.text_area("Enter your interests:", "Data Science, AI, Problem Solving")
education = st.sidebar.selectbox("Current Education Level:", ["High School", "Undergraduate", "Graduate", "Postgraduate", "Other"])

if st.sidebar.button("Generate Career Path Recommendations"):
    with st.spinner("Analyzing your profile and preparing recommendations..."):
        recommendations = recommend_careers(skills, interests, education)
    st.subheader("📌 Career Recommendations & Skill Gap Analysis")
    st.write(recommendations)

st.subheader("💬 Career Chatbot")
st.write("Ask me anything about careers, skills, or learning resources.")

user_question = st.text_input("Your Question:", "")
if st.button("Ask Advisor"):
    if user_question.strip() != "":
        with st.spinner("Thinking..."):
            response = chat_with_ai(user_question)
        st.success("Answer:")
        st.write(response)
    else:
        st.warning("Please enter a question.")

st.markdown("---")
st.caption("⚡ Powered by **Google Gemini AI** + **Streamlit**")

st.caption("👨‍💻 Developed by **Soham Dey**")

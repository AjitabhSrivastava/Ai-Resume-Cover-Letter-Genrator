import streamlit as st
import ollama
from utils import generate_resume_pdf, generate_cover_letter_pdf

st.set_page_config(page_title="THE AI RESUME AND COVEr LETTER", page_icon="📝")
st.title("📝✨ AI POWERED RESUME AND COVER LETTER ")



with st.form("resume_form"):
    st.header("👤 Enter your  Personal Info")
    name = st.text_input("Full Name")
    phone = st.text_input("Phone Number")
    email = st.text_input("Email")
    linkedin = st.text_input("LinkedIn URL (optional)")

    st.header("🎓 Enter Your Education")
    col1, col2 = st.columns(2)
    with col1:
        college = st.text_input("College Name & Course")
        cgpa = st.text_input("CGPA / Percentage")
        branch = st.selectbox("Branch", ["CSE", "IT", "ECE", "EEE", "Mechanical", "Civil", "Other"])
    with col2:
        year_of_completion = st.selectbox("Graduation Year", ["2024", "2025", "2026", "2027", "2028"])
        school_12 = st.text_input("12th School Name")
        percent_12 = st.text_input("12th Percentage")
        school_10 = st.text_input("10th School Name")
        percent_10 = st.text_input("10th Percentage")

    st.header(" Skills & Projects")
    skills = st.text_area("Technical Skills (comma-separated)")
    soft_skills = st.text_area("Soft Skills (comma-separated)")
    projects = st.text_area("Project Titles / Descriptions (comma-separated)")

    st.header(" Extra-Curricular")
    hobbies = st.text_area("Extra-Curricular Activities (comma-separated)")

    resume_style = st.selectbox("🎨 Resume style / target:", ["Standard", "MNC", "Startup", "Government", "Academic"])

    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        generate_resume = st.form_submit_button("Generate Resume")
    with col_btn2:
        generate_cover = st.form_submit_button("✉ Generate Cover Letter")

if generate_resume:
    st.info("✨ AI is writing your professional resume, wait a moment...")
    model = "llama3"

    prompt = f"""
You are a professional resume writer. For {name}, targeting {resume_style}:
Write these 6 sections, each starting with ###SECTION###:
###SECTION###
Profile Summary: first-person, start with 'Myself {name}', include phone: {phone}, highlight key skills: {skills}. Make it short (3–4 lines), catchy & confident.
###SECTION###
Education: bullets:
• {college} (B.Tech {branch})
• CGPA: {cgpa}
• Year of completion: {year_of_completion}
• Achieved {percent_12}% from {school_12} in 12th
• Secured {percent_10}% from {school_10} in 10th
###SECTION###
Academic Projects: from {projects}. Write short catchy 1-line title + 1–2 bullets: tools & impact, for each. Max 2–3 projects.
###SECTION###
Technical Skills: bullet list from: {skills}.
###SECTION###
Soft Skills: bullet list from: {soft_skills}.
###SECTION###
Extra-Curricular Activities: creative 2–3 bullets from: {hobbies}.

⚠ No headings inside content, only text.
⚠ Return exactly:
###SECTION###<Profile>
###SECTION###<Education>
###SECTION###<Projects>
###SECTION###<Tech Skills>
###SECTION###<Soft Skills>
###SECTION###<Extras>
"""

    response = ollama.chat(model=model, messages=[{'role':'user','content':prompt}])['message']['content']
    sections = response.split('###SECTION###')
    profile = sections[1].strip() if len(sections) > 1 else ""
    education = sections[2].strip() if len(sections) > 2 else ""
    projects_ai = sections[3].strip() if len(sections) > 3 else ""
    skills_ai = sections[4].strip() if len(sections) > 4 else ""
    soft_skills_ai = sections[5].strip() if len(sections) > 5 else ""
    extras_ai = sections[6].strip() if len(sections) > 6 else ""

    pdf = generate_resume_pdf(name, email, phone, linkedin, profile, education, projects_ai, skills_ai, soft_skills_ai, extras_ai)
    with open(pdf, "rb") as f:
        st.download_button("📄 Download Resume PDF", data=f, file_name="resume.pdf", mime="application/pdf")
    st.success("🪁 Resume ready!")

if generate_cover:
    st.info("⚡⚡✨✨AI is writing your cover letter...")
    cover_prompt = f"""
Write a detailed (5–6 paragraphs) first-person cover letter for {name}.
Mention phone: {phone}, email: {email}, linkedin: {linkedin}.
Include college: {college}, branch: {branch}, CGPA: {cgpa}, graduation: {year_of_completion}, projects: {projects}, technical skills: {skills}.
Make it professional, confident & creative.
""" 
    model = "llama3"  # or "llama2", "gemma", etc. depending on what you have installed in Ollama

    cover_letter = ollama.chat(model=model, messages=[{'role':'user','content':cover_prompt}])['message']['content'].strip()
    cover_pdf = generate_cover_letter_pdf(name, email, phone, linkedin, cover_letter)
    with open(cover_pdf, "rb") as f:
        st.download_button(" 💼💼Download Cover Letter PDF", data=f, file_name="cover_letter.pdf", mime="application/pdf")
    st.success("😃😃 Cover letter ready!😃😃")
import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
import tempfile
from dotenv import load_dotenv
from utils.helpers import validate_pdf, truncate_text
from components.ui import render_sidebar, render_header, render_results

load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")

# ── PAGE CONFIG ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CV AdvIser",
    layout="centered",
    page_icon="📄",
    initial_sidebar_state="expanded"
)

# ── SIDEBAR & HEADER ───────────────────────────────────────────────────────────
render_sidebar()
render_header()

# ── MODEL ─────────────────────────────────────────────────────────────────────
if not google_api_key:
    st.error("GOOGLE_API_KEY not found. Please set it in your .env file.")
    st.stop()

model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    temperature=0.7,
    max_output_tokens=2048,
    google_api_key=google_api_key
)
parser = StrOutputParser()

# ── PROMPTS ───────────────────────────────────────────────────────────────────
cv_eval_prompt = PromptTemplate(
    template="""You are an experienced interviewer and hiring manager recruiting for the role of **{role}**.
Given the following CV, perform a detailed evaluation covering:

1. **CV Assessment** - Analyze the CV with respect to the {role} position. Evaluate relevant skills,
   experience level, strengths, weaknesses, and overall impression.
2. **Suggestions for Improvement** - Recommend specific, actionable changes to improve the CV's
   relevance, clarity, and impact for a {role} role. Include keyword optimization suggestions.
3. **Customized Interview Questions** - Generate 8–10 insightful, role-specific interview questions
   tailored to the CV content.
4. **Practice Advice for Candidate** - Suggest technical and non-technical topics the candidate
   should prepare for, based on observed gaps or emphasis in the CV.

CV:
{cv}
""",
    input_variables=["cv", "role"]
)

skill_extraction_prompt = PromptTemplate(
    template="""Extract all relevant technical and soft skills from the following text.
Return them as a **comma-separated list** without extra commentary.

Text:
{content}
""",
    input_variables=["content"]
)

skill_gap_prompt = PromptTemplate(
    template="""Compare the following skills:

**CV Skills:** {cv_skills}
**Job Description Skills:** {jd_skills}

Identify:
1. Skills in JD missing from CV (skill gaps to address).
2. Skills in CV not required in JD (may de-prioritize).
3. Transferable/related skills in CV that match JD requirements.

Return in **Markdown** format with clear headings.
""",
    input_variables=["cv_skills", "jd_skills"]
)

scoring_prompt = PromptTemplate(
    template="""You are a professional recruiter. Score the following CV for the role of **{role}**:

1. **Relevance to Role** — score /10 + star rating /5
2. **Clarity** — score /10 + star rating /5
3. **Skill Match** — score /10 + star rating /5
4. **Readability** — score /10 + star rating /5
5. **Overall Score** — /10
6. One-sentence summary of candidate fit.

CV Content:
{cv}
""",
    input_variables=["cv", "role"]
)

grammar_prompt = PromptTemplate(
    template="""You are an expert proofreader and career coach.
Review the CV text for grammar mistakes, awkward phrasing, formatting issues, and layout inconsistencies.

Provide feedback in:
1. **Grammar & Spelling Errors**
2. **Sentence Clarity**
3. **Formatting Suggestions**

CV Content:
{cv}
""",
    input_variables=["cv"]
)

# ── CHAINS ────────────────────────────────────────────────────────────────────
cv_eval_chain       = cv_eval_prompt       | model | parser
skill_extract_chain = skill_extraction_prompt | model | parser
skill_gap_chain     = skill_gap_prompt     | model | parser
scoring_chain       = scoring_prompt       | model | parser
grammar_chain       = grammar_prompt       | model | parser

# ── USER INPUTS ───────────────────────────────────────────────────────────────
job_role = st.selectbox(
    "Select the job role you are preparing this CV for",
    ["Software Engineer", "Data Scientist", "AI Engineer", "ML Engineer",
     "Backend Developer", "Frontend Developer", "DevOps Engineer", "Other"],
    index=0
)

if job_role == "Other":
    job_role = st.text_input(
        "Specify Job Role",
        placeholder="e.g. Backend Developer, Product Manager"
    )

if not job_role or not job_role.strip():
    st.warning("Please enter a job role to proceed.")
    st.stop()

jd_text = ""
if st.checkbox("📎 Add Job Description for Skill Gap Analysis"):
    jd_text = st.text_area(
        "Paste Job Description text here",
        height=200,
        placeholder="Paste the full job description here..."
    )

uploaded_cv = st.file_uploader("Upload your CV (PDF only)", type=["pdf"])

# ── PROCESSING ────────────────────────────────────────────────────────────────
if uploaded_cv and job_role:
    # Validate file
    is_valid, msg = validate_pdf(uploaded_cv)
    if not is_valid:
        st.error(msg)
        st.stop()

    with st.spinner("Analysing your CV... Please wait."):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(uploaded_cv.read())
            tmp_path = tmp.name

        try:
            # Load & chunk PDF
            loader    = PyPDFLoader(tmp_path)
            documents = loader.load()
            splitter  = RecursiveCharacterTextSplitter(
                chunk_size=1000, chunk_overlap=100
            )
            merged_cv = "\n".join(
                c.page_content for c in splitter.split_documents(documents)
            )
            merged_cv = truncate_text(merged_cv, max_chars=6000)

            # Run all chains
            eval_result     = cv_eval_chain.invoke({"cv": merged_cv, "role": job_role})
            scoring_result  = scoring_chain.invoke({"cv": merged_cv, "role": job_role})
            grammar_result  = grammar_chain.invoke({"cv": merged_cv})

            skill_gap_result = ""
            if jd_text.strip():
                cv_skills        = skill_extract_chain.invoke({"content": merged_cv})
                jd_skills        = skill_extract_chain.invoke({"content": jd_text})
                skill_gap_result = skill_gap_chain.invoke(
                    {"cv_skills": cv_skills, "jd_skills": jd_skills}
                )

            # Render results
            render_results(
                eval_result, scoring_result, grammar_result,
                skill_gap_result, jd_text
            )

        finally:
            os.remove(tmp_path)

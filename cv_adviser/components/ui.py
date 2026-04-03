"""
components/ui.py
All Streamlit UI rendering functions for CV Adviser.
"""
import streamlit as st
from utils.helpers import build_download_bundle


def render_sidebar():
    """Render the left sidebar with logo, description, and links."""
    with st.sidebar:
        # Logo
        try:
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.image("assets/logo.png", width=100)
        except Exception:
            st.markdown("### 📄 CV AdvIser")

        st.markdown(
            """
            <p style='text-align: justify; font-size: 0.9em;'>
            <strong>CV AdvIser</strong> is an AI-powered CV analysis platform that helps
            students and job seekers evaluate resumes, identify skill gaps, get grammar
            feedback and prepare for future applications.
            </p>
            """,
            unsafe_allow_html=True
        )
        st.markdown("---")

        col1, col2, col3 = st.columns([1,2,1])

st.markdown(
    """
    <p style='text-align: center; font-size: 0.9em;'>
        <b>A GROUP PROJECT BY</b><br><br>

        Arnab Mukherjee,      25MA60R05 <br>
        Sagar Kumar Khairwar, 25MA60R12 <br>
        Pabitra Mondal,       25MA60R13 <br>
        Sanchita Ghosh,       25MA60R33 <br><br>

        <b>AI/ML (MA60274), Semester-II</b><br>
        M.Tech. in CSDP, Dept. of Mathematics<br>
        Indian Institute of Technology Kharagpur
    </p>
    """,
    unsafe_allow_html=True
)

with col2:
    st.image("iitkgplogo1.png", width=120)        

        

        st.markdown("---")
        st.markdown("#### ℹ️ How to Use")
        st.markdown(
            """
            1. Select your **target job role**
            2. **Upload** your CV as a PDF
            3. Wait for the analysis to complete
            4. **Download** your reports
            """
        )
       


def render_header():
    """Render the main page header with logo and title."""
    try:
        col1, col2, col3 = st.columns([20, 10, 20])
        with col2:
            st.image("assets/logo.png", width=150)
    except Exception:
        pass

    st.markdown(
        "<h2 style='text-align: center; color: #2E5090;'>CV Adviser</h2>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<h4 style='text-align: center; color: #555;'>"
        "Evaluation · Skill Analysis · Scoring · Grammar Review"
        "</h4>",
        unsafe_allow_html=True
    )
    st.markdown("<hr>", unsafe_allow_html=True)


def render_results(
    eval_result: str,
    scoring_result: str,
    grammar_result: str,
    skill_gap_result: str,
    jd_text: str,
    role: str = ""
):
    """Render all analysis results in organized tabs with download buttons."""
    st.success("✅ CV analysis complete!")

    # ── TABS ──────────────────────────────────────────────────────────────────
    tabs = ["📊 Scoring", "📋 Evaluation", "✏️ Grammar"]
    if jd_text.strip() and skill_gap_result:
        tabs.append("🛠 Skill Gap")

    tab_objects = st.tabs(tabs)

    with tab_objects[0]:
        st.markdown("### 📊 CV Scoring & Rating")
        st.markdown(scoring_result)

    with tab_objects[1]:
        st.markdown("### 📋 CV Evaluation Summary")
        st.markdown(eval_result)

    with tab_objects[2]:
        st.markdown("### ✏️ Grammar & Formatting Feedback")
        st.markdown(grammar_result)

    if len(tabs) == 4:
        with tab_objects[3]:
            st.markdown("### 🛠 Skill Gap Analysis")
            st.markdown(skill_gap_result)

    # ── DOWNLOADS ─────────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### 📥 Download Reports")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.download_button(
            "📋 Evaluation Report",
            eval_result,
            "CV_Evaluation.md",
            "text/markdown",
            use_container_width=True
        )
    with col2:
        st.download_button(
            "📊 Scoring Report",
            scoring_result,
            "CV_Scoring.md",
            "text/markdown",
            use_container_width=True
        )
    with col3:
        st.download_button(
            "✏️ Grammar Report",
            grammar_result,
            "Grammar_Feedback.md",
            "text/markdown",
            use_container_width=True
        )

    if jd_text.strip() and skill_gap_result:
        col4, col5 = st.columns([1, 1])
        with col4:
            st.download_button(
                "🛠 Skill Gap Report",
                skill_gap_result,
                "Skill_Gap_Analysis.md",
                "text/markdown",
                use_container_width=True
            )
        with col5:
            full_report = build_download_bundle(
                eval_result, scoring_result, grammar_result, skill_gap_result, role
            )
            st.download_button(
                "📦 Full Bundle (All Reports)",
                full_report,
                "CV_Master_Full_Report.md",
                "text/markdown",
                use_container_width=True
            )
    else:
        full_report = build_download_bundle(
            eval_result, scoring_result, grammar_result, "", role
        )
        st.download_button(
            "📦 Download Full Report",
            full_report,
            "CV_Master_Full_Report.md",
            "text/markdown",
            use_container_width=True
        )

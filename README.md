# 📄 CV Adviser

> AI-powered CV analysis platform for students and job seekers.

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35%2B-red)](https://streamlit.io)
[![LangChain](https://img.shields.io/badge/LangChain-0.2%2B-green)](https://langchain.com)
[![Gemini](https://img.shields.io/badge/Gemini-2.5--flash--lite-orange)](https://ai.google.dev)
[![License](https://img.shields.io/badge/License-MIT-lightgrey)](LICENSE)

---

## 🎯 What It Does

CV Adviser takes your uploaded PDF resume and generates:

| Feature | Description |
|---|---|
| **CV Evaluation** | Detailed assessment of skills, experience, strengths & weaknesses vs target role |
| **CV Scoring** | Score out of 10 across Relevance, Clarity, Skill Match, Readability |
| **Grammar Review** | Grammar errors, awkward phrasing, and formatting suggestions |
| **Skill Gap Analysis** | Compares your CV skills against a pasted Job Description |
| **Download Reports** | All results downloadable as Markdown files |

---

## 🏗️ Project Structure

```
cv-adviser/
│
├── app.py                  ← Main Streamlit application
├── requirements.txt        ← Python dependencies
├── .env.example            ← Template for environment variables
├── .gitignore
├── README.md
│
├── assets/
│   └── logo.png            ← App logo
│
├── components/
│   ├── __init__.py
│   └── ui.py               ← All Streamlit UI rendering functions
│
├── utils/
│   ├── __init__.py
│   └── helpers.py          ← PDF validation, text utils, report builder
│
├── tests/
│   ├── __init__.py
│   ├── test_helpers.py     ← Unit tests for utility functions
│   └── test_prompts.py     ← Prompt quality tests
│
└── docs/
    ├── architecture.md     ← System design & flow diagram
    └── api_reference.md    ← Function/module reference
```

---

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/pabitramondalkgpian25/cv-adviser.git
cd cv-adviser
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up API Key
```bash
cp .env.example .env
# Edit .env and add your Gemini API key
```
Get your free API key at: https://aistudio.google.com/app/apikey

### 5. Run the App
```bash
streamlit run app.py
```
The app opens at `http://localhost:8501`

---

## 🔑 Environment Variables

| Variable | Description | Required |
|---|---|---|
| `GOOGLE_API_KEY` | Google Gemini API key | ✅ Yes |

---

## 🧱 Tech Stack

| Layer | Technology |
|---|---|
| **Frontend** | Streamlit |
| **LLM** | Google Gemini 2.5 Flash Lite |
| **Orchestration** | LangChain (LCEL chains) |
| **PDF Parsing** | PyPDFLoader (LangChain Community) |
| **Text Splitting** | RecursiveCharacterTextSplitter |
| **Config** | python-dotenv |

---

## 🔄 Application Flow

```
User uploads PDF
      ↓
PyPDFLoader extracts text
      ↓
RecursiveCharacterTextSplitter chunks text
      ↓
Text truncated to 6000 chars (token safety)
      ↓
┌─────────────────────────────────┐
│  Parallel LangChain LCEL Chains │
│  ├── cv_eval_chain              │
│  ├── scoring_chain              │
│  ├── grammar_chain              │
│  └── skill_gap_chain (if JD)    │
└─────────────────────────────────┘
      ↓
Results rendered in Streamlit tabs
      ↓
User downloads Markdown reports
```

---

## 📊 Features in Detail

### CV Evaluation
Assesses the resume against the selected job role across:
- Relevance of skills and experience
- Identified strengths and weaknesses
- Specific improvement suggestions with keyword optimization
- 8–10 customised interview questions
- Study/preparation advice based on CV gaps

### CV Scoring
Scores on four dimensions (each /10 with star rating):
- Relevance to Role
- Clarity
- Skill Match
- Readability
- Overall Score with a one-sentence summary

### Grammar & Formatting Review
- Grammar and spelling errors highlighted
- Sentence clarity improvements
- Formatting and layout consistency suggestions

### Skill Gap Analysis *(requires Job Description)*
- Skills in JD missing from CV
- Skills in CV not required for the role
- Transferable skills mapping

---

## 🧪 Running Tests

```bash
pip install pytest
pytest tests/ -v
```

---

## 📸 Screenshots

> Add screenshots here after deployment.

---

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Pabitra Mondal**
M.Tech CSDP, Batch 2025–27, IIT Kharagpur

- LinkedIn: [linkedin.com/in/pabitra-mondal-aa6151176](https://www.linkedin.com/in/pabitra-mondal-aa6151176)
- GitHub: [github.com/pabitramondalkgpian25](https://github.com/pabitramondalkgpian25)

---

## ⭐ Acknowledgements

- [LangChain](https://langchain.com) for the LLM orchestration framework
- [Google AI Studio](https://aistudio.google.com) for the Gemini API
- [Streamlit](https://streamlit.io) for the rapid UI framework
- Original project inspired by [Tanmoy Giri](https://github.com/iamtgiri/cv-master)

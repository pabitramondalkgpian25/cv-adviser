# CV Adviser — Architecture & Design

## System Overview

CV Adviser is a single-page Streamlit application powered by Google Gemini via LangChain.
All processing is stateless — no user data is stored between sessions.

---

## Component Diagram

```
┌──────────────────────────────────────────────────────────────┐
│                        FRONTEND (Streamlit)                  │
│  ┌─────────────┐  ┌──────────────┐  ┌────────────────────┐  │
│  │  Sidebar    │  │  Main Page   │  │  Results / Tabs    │  │
│  │  (ui.py)    │  │  (app.py)    │  │  (ui.py)           │  │
│  └─────────────┘  └──────────────┘  └────────────────────┘  │
└──────────────────────────────────────────────────────────────┘
            │                   │
            ▼                   ▼
┌──────────────────────────────────────────────────────────────┐
│                    PROCESSING LAYER                          │
│  ┌──────────────────────┐  ┌─────────────────────────────┐  │
│  │  PDF Ingestion       │  │  LangChain LCEL Chains       │  │
│  │  PyPDFLoader         │  │  ├── cv_eval_chain           │  │
│  │  RecursiveTextSplit  │  │  ├── scoring_chain           │  │
│  │  helpers.py          │  │  ├── grammar_chain           │  │
│  └──────────────────────┘  │  └── skill_gap_chain         │  │
│                             └─────────────────────────────┘  │
└──────────────────────────────────────────────────────────────┘
            │
            ▼
┌──────────────────────────────────────────────────────────────┐
│                    LLM LAYER                                 │
│           Google Gemini 2.5 Flash Lite                       │
│           (via langchain-google-genai)                       │
└──────────────────────────────────────────────────────────────┘
```

---

## Data Flow

1. **User uploads PDF** → Streamlit file_uploader
2. **PDF saved to temp file** → `tempfile.NamedTemporaryFile`
3. **Text extracted** → `PyPDFLoader.load()`
4. **Text chunked** → `RecursiveCharacterTextSplitter(chunk_size=1000)`
5. **Text truncated** → `helpers.truncate_text(max_chars=6000)` for token safety
6. **Chains invoked** → Each PromptTemplate filled + sent to Gemini
7. **Results parsed** → `StrOutputParser` extracts plain text
8. **Rendered** → `components/ui.py` displays in Streamlit tabs
9. **Temp file deleted** → `os.remove(tmp_path)` in `finally` block

---

## Module Reference

### `app.py`
- Entry point
- Defines all `PromptTemplate` objects and `LCEL chains`
- Handles user input collection and chain orchestration

### `components/ui.py`
- `render_sidebar()` — left sidebar with logo, description, links
- `render_header()` — top of main page
- `render_results(...)` — tabbed display of all 4 analysis sections + download buttons

### `utils/helpers.py`
- `validate_pdf(file)` → `(bool, str)` — size and type validation
- `truncate_text(text, max_chars)` → `str` — prevents token limit errors
- `build_download_bundle(...)` → `str` — combines all reports into one Markdown file

---

## Security Notes

- API key loaded via `python-dotenv` from `.env` — never hardcoded
- `.env` is in `.gitignore` — never committed to Git
- Uploaded PDFs are stored only in OS temp directory and deleted immediately after processing
- No database, no user accounts, no persistent storage

---

## Prompt Design

All prompts follow this structure:
```
[Role assignment] + [Task description] + [Output format] + [Input variable]
```

Temperature is set to `0.7` — allows some creativity in suggestions while keeping
evaluation grounded. `max_output_tokens=2048` prevents runaway responses.

        # Mind Neuro AI - Minimal Chatbot (FastAPI + Gemini + Streamlit)

        ## Overview

This project is a minimal Mind Neuro AI chatbot using:

- FastAPI (backend)
- Gemini (Google Generative AI) as the LLM (configurable via .env)
- SQLite (chat history)
- Streamlit (simple frontend)

**This simplified version does not include RAG, file uploads, or Groq**.

---

## Setup

1. Clone or unzip the project and `cd` into the project folder:

```bash
cd /path/to/mind_neuro_ai
```

2. Create a virtual environment (recommended) and activate it:

```bash
python -m venv .venv
source .venv/bin/activate   # macOS / Linux
.venv\Scripts\activate     # Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Configure your Gemini (Google Generative AI) API key:

- Open `.env` and set `GOOGLE_API_KEY` to your API key.

5. Start the backend (FastAPI):

```bash
uvicorn backend.main:app --reload
```

The server will run at `http://127.0.0.1:8000`.

6. In a new terminal, start the Streamlit frontend:

```bash
streamlit run frontend/app.py
```

Open the Streamlit URL shown (usually `http://localhost:8501`).

---

## Notes

- If `google-generativeai` is not installed or `GOOGLE_API_KEY` is not set, the app will return a placeholder reply explaining it's not configured.
- Database `mindneuro.db` will be created automatically in the project root when the backend runs.

Enjoy building your Mind Neuro AI chatbot!

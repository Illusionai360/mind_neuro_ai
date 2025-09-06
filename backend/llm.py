from backend.config import GOOGLE_API_KEY, SYSTEM_PROMPT
try:
    import google.generativeai as genai
    genai.configure(api_key=GOOGLE_API_KEY)
    _HAS_GENAI = True
except Exception:
    _HAS_GENAI = False

def generate_answer(user_query: str) -> str:
    """
    Use Gemini API to generate a thoughtful AI response.
    If the google-generativeai package or API key is not available,
    return a helpful fallback message.
    """
    prompt = (
        f"{SYSTEM_PROMPT}\n\n"
        f"User query:\n{user_query}\n\n"
        f"Answer clearly and concisely.")
    if not _HAS_GENAI or not GOOGLE_API_KEY:
        return ("(Gemini not configured) This is a placeholder response.\n\n"
                "Set GOOGLE_API_KEY in your .env and install google-generativeai to enable real responses.\n"
                f"Prompt sent would be:\n{prompt[:800]}...")
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        resp = model.generate_content(prompt)
        return getattr(resp, "text", "I'm sorry, I couldn't generate a response right now.")
    except Exception as e:
        return f"(Error calling Gemini) {str(e)}"


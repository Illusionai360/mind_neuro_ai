
from fastapi import FastAPI, Form, Depends, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from backend.db import Base, engine, get_db
from backend.models import Chat, Message
from backend.schemas import ChatCreateOut, ChatHistoryOut, ChatThreadOut, MessageOut
from backend.llm import generate_answer

# create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Mind Neuro AI - Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)

@app.get("/api/health")
def health():
    return {"ok": True}

@app.post("/api/chats/new", response_model=ChatCreateOut)
def new_chat(db: Session = Depends(get_db)):
    chat = Chat(title="New chat")
    db.add(chat); db.commit(); db.refresh(chat)
    return {"id": chat.id, "title": chat.title}

@app.get("/api/chats", response_model=List[ChatHistoryOut])
def list_chats(db: Session = Depends(get_db)):
    rows = db.query(Chat).order_by(Chat.id.desc()).limit(50).all()
    return rows

@app.get("/api/chats/{chat_id}", response_model=ChatThreadOut)
def get_thread(chat_id: int, db: Session = Depends(get_db)):
    chat = db.query(Chat).get(chat_id)
    if not chat:
        return {"chat_id": chat_id, "messages": []}
    msgs = db.query(Message).filter(Message.chat_id==chat_id).order_by(Message.created_at.asc()).all()
    return {"chat_id": chat_id, "messages": msgs}

# @app.post("/api/chat", response_model=MessageOut)
# def chat(chat_id: int = Form(...), content: str = Form(...), db: Session = Depends(get_db)):
#     # save user message
#     user_msg = Message(chat_id=chat_id, role="user", content=content)
#     db.add(user_msg); db.commit(); db.refresh(user_msg)

# from fastapi import Body, HTTPException

@app.post("/api/chat", response_model=MessageOut)
def chat(chat_id: int = Form(...), content: str = Form(...), db: Session = Depends(get_db)):
    """
    Handles incoming chat message:
    1. Saves user's message
    2. Generates AI reply
    3. Saves and returns assistant's reply
    """
    # Save user message
    user_msg = Message(chat_id=chat_id, role="user", content=content)
    db.add(user_msg)
    db.commit()
    db.refresh(user_msg)

    # Generate assistant reply
    try:
        reply = generate_answer(content)
    except Exception as e:
        reply = f"(Error generating response: {e})"

    # Save assistant message
    bot_msg = Message(chat_id=chat_id, role="assistant", content=reply)
    db.add(bot_msg)
    db.commit()
    db.refresh(bot_msg)

    return bot_msg



@app.put("/api/chats/{chat_id}")
def rename_chat(chat_id: int, data: dict = Body(...), db: Session = Depends(get_db)):
    chat = db.query(Chat).get(chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    chat.title = data.get("title", chat.title)
    db.commit()
    return {"message": "Chat renamed successfully"}

@app.delete("/api/chats/{chat_id}")
def delete_chat(chat_id: int, db: Session = Depends(get_db)):
    chat = db.query(Chat).get(chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    db.delete(chat)
    db.commit()
    return {"message": "Chat deleted successfully"}

 

    # generate reply via Gemini (or fallback)
    reply = generate_answer(content)




    # save assistant message
    bot_msg = Message(chat_id=chat_id, role="assistant", content=reply)
    db.add(bot_msg); db.commit(); db.refresh(bot_msg)

    return bot_msg

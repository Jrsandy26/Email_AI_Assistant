from fastapi import FastAPI
from fastapi import WebSocket
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.staticfiles import StaticFiles

import asyncio
import sqlite3
import time

app = FastAPI()

templates = Jinja2Templates(directory="templates")

# static files (css / js)
app.mount("/static", StaticFiles(directory="templates"), name="static")


# -----------------------------
# DATABASE
# -----------------------------
def get_db():
    return sqlite3.connect("../email_ai.db")


# -----------------------------
# DASHBOARD PAGE
# -----------------------------
@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request):

    conn = get_db()
    cur = conn.cursor()

    # USERS
    cur.execute("SELECT COUNT(*) FROM users")
    users = cur.fetchone()[0]

    # ACTIVE USERS (last 5 min)
    cur.execute("""
    SELECT COUNT(DISTINCT session_id)
    FROM users
    WHERE created_at > datetime('now','-5 minutes')
    """)
    active_users = cur.fetchone()[0]

    # CONVERSATIONS
    cur.execute("SELECT COUNT(*) FROM conversations")
    conversations = cur.fetchone()[0]

    # TOTAL MESSAGES
    cur.execute("SELECT COUNT(*) FROM messages")
    messages = cur.fetchone()[0]

    # AI MESSAGES
    cur.execute("SELECT COUNT(*) FROM messages WHERE role='assistant'")
    ai_messages = cur.fetchone()[0]

    # USER MESSAGES
    cur.execute("SELECT COUNT(*) FROM messages WHERE role='user'")
    user_messages = cur.fetchone()[0]

    # ERRORS
    cur.execute("SELECT COUNT(*) FROM errors")
    errors = cur.fetchone()[0]

    # TOKEN USAGE
    cur.execute("SELECT SUM(tokens) FROM metrics_events")
    tokens = cur.fetchone()[0] or 0

    # AI LATENCY
    cur.execute("SELECT AVG(latency) FROM metrics_events")
    latency = cur.fetchone()[0] or 0

    # FEATURE USAGE
    cur.execute("""
    SELECT feature_name, COUNT(*)
    FROM feature_usage
    GROUP BY feature_name
    """)
    feature_usage = cur.fetchall()

    conn.close()

    # API cost estimate
    cost = round((tokens / 1000) * 0.0003, 4)

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "users": users,
            "active_users": active_users,
            "conversations": conversations,
            "messages": messages,
            "ai": ai_messages,
            "user": user_messages,
            "errors": errors,
            "tokens": tokens,
            "latency": round(latency, 2),
            "cost": cost,
            "feature_usage": feature_usage,
        },
    )


# -----------------------------
# REAL TIME METRICS API
# -----------------------------
@app.get("/api/live")
def live_metrics():

    conn = get_db()
    cur = conn.cursor()

    # messages per minute
    cur.execute("""
    SELECT COUNT(*)
    FROM messages
    WHERE created_at > datetime('now','-1 minute')
    """)
    messages_per_min = cur.fetchone()[0]

    # active users
    cur.execute("""
    SELECT COUNT(DISTINCT session_id)
    FROM users
    WHERE created_at > datetime('now','-5 minutes')
    """)
    active = cur.fetchone()[0]

    conn.close()

    return JSONResponse(
        {
            "messages_per_minute": messages_per_min,
            "active_users": active,
            "timestamp": time.time()
        }
    )


# -----------------------------
# CONVERSATION INSPECTOR
# -----------------------------
@app.get("/api/conversations")
def get_conversations():

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
    SELECT id,title,created_at
    FROM conversations
    ORDER BY created_at DESC
    LIMIT 50
    """)

    rows = cur.fetchall()

    conn.close()

    return rows


@app.get("/api/messages/{conversation_id}")
def get_messages(conversation_id: int):

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
    SELECT role,content,created_at
    FROM messages
    WHERE conversation_id=?
    """, (conversation_id,))

    rows = cur.fetchall()

    conn.close()

    return rows

# -----------------------------
# WEB ANALYTICS (REAL TIME)
# -----------------------------
@app.websocket("/ws/analytics")
async def analytics_ws(websocket: WebSocket):

    await websocket.accept()

    while True:

        conn = sqlite3.connect("../email_ai.db")
        cur = conn.cursor()

        # avg runtime
        cur.execute("SELECT AVG(latency) FROM metrics_events")
        runtime = cur.fetchone()[0] or 0

        # token usage
        cur.execute("SELECT SUM(tokens) FROM metrics_events")
        tokens = cur.fetchone()[0] or 0

        conn.close()

        # cost estimate
        cost = (tokens / 1000) * 0.0003

        await websocket.send_json({
            "runtime": round(runtime * 1000, 2),
            "cost": round(cost, 4)
        })

        await asyncio.sleep(3)
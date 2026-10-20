from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import psycopg2
import requests
import os

app = FastAPI()

# Разрешаем Frontend обращаться к Backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "db"),
        database=os.getenv("DB_NAME", "postgres"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "postgres")
    )

class MeetingRequest(BaseModel):
    title: str
    base_time: str
    target_timezone: str

@app.get("/meetings")
def get_meetings():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, title, base_time, target_timezone, converted_time FROM meetings ORDER BY id ASC;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [{"id": r[0], "title": r[1], "base_time": str(r[2]), "target_tz": r[3], "converted_time": str(r[4]) if r[4] else None} for r in rows]

@app.post("/add_meeting")
def add_meeting(meeting: MeetingRequest):
    # Запрос к Web-сервису
    ws_url = "http://web-service:8001/convert"
    ws_response = requests.post(ws_url, json={
        "base_time_str": meeting.base_time,
        "target_tz": meeting.target_timezone,
        "source_tz": "Europe/Moscow"
    })
    
    converted = None
    if ws_response.status_code == 200:
        converted = ws_response.json().get("converted_time")

    # Сохранение в БД
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO meetings (title, base_time, target_timezone, converted_time) VALUES (%s, %s, %s, %s)",
        (meeting.title, meeting.base_time, meeting.target_timezone, converted)
    )
    conn.commit()
    cur.close()
    conn.close()
    return {"status": "success", "converted": converted}

@app.delete("/delete_meeting/{meeting_id}")
def delete_meeting(meeting_id: int):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM meetings WHERE id = %s", (meeting_id,))
    conn.commit()
    cur.close()
    conn.close()
    return {"status": "success"}

# --- Блок для независимого конвертера ---

class StandaloneRequest(BaseModel):
    base_time: str
    source_tz: str
    target_tz: str

@app.post("/convert_standalone")
def convert_standalone(req: StandaloneRequest):
    ws_url = "http://web-service:8001/convert"
    ws_response = requests.post(ws_url, json={
        "base_time_str": req.base_time,
        "target_tz": req.target_tz,
        "source_tz": req.source_tz
    })
    if ws_response.status_code == 200:
        return ws_response.json()
    return {"error": "Ошибка внешнего веб-сервиса"}
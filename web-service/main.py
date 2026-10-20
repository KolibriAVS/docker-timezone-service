from fastapi import FastAPI
from pydantic import BaseModel
import pytz
from datetime import datetime

app = FastAPI()

class TimeData(BaseModel):
    base_time_str: str
    target_tz: str

@app.post("/convert")
def convert_time(data: TimeData):
    try:
        # 1. Парсим строку в объект времени
        dt_naive = datetime.strptime(data.base_time_str, "%Y-%m-%d %H:%M:%S")
        
        # 2. Устанавливаем исходный часовой пояс (Москва, UTC+3)
        base_tz = pytz.timezone("Europe/Moscow")
        dt_aware = base_tz.localize(dt_naive)
        
        # 3. Переводим в целевой часовой пояс
        target_tz = pytz.timezone(data.target_tz)
        converted = dt_aware.astimezone(target_tz)
        
        return {"converted_time": converted.strftime("%Y-%m-%d %H:%M:%S")}
    except Exception as e:
        return {"error": str(e)}
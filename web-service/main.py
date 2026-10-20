from fastapi import FastAPI
from pydantic import BaseModel
import pytz
from datetime import datetime
from typing import Optional

app = FastAPI()

class TimeData(BaseModel):
    base_time_str: str
    target_tz: str
    source_tz: Optional[str] = "Europe/Moscow" # По умолчанию оставляем Москву, чтобы не сломать старые записи

@app.post("/convert")
def convert_time(data: TimeData):
    try:
        dt_naive = datetime.strptime(data.base_time_str, "%Y-%m-%d %H:%M:%S")
        base_tz = pytz.timezone(data.source_tz)
        dt_aware = base_tz.localize(dt_naive)
        
        target_tz = pytz.timezone(data.target_tz)
        converted = dt_aware.astimezone(target_tz)
        
        # Расчет разницы в часах
        diff_hours = (converted.utcoffset() - dt_aware.utcoffset()).total_seconds() / 3600
        diff_str = f"+{int(diff_hours)}" if diff_hours > 0 else str(int(diff_hours))
        
        return {
            "converted_time": converted.strftime("%Y-%m-%d %H:%M:%S"),
            "difference": diff_str
        }
    except Exception as e:
        return {"error": str(e)}
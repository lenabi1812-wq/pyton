from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

app = FastAPI(title="Клуб будущего")
templates = Jinja2Templates(directory="templates")

events = [
    {
        "id": 1,
        "title": "Лаборатория марсоходов",
        "direction": "Инженерия",  # <-- Добавили поле
        "seats": 8,
        "status": "Открыта",
    },
    {
        "id": 2,
        "title": "Космический квиз",
        "direction": "Астрономия",  # <-- Добавили поле
        "seats": 0,
        "status": "Регистрация завершена",
    },
    {
        "id": 3,
        "title": "Создание игры на Python",
        "direction": "Программирование",  # <-- Добавили поле
        "seats": 12,
        "status": "Открыта",
    },
    {
        "id": 4,                           # <-- Добавили новое мероприятие
        "title": "Робототехника",
        "direction": "Инженерия",
        "seats": 5,
        "status": "Открыта",
    }
]

class Event(BaseModel):
    id: int
    title: str
    direction: str
    seats: int
    status: str

@app.get("/api/events", response_model=list[Event])
def get_events():
    return events

@app.get("/api/events/open", response_model=list[Event])
def get_open_events():
    return [event for event in events if event["status"] == "Открыта"]

@app.get("/", response_class=HTMLResponse)
def get_index(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"events": events},
    )
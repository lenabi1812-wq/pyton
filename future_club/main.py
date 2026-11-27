from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

app = FastAPI(title="Клуб будущего")
templates = Jinja2Templates(directory="templates")

events = [
    {
        "id": 1,
        "title": "Лаборатория марсоходов",
        "direction": "Инженерия",
        "seats": 8,
        "status": "Открыта",
    },
    {
        "id": 2,
        "title": "Космический квиз",
        "direction": "Астрономия",
        "seats": 0,
        "status": "Регистрация завершена",
    },
    {
        "id": 3,
        "title": "Создание игры на Python",
        "direction": "Программирование",
        "seats": 12,
        "status": "Открыта",
    }
]


class Event(BaseModel):
    id: int
    title: str
    direction: str
    seats: int
    status: str


class EventCreate(BaseModel):
    title: str
    seats: int


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


@app.get("/events/new", response_class=HTMLResponse)
def get_new_event_form(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="new_event.html",
    )


@app.post("/events/new")
def create_event(
        title: str = Form(),
        seats: int = Form(),
):
    new_event = {
        "id": len(events) + 1,
        "title": title,
        "seats": seats,
        "status": "Открыта",
        "direction": "Не указано"
    }

    if seats == 0:
        new_event["status"] = "Регистрация завершена"

    events.append(new_event)
    return RedirectResponse(url="/", status_code=303)


@app.post("/api/events", status_code=201)
def create_event_api(event_data: EventCreate):
    new_event = {
        "id": len(events) + 1,
        "title": event_data.title,
        "seats": event_data.seats,
        "status": "Открыта",
        "direction": "Не указано"
    }

    if event_data.seats == 0:
        new_event["status"] = "Регистрация завершена"

    events.append(new_event)
    return new_event
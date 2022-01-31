from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
from app.models import mongodb
from app.models.book import BookModel

BASE_DIR = Path(__file__).resolve().parent.parent

app = FastAPI()
templates = Jinja2Templates(directory=BASE_DIR / "templates")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    book = BookModel(
        keyword="python",
        publisher="BJpublic",
        price=1200,
        image="me.png",
        hhh="asdf",
    )
    print(book)
    await mongodb.engine.save(book)  # DB에 저장된다.
    return templates.TemplateResponse(
        "/index.html", {"request": request, "title": "북 콜렉터"}
    )


@app.get("/search", response_class=HTMLResponse)
async def search(request: Request, q: str):
    print(q)
    return templates.TemplateResponse(
        "/index.html", {"request": request, "title": "북 콜렉터", "keyword": q}
    )


@app.on_event("startup")
async def on_app_start():
    print("server started...")
    """before app starts"""
    mongodb.connect()


@app.on_event("shutdown")
async def on_app_shutdown():
    print("server shutdown...")
    """after app shutdown"""
    print(mongodb.__dir__())

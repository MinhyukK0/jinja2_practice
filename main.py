from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path

# 절대 경로 설정 (fastAPIProject/app폴더를 절대경로로 설정함)
BASE_DIR = Path(__file__).parent


app = FastAPI()


templates = Jinja2Templates(directory=BASE_DIR/"templates")


@app.get("/items/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id: str):
    return templates.TemplateResponse("item.html", {"request": request, "id": id, "framework": "fastapi"})

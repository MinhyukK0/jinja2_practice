from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
from app.models import mongodb
from app.models.book import BookModel
from app.book_scraper import NaverBookScraper

BASE_DIR = Path(__file__).resolve().parent.parent

app = FastAPI()
templates = Jinja2Templates(directory=BASE_DIR / "app/templates")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    # book = BookModel(
    #     keyword="python",
    #     publisher="BJpublic",
    #     price=1200,
    #     image="me.png",
    #     hhh="asdf",
    # )
    # print(book)
    # await mongodb.engine.save(book)  # DB에 저장된다.
    return templates.TemplateResponse(
        "/index.html", {"request": request, "title": "북 콜렉터"}
    )


@app.get("/search", response_class=HTMLResponse)
async def search(request: Request, q: str):
    """
    로직 설계
    # 1 쿼리에서 검색어를 추출한다.
        - 검색어가 없다면 검색을 요구
        - 해당 검색어에 대한 수집된 데이터가 존재한다면, 해당 데이터를 사용자에게 보여준다.
    # 2 데이터 수집기로 해당 검색어에 대한 데이터를 수집한다.
    # 3 db에 데이터를 저장한다.
        - 수집된 각각의 데이터에 대해서 db 인스턴스 모델로 시리얼라이징한다.
        - db에 저장한다.
    """
    # 1
    keyword = q
    naver_book_scraper = NaverBookScraper()
    # 2
    books = await naver_book_scraper.search(keyword=keyword, total_page=10)
    # 3
    book_model_list = [BookModel(keyword=keyword, **book)for book in books if book.title]
    await mongodb.engine.save_all(book_model_list)
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
    mongodb.close()

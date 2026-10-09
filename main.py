
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, RedirectResponse
from pydantic import BaseModel, HttpUrl

from url_shortener import URLShortener

app = FastAPI(
    title="SmartURL",
    description="A URL shortener with SQLite storage and LRU caching",
    version="1.0.0"
)

shortener = URLShortener()
FRONTEND = Path(__file__).parent / "static" / "index.html"


class URLRequest(BaseModel):
    original_url: HttpUrl


@app.get("/", include_in_schema=False)
def home():
    return FileResponse(FRONTEND)


@app.get("/health")
def health():
    return {"status": "healthy", "service": "SmartURL"}


@app.post("/shorten", status_code=201)
def create_short_url(request: URLRequest):
    original_url = str(request.original_url)
    code = shortener.shorten_url(original_url)

    return {
        "short_code": code,
        "short_url": f"http://127.0.0.1:8000/{code}",
        "original_url": original_url
    }


@app.get("/stats/{short_code}")
def url_stats(short_code: str):
    stats = shortener.get_stats(short_code)

    if stats is None:
        raise HTTPException(
            status_code=404,
            detail="Short URL not found"
        )

    return {"short_code": short_code, **stats}


@app.get("/{short_code}", include_in_schema=False)
def redirect_to_original(short_code: str):
    original_url = shortener.get_original_url(short_code)

    if original_url is None:
        raise HTTPException(
            status_code=404,
            detail="Short URL not found"
        )

    shortener.record_click(short_code)
    return RedirectResponse(url=original_url, status_code=307)
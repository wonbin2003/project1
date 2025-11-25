from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from crawler import crawl_url, CrawlError
from gemini_summarizer import summarize_recipe


app = FastAPI()


class UrlRequest(BaseModel):
    url: str


@app.post("/api/recipe")
def api_recipe(req: UrlRequest):
    try:
        raw_text = crawl_url(req.url)
    except CrawlError as e:
        raise HTTPException(status_code=400, detail=str(e))
    if not raw_text.strip():
        raise HTTPException(status_code=400, detail="텍스트를 추출하지 못했습니다.")
    summary = summarize_recipe(raw_text)
    return {
        "url": req.url,
        "recipe": summary
    }

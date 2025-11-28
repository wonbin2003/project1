from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel
from crawler import crawl_url, CrawlError
from gemini_summarizer import summarize_recipe

app = FastAPI()

# 🔓 CORS는 불필요하지만 혹시 JS 외부 접근 대비해 유지
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 📂 정적파일, 템플릿 경로 지정
app.mount("/static", StaticFiles(directory= "static"), name="static")
templates = Jinja2Templates(directory="templates")

# 📄 HTML 렌더링 라우터
@app.get("/", response_class=HTMLResponse)
async def serve_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# 🔌 API 엔드포인트
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

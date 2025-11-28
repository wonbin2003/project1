import re
from urllib.parse import urlparse, parse_qs, urljoin

import requests
from bs4 import BeautifulSoup
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound

from dotenv import load_dotenv
load_dotenv()  # .env 파일에서 환경변수 자동 불러오기


class CrawlError(Exception):
    pass


def is_youtube_url(url: str) -> bool:
    host = (urlparse(url).hostname or "").lower()
    return "youtube.com" in host or "youtu.be" in host


def extract_youtube_video_id(url: str) -> str:
    parsed = urlparse(url)
    host = (parsed.hostname or "").lower()
    if "youtube.com" in host:
        query = parse_qs(parsed.query)
        if "v" in query:
            return query["v"][0]
    if "youtu.be" in host:
        return parsed.path.lstrip("/")
    raise CrawlError("유효한 유튜브 URL이 아닙니다.")


def fetch_youtube_transcript_text(url: str, preferred_langs=None) -> str:
    if preferred_langs is None:
        preferred_langs = ["ko", "ko-KR", "en"]
    video_id = extract_youtube_video_id(url)
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
    except TranscriptsDisabled:
        raise CrawlError("해당 영상은 자막이 비활성화되어 있습니다.")
    except NoTranscriptFound:
        raise CrawlError("해당 영상에 사용 가능한 자막이 없습니다.")
    transcript = None
    for code in preferred_langs:
        try:
            transcript = transcript_list.find_transcript([code])
            break
        except Exception:
            continue
    if transcript is None:
        try:
            transcript = transcript_list.find_generated_transcript(preferred_langs)
        except Exception:
            raise CrawlError("선호 언어 자막을 찾을 수 없습니다.")
    chunks = transcript.fetch()
    lines = []
    for c in chunks:
        t = c.get("text", "").replace("\n", " ").strip()
        if t:
            lines.append(t)
    text = " ".join(lines)
    text = re.sub(r"\s+", " ", text)
    if not text:
        raise CrawlError("자막 텍스트가 비어 있습니다.")
    return text


def _clean_soup_text(soup: BeautifulSoup) -> str:
    for tag in soup(["script", "style", "noscript", "header", "footer", "nav", "aside"]):
        tag.decompose()
    text = soup.get_text("\n")
    lines = [line.strip() for line in text.splitlines()]
    lines = [l for l in lines if l]
    filtered = []
    noise_patterns = [
        "로그인",
        "회원가입",
        "이웃추가",
        "이웃 추가",
        "광고",
        "Sponsored",
        "관련 글",
        "이 포스트 공유",
        "댓글 쓰기",
    ]
    for line in lines:
        if len(line) < 4:
            continue
        if any(p in line for p in noise_patterns):
            continue
        filtered.append(line)
    result = "\n".join(filtered)
    return result


def fetch_html(url: str, headers=None, timeout=10) -> str:
    if headers is None:
        headers = {"User-Agent": "Mozilla/5.0 recipe-summarizer"}
    resp = requests.get(url, headers=headers, timeout=timeout)
    resp.raise_for_status()
    return resp.text


def fetch_naver_blog_text(url: str) -> str:
    html = fetch_html(url)
    soup = BeautifulSoup(html, "html.parser")
    iframe = soup.find("iframe", id="mainFrame")
    if iframe is None:
        iframe = soup.find("iframe", src=re.compile("blog.naver.com"))
    if iframe is None:
        return _clean_soup_text(soup)
    iframe_src = iframe.get("src", "")
    if not iframe_src:
        return _clean_soup_text(soup)
    iframe_url = urljoin(url, iframe_src)
    iframe_html = fetch_html(iframe_url)
    iframe_soup = BeautifulSoup(iframe_html, "html.parser")
    return _clean_soup_text(iframe_soup)


def fetch_generic_blog_text(url: str) -> str:
    html = fetch_html(url)
    soup = BeautifulSoup(html, "html.parser")
    return _clean_soup_text(soup)


def fetch_blog_text(url: str) -> str:
    host = (urlparse(url).hostname or "").lower()
    if "blog.naver.com" in host:
        return fetch_naver_blog_text(url)
    return fetch_generic_blog_text(url)


def crawl_url(url: str) -> str:
    if is_youtube_url(url):
        return fetch_youtube_transcript_text(url)
    text = fetch_blog_text(url)
    if not text.strip():
        raise CrawlError("블로그 본문 텍스트가 비어 있습니다.")
    return text

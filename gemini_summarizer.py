import os
import json
import google.generativeai as genai



GEMINI_PROMPT_TEMPLATE = """
너는 요리 레시피를 초보자도 쉽게 따라 할 수 있게 정리하는 전문 어시스턴트이다.

이 텍스트를 읽고, 아래 JSON 형식에 정확하게 맞추어 한글로 출력하라.

JSON 필드 설명:
- recipe_name: 요리 이름. 텍스트에서 유추해서 간단하게 한 줄로 작성. 없으면 대표적인 이름을 짧게 지어서 넣는다.
- ingredients: 필요한 재료를 ["재료명 수량 단위"] 형식으로 나열. 예: ["양파 1개", "간장 2큰술"]. 수량이 정확하지 않으면 대략 추정해서 "(약)"을 붙인다.
- steps: 초보자 기준으로 매우 쉽게 쪼갠 단계 설명. 각 단계는 한 문장 또는 두 문장 정도로, 순서대로 나열한다.
- time: 전체 예상 소요 시간(준비+조리) 한글 설명으로 적는다. 예: "약 20분", "30~40분".
- level: 난이도를 "매우 쉬움", "쉬움", "보통", "어려움" 중 하나로 선택한다.

반드시 아래 형식의 JSON만 출력하고, 추가 설명이나 코드 블록 기호는 절대 포함하지 마라.

{{
  "recipeName": "",
  "ingredients": [],
  "steps": [],
  "cookingTime": ""
}}

입력 텍스트는 다음과 같다:

[RECIPE_TEXT_START]
{recipe_text}
[RECIPE_TEXT_END]
"""

def setup_gemini():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("❌ GEMINI_API_KEY 환경 변수가 설정되지 않았습니다.")
    
    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-2.5-flash")

def summarize_recipe(text: str) -> dict:
    model = setup_gemini()

    # 너무 길면 자르기
    truncated = text[:10000]
    prompt = GEMINI_PROMPT_TEMPLATE.format(recipe_text=truncated)

    # Gemini 호출
    response = model.generate_content(prompt)
    raw = response.text or ""

    if not raw.strip():
        raise ValueError("❌ Gemini가 빈 응답을 반환했습니다.")

    # --- JSON 부분만 자동 추출 ---
    try:
        start = raw.index("{")
        end = raw.rindex("}") + 1
        json_str = raw[start:end]
        return json.loads(json_str)

    except Exception as e:
        print("🔴 Gemini 응답 원본:")
        print(raw)
        raise ValueError("❌ JSON 파싱 실패: " + str(e))

import os
import requests
from dotenv import load_dotenv
from .answer_llm import llm_answer

load_dotenv()
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

def tavily_search(user_query: str) -> str:
    """
    Tavily API를 사용하여 외부 검색을 수행하고, Gemma로 최종 응답 생성.
    지정한 와인 관련 도메인만 대상으로 검색하며, 정확한 정보가 없을 경우에도 배경 설명을 제공하도록 유도.
    """
    url = "https://api.tavily.com/search"
    headers = {"Content-Type": "application/json"}

    # ✅ 검색 쿼리에 site 필터 명시적으로 포함
    domain_sites = ["wine21.com", "wine.co.kr", "google.com", "naver.com"]
    filtered_query = f'{user_query} site:' + ' OR site:'.join(domain_sites)

    payload = {
        "api_key": TAVILY_API_KEY,
        "query": filtered_query,
        "search_depth": "advanced",
        "include_answer": False,
        "include_raw_content": True,
        "num_results": 3,
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    results = response.json().get("results", [])

    if not results:
        return "외부 검색 결과를 찾을 수 없었습니다."

    # ✅ 가장 관련성 높은 문서 1개만 사용
    top_result = results[0]
    content = top_result.get("content", "")
    source_url = top_result.get("url", "")

    # ✅ 프롬프트: 배경 설명 유도 + 전문가 어투
    prompt = f"""
    당신은 와인 분야에 특화된 전문 큐레이터입니다.  
    아래는 외부 웹에서 수집된 문서 내용입니다:

    {content}

    이 자료를 바탕으로 사용자 질문에 대해 다음 조건을 충실히 반영해 정리해 주세요:

    1. **반드시 위의 문서(context)에 포함된 정보만 사용**하세요.  
    2. 내용을 항목별로 요약 정리하되, **빠짐없이 정확하게** 구성하세요.  
    3. 출력은 HTML 형식으로 하며, 다음과 같은 구성 순서를 지킵니다:
    - <b>요약:</b> 한두 문장으로 핵심 정리 후 `<br><br>` 줄바꿈
    - `<ul><li>` 형식으로 주요 특징을 나열 후 `<br><br>` 줄바꿈
    - 그 아래에 문단 형태로 부가 설명을 덧붙이세요.
    4. 감성 표현은 생략하고, **정보 중심의 간결하고 명확한 설명**을 작성하세요.

    질문: {user_query}
    """



    answer = llm_answer(prompt)

    if source_url:
        answer += f"<br><br><a href='{source_url}' target='_blank'>🔗 참고 링크</a>"

    return answer
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
    당신은 와인 전문 큐레이터입니다.

    다음은 외부 웹 문서에서 수집된 정보입니다.  
    이 정보를 바탕으로 사용자 질문에 대해 정확하고 신뢰감 있게 답변해주세요.

    - 질문에 대한 직접적인 정보가 부족할 경우, 관련 배경 지식이나 일반적인 트렌드를 제시해주세요.
    - '정보가 없습니다'라는 말은 피하고, 가능한 한 풍부하게 설명해주세요.
    - 반드시 친절하고 전문가다운 어투로 작성해주세요.

    [외부 문서 정보]
    {content}

    [사용자 질문]
    {user_query}

    [와인 전문가의 답변]
    """

    answer = llm_answer(prompt)

    # ✅ 관련성 높은 링크 1개만 표시
    if source_url:
        answer += f"\n\n🔗 참고 링크: {source_url}"

    return answer

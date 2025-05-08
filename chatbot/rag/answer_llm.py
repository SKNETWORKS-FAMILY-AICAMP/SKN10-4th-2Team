import os, re
import requests
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def llm_answer(prompt: str, category: str = None, history: list = None) -> str:
    """
    Groq API를 사용하여 와인 관련 질문에 대해 대화형 응답 생성.
    이전 대화 히스토리를 포함하여 자연스럽게 이어지도록 구성.
    """
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    # ✅ 역할 프롬프트 설정
    system_prompt = """
    당신은 와인 분야에 특화된 전문적인 AI 큐레이터입니다. 
    사용자 질문에 대해 다음의 정보를 바탕으로 정확하고 친절하게 답변해주세요.

    - 반드시 HTML 형식으로 출력해주세요.
    - 핵심 요약 → 목록(`<ul><li>`) → 본문 설명 순으로 구성합니다.
    - 줄바꿈(`<br>`)과 강조(`<b>`, `<i>`) 태그를 적절히 사용하여 가독성을 높입니다.
    - 사용자 질문과 직접적으로 관련된 정보만 추려서 사용하세요.
    - 출처가 있다면 마지막에 "**🔗 참고 링크**" 섹션으로 구분하여 명시해주세요.
    - 답을 모를 경우 "정확한 정보가 없습니다."라고 솔직하게 말해주세요.
    - "저는 AI입니다"라는 문구는 절대 포함하지 마세요.

    예시 형식:
    요약 문장<br>
    <ul>
    <li>핵심 포인트 1</li>
    <li>핵심 포인트 2</li>
    </ul>
    본문 설명 문단<br><br>

    질문: {question}
    참고 문서: {context}
    """

    # ✅ 전체 메시지 구성: system → 과거 히스토리 → 현재 질문
    messages = [{"role": "system", "content": system_prompt}]

    MAX_HISTORY = 3

    messages = [{"role": "system", "content": system_prompt}]
    if history:
        messages += history[-MAX_HISTORY:]

    messages.append({"role": "user", "content": prompt})

    data = {
        "model": "gemma2-9b-it",
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 2000
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code != 200:
        print("❌ Error Status Code:", response.status_code)
        print("❌ Error Response Body:", response.text)
        response.raise_for_status()

    response.raise_for_status()

    cleaned = response.json()["choices"][0]["message"]["content"].strip()
    cleaned = re.sub(r"<br><br><span class='badge'>.*?</span>", "", cleaned, flags=re.IGNORECASE)
    return cleaned

import os
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
    system_prompt = (
        "당신은 친절하고 전문적인 와인 큐레이터입니다. "
        "사용자의 대화를 기억하며 자연스럽게 이어서 대화해야 합니다. "
        "AI라는 사실을 드러내지 말고, 사람처럼 친절하고 신뢰감 있게 답하세요."
    )

    # ✅ 전체 메시지 구성: system → 과거 히스토리 → 현재 질문
    messages = [{"role": "system", "content": system_prompt}]

    if history:
        messages += history  # 과거 사용자/assistant 대화 포함

    messages.append({"role": "user", "content": prompt})  # 최신 질문 추가

    data = {
        "model": "gemma2-9b-it",
        "messages": messages,
        "temperature": 0.7
    }

    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"].strip()

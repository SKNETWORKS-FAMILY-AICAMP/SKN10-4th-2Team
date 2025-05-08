import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

openai = OpenAI()

def is_relevant(user_question: str, answer: str) -> bool:
    """
    GPT-4o-mini를 이용해 질문과 응답의 정확한 관련성을 판단해주세요.
    반드시 '질문을 정확하게 분석하여 답변과 연관성이 있는지 여부'에 초점을 맞춰 평가해주세요.
    """
    prompt = f"""
    다음 사용자 질문과 AI 응답의 관련성을 평가해 주세요.

    아래 기준을 반드시 따르세요:

    - 응답이 문서 기반의 정확한 정보를 포함하고 있어야 1을 반환합니다.
    - 일반적인 상식, 추측, 감성적 표현만 있거나 구체적 근거가 부족한 경우는 0입니다.
    - 질문의 핵심을 직접적으로 설명하지 않거나, 문서에 없는 내용을 상상하거나 과장했다면 0을 반환하세요.
    - 반드시 질문에 정밀하고 구체적으로 답해야 합니다.

    오직 숫자만 출력하세요.  
    "0" 또는 "1"만 반환하세요. 부가 설명은 하지 마세요.

    질문: "{user_question}"  
    응답: "{answer}"  
    관련성 점수:
    """


    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )

    result = response.choices[0].message.content.strip().lower()
    print(f"[🔍] 관련성 평가 결과: {result}")
    return result == "1"


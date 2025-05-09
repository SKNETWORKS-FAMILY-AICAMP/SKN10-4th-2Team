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
    다음은 사용자 질문과 AI의 응답입니다.  
    응답이 질문에 대해 **정확하고 근거 있는 정보**를 제공했는지 평가하세요.

    아래 기준을 반드시 따르세요:

    - 응답이 **실제 문서 기반의 구체적인 정보**를 포함해야만 '1'을 반환합니다.
    - 단순한 일반 지식, 감성적인 말, 추측이나 불확실한 설명만 있을 경우 '0'을 반환하세요.
    - 질문의 **핵심에 대한 직접적이고 명확한 설명**이 없다면 무조건 '0'을 반환하세요.
    - 응답이 **사실에 기반하지 않거나, 답을 회피하거나, 유사하지만 틀린 정보**라면 무조건 '0'입니다.

    오직 숫자만 출력하세요.  
    정답은 반드시 "1" 또는 "0" 중 하나여야 하며, 부가 설명은 포함하지 마세요.

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


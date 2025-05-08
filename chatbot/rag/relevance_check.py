import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

openai = OpenAI()

def is_relevant(user_question: str, answer: str) -> bool:
    """
    GPT-4o-mini를 이용해 질문과 응답의 정확한 관련성을 판단해주세요.
    단순한 주제 유사성보다 반드시 '출처가 정확한 정보 제공 여부'에 초점을 맞춰 평가해주세요.
    """
    prompt = f"""다음 사용자 질문과 응답의 관련성을 평가해줘.

    - 응답이 질문의 핵심을 정확히 다루지 못하거나, 불분명하거나, 질문을 회피하거나, 시점/사실 누락이 있다면 '0'을 반환해.
    - 응답이 질문에 명확하고 구체적인 답을 제공했다면 '1'을 반환해주세요.
    - 질문과 주제가 비슷해도 정확한 답이 아니면 반드시 '0'을 반환해주세요.

    질문: "{user_question}"
    응답: "{answer}"

    관련성 점수 (1 또는 0):"""

    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )

    result = response.choices[0].message.content.strip().lower()
    print(f"[🔍] 관련성 평가 결과: {result}")
    return result == "1"


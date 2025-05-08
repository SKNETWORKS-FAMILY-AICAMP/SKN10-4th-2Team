import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

openai = OpenAI()

def generate_multi_queries(user_question: str) -> list[str]:
    """
    사용자 질문에 대해 와인의 맛, 특징, 구매 판단에 도움을 줄 수 있는 서브 질문 3개 생성.
    """
    prompt = f"""당신은 와인 전문 큐레이터입니다.

    사용자의 질문은 특정 와인이나 와인 종류에 대해 "이 와인을 마시기 전에 어떤 맛일지, 어떤 특징이 있을지" 알고 싶어서 묻는 경우가 많습니다.

    아래 사용자 질문을 더 잘 이해하고, 구체적으로 와인의 **맛, 향, 스타일, 유사한 와인**을 설명할 수 있도록 서브 질문 3개를 생성해 주세요.

    - 사용자가 구매를 고려 중이라는 점을 고려하세요.
    - 음식 궁합, 맛, 향 등 **선택에 도움 되는 정보** 중심으로 구성해주세요.
    - 질문 번호 없이 간결하게 출력해주세요.

    사용자 질문: "{user_question}"
    """

    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )

    content = response.choices[0].message.content.strip()
    queries = [line.strip() for line in content.split("\n") if line.strip()]
    return queries[:3]


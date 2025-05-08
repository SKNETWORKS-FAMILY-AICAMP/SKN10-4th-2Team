import re
from openai import OpenAI
from dotenv import load_dotenv
from .entity_names import get_known_entities

load_dotenv()
openai = OpenAI()

def normalize_name(name: str) -> str:
    name = re.sub(r"[^\w\s]", " ", name)  # 특수문자 제거
    name = re.sub(r"\s+", " ", name)      # 다중 공백 제거
    return name.lower().strip()

# ✅ 캐시된 엔티티 불러오기 (1회만 수행됨)
ENTITIES = get_known_entities()

KNOWN_WINE_NAMES = ENTITIES["wine"]
KNOWN_GRAPE_NAMES = ENTITIES["grape"]
KNOWN_REGION_NAMES = ENTITIES["region"]
KNOWN_PRODUCER_NAMES = ENTITIES["producer"]

# ✅ 카테고리 분류 함수
def classify_category(user_question: str) -> str:
    lowered_question = normalize_name(user_question)

    for name in KNOWN_WINE_NAMES:
        if name in lowered_question:
            return "wine"
    for name in KNOWN_GRAPE_NAMES:
        if name in lowered_question:
            return "grape"
    for name in KNOWN_REGION_NAMES:
        if name in lowered_question:
            return "region"
    for name in KNOWN_PRODUCER_NAMES:
        if name in lowered_question:
            return "producer"

    greetings = ["안녕", "안녕하세요", "하이", "hello", "ㅎㅇ", "반가워", "잘 지냈어", "굿모닝", "오랜만", "하이요"]
    if any(greet in lowered_question for greet in greetings):
        return "greeting"

    # fallback: GPT-4o-mini 분류
    prompt = f"""다음 사용자 질문을 가장 적절한 카테고리로 분류해줘. 
카테고리는 다음 중 하나야: wine, grape, region, producer, etc

- 와인 추천, 가격, 종류, 향, 음식 매칭은 모두 'wine'
- 특정 와인 생산지에 대한 질문은 'region'
- 포도 품종에 대한 질문은 'grape'
- 와인 제조사, 브랜드 관련 질문은 'producer'
- 위에 해당하지 않으면 'etc'

사용자 질문: "{user_question}"
카테고리:"""

    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    result = response.choices[0].message.content.strip().lower()
    return result if result in ["wine", "grape", "region", "producer"] else "etc"

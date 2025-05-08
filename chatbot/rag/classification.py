import os
import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
openai = OpenAI()

# ✅ 경로 기반 정제된 CSV → set 로드
def load_entity_names(csv_path: str) -> set:
    if not os.path.exists(csv_path):
        print(f"[⚠️] 파일 없음: {csv_path}")
        return set()
    df = pd.read_csv(csv_path)
    if "name" not in df.columns:
        print(f"[⚠️] 'name' 컬럼 없음: {csv_path}")
        return set()
    return set(df["name"].dropna().astype(str).str.lower().str.strip())

# ✅ 사전 정의된 정제된 엔티티 CSV 경로
ENTITY_BASE = "VectorDB/entity_names"

KNOWN_WINE_NAMES = load_entity_names(os.path.join(ENTITY_BASE, "wine/names.csv"))
KNOWN_GRAPE_NAMES = load_entity_names(os.path.join(ENTITY_BASE, "grape/names.csv"))
KNOWN_REGION_NAMES = load_entity_names(os.path.join(ENTITY_BASE, "region/names.csv"))
KNOWN_PRODUCER_NAMES = load_entity_names(os.path.join(ENTITY_BASE, "producer/names.csv"))

print(f"[🔍] 로드된 와인명 개수: {len(KNOWN_WINE_NAMES)}")
print(f"[🔍] 로드된 포도 품종 개수: {len(KNOWN_GRAPE_NAMES)}")
print(f"[🔍] 로드된 생산지역 개수: {len(KNOWN_REGION_NAMES)}")
print(f"[🔍] 로드된 생산자 개수: {len(KNOWN_PRODUCER_NAMES)}")

# ✅ 카테고리 분류 함수
def classify_category(user_question: str) -> str:
    lowered_question = user_question.lower()

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

    # fallback
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

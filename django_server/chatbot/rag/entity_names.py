import os, re
import pandas as pd
from glob import glob

# 내부 캐시
_entity_cache = {}

def normalize_name(name: str) -> str:
    name = re.sub(r"[^\w\s]", " ", name)  # 특수문자 제거
    name = re.sub(r"\s+", " ", name)      # 다중 공백 제거
    return name.lower().strip()

def load_column_values_from_csv(folder_path: str, column_name: str) -> set:
    values = set()
    csv_files = glob(os.path.join(folder_path, "*.csv"))

    for file_path in csv_files:
        try:
            df = pd.read_csv(file_path)
            if column_name in df.columns:
                cleaned = df[column_name].dropna().astype(str).map(normalize_name)
                values.update(cleaned)
        except Exception as e:
            print(f"[⚠️] CSV 로드 실패: {file_path} → {e}")

    return values

def load_known_wine_names(data_dir: str = "VectorDB/data/wine") -> set:
    wine_names = set()
    csv_files = glob(os.path.join(data_dir, "*.csv"))
    for file_path in csv_files:
        try:
            df = pd.read_csv(file_path)
            if "와인명" in df.columns:
                cleaned = df["와인명"].dropna().astype(str).map(normalize_name)
                wine_names.update(cleaned)
            if "와인 영문명" in df.columns:
                cleaned_eng = df["와인 영문명"].dropna().astype(str).map(normalize_name)
                wine_names.update(cleaned_eng)
        except Exception as e:
            print(f"[⚠️] CSV 로드 실패: {file_path} → {e}")
    return wine_names

def load_known_grape_names(data_dir: str = "VectorDB/data/grape") -> set:
    return load_column_values_from_csv(data_dir, "포도품종")

def load_known_region_names(data_dir: str = "VectorDB/data/region") -> set:
    return load_column_values_from_csv(data_dir, "생산지역")

def load_known_producer_names(data_dir: str = "VectorDB/data/producer") -> set:
    return load_column_values_from_csv(data_dir, "생산자")

# ✅ 공개 API: 최초 1회만 로드 후 재사용
def get_known_entities() -> dict:
    if _entity_cache:
        return _entity_cache  # 이미 로드된 경우 재사용

    wine = load_known_wine_names()
    grape = load_known_grape_names()
    region = load_known_region_names()
    producer = load_known_producer_names()

    _entity_cache.update({
        "wine": wine,
        "grape": grape,
        "region": region,
        "producer": producer
    })

    print(f"[🔍] 로드된 와인명 개수: {len(wine)}")
    print(f"[🔍] 로드된 포도 품종 개수: {len(grape)}")
    print(f"[🔍] 로드된 생산지역 개수: {len(region)}")
    print(f"[🔍] 로드된 생산자 개수: {len(producer)}")

    return _entity_cache

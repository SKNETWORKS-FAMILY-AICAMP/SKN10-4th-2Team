import os, re
import pandas as pd
from glob import glob

def normalize_name(name: str) -> str:
    # 쉼표 제거, 다중 공백 정리, 소문자 통일
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

def load_known_producer_names(data_dir: str = "VectorDB/data/producer") -> set:
    return load_column_values_from_csv(data_dir, "생산자")


def load_known_region_names(data_dir: str = "VectorDB/data/region") -> set:
    return load_column_values_from_csv(data_dir, "생산지역")


def load_known_grape_names(data_dir: str = "VectorDB/data/grape") -> set:
    return load_column_values_from_csv(data_dir, "포도품종")

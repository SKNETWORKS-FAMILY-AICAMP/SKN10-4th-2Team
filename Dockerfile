FROM python:3.12

# ✅ 코드 및 파일 복사
COPY ./django_server /app
COPY ./entrypoint.sh /app/entrypoint.sh
COPY ./models /models
COPY ./Modelfile /Modelfile

# ✅ 작업 디렉토리 설정
WORKDIR /app

# ✅ Ollama 및 시스템 패키지 설치
RUN apt-get update && \
    apt-get install -y curl gnupg2 && \
    curl -fsSL https://ollama.com/install.sh | sh && \
    apt-get clean

# ✅ Python 패키지 설치
RUN pip install --upgrade pip && \
    pip install -r /app/requirements.txt

# ✅ entrypoint 실행 권한 부여
RUN chmod +x /app/entrypoint.sh

ENTRYPOINT [ "sh", "/app/entrypoint.sh" ]

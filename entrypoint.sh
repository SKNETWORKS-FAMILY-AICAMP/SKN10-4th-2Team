#!/bin/sh

# 1. Ollama 서버 실행 (백그라운드)
ollama serve &

# 2. 서버가 뜰 시간을 잠시 대기
sleep 5

# 3. .gguf 모델 파일을 Ollama 내부 경로로 복사
mkdir -p /root/.ollama/models/gemma3-wine
cp /models/gemma3-Wine-Guid.Q8_0.gguf /root/.ollama/models/gemma3-wine/model.gguf

# 4. 모델 등록 (이미 등록되어 있으면 무시됨)
ollama create gemma3-wine -f /Modelfile || echo "모델이 이미 존재합니다."

# 5. Django 초기화
python manage.py makemigrations --no-input
python manage.py migrate --no-input
python manage.py collectstatic --no-input

# 6. 슈퍼유저 자동 생성
DJANGO_SUPERUSER_PASSWORD=$SUPER_USER_PASSWORD \
python manage.py createsuperuser \
--username $SUPER_USER_NAME \
--email $SUPER_USER_EMAIL \
--noinput

# 7. Gunicorn 실행
gunicorn config.wsgi:application --bind 0.0.0.0:8000 --timeout 300

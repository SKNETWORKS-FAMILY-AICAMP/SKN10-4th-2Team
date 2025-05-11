#!/bin/sh

# 1. Ollama 서버 실행 (백그라운드)
ollama serve &

# 2. 서버가 뜰 시간을 잠시 대기
sleep 5

# 3. 모델 파일 다운로드 (존재하지 않으면)
mkdir -p /models
if [ ! -f /models/gemma3-Wine-Guid.Q8_0.gguf ]; then
    echo "모델 파일 다운로드 중..."
    curl -L -o /models/gemma3-Wine-Guid.Q8_0.gguf \
    https://huggingface.co/Minkyeong2/gemma3-Wine-Guide-gguf/resolve/main/gemma3-Wine-Guid.Q8_0.gguf
fi

# 4. Ollama 모델 경로로 복사
mkdir -p /root/.ollama/models/gemma3-wine
cp /models/gemma3-Wine-Guid.Q8_0.gguf /root/.ollama/models/gemma3-wine/model.gguf

# 5. 모델 등록
ollama create gemma3-wine -f /Modelfile || echo "모델이 이미 존재합니다."

# 6. Django 초기화
python manage.py makemigrations --no-input
python manage.py migrate --no-input
python manage.py collectstatic --no-input

# 7. 슈퍼유저 자동 생성
DJANGO_SUPERUSER_PASSWORD=$SUPER_USER_PASSWORD \
python manage.py createsuperuser \
--username $SUPER_USER_NAME \
--email $SUPER_USER_EMAIL \
--noinput

# 8. Gunicorn 실행
gunicorn config.wsgi:application --bind 0.0.0.0:8000 --timeout 300

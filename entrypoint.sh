#!/bin/sh

# 1. Ollama 서버 실행 (백그라운드)
ollama serve &

# 2. 서버가 뜰 시간을 잠시 대기
sleep 5

# 3. 모델 다운로드
mkdir -p /models
if [ ! -f /models/gemma3-Wine-Guid.Q8_0.gguf ]; then
    echo "[💾] 모델 다운로드 시작..."
    curl -L -o /models/gemma3-Wine-Guid.Q8_0.gguf \
    https://huggingface.co/Minkyeong2/gemma3-Wine-Guide-gguf/resolve/main/gemma3-Wine-Guid.Q8_0.gguf
fi

# 4. 모델 복사
mkdir -p /root/.ollama/models/gemma3-wine
cp /models/gemma3-Wine-Guid.Q8_0.gguf /root/.ollama/models/gemma3-wine/model.gguf

# 5. 모델 등록
echo "[📦] 모델 등록 중..."
ollama create gemma3-wine -f /Modelfile || echo "[⚠️] 모델 이미 등록됨"

# 6. 모델 준비 대기
echo "[⏳] 모델 준비 상태 확인 중..."
until curl -s http://localhost:11434/api/tags | grep -q gemma3-wine; do
    sleep 1
done
echo "[✅] 모델 준비 완료"

# 7. Django 초기화
python manage.py makemigrations --no-input
python manage.py migrate --no-input
python manage.py collectstatic --no-input

# 8. 슈퍼유저 자동 생성
DJANGO_SUPERUSER_PASSWORD=$SUPER_USER_PASSWORD \
python manage.py createsuperuser \
--username $SUPER_USER_NAME \
--email $SUPER_USER_EMAIL \
--noinput || echo "[⚠️] 슈퍼유저 이미 존재함"

# 9. Gunicorn 실행
gunicorn config.wsgi:application --bind 0.0.0.0:8000 --timeout 300

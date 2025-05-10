from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import json

# RAG 파이프라인 모듈 임포트
from .rag.pipeline import get_final_answer

def index(request):
    return render(request, 'chatbot/main.html')

@login_required(login_url='/user/login-register/')
def chat(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_input = data.get('message', '').strip()

        chat_history = request.session.get('chat_history', [])

        try:
            # ✅ 항상 history 포함 파이프라인 실행
            final_answer = get_final_answer(user_input, history=chat_history)

            chat_history.append({"role": "user", "content": user_input})
            chat_history.append({"role": "assistant", "content": final_answer})
            request.session['chat_history'] = chat_history

            return JsonResponse({'response': final_answer})
        except Exception as e:
            print("[❌] 오류:", e)
            return JsonResponse({'response': "답변 생성 중 오류가 발생했습니다."})

    return render(request, 'chatbot/chatbot.html')

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import CustomUser
from django.contrib.auth import authenticate, login, logout

# 로그아웃
def user_logout(request):
    # 로그아웃 요청
    logout(request)
    return redirect('user-login-register')

# 로그인 및 회원가입
def login_required(request):
    # 이미 로그인된 상태면 챗봇 페이지로
    if request.user.is_authenticated:
        return redirect('chatbot-index')

    # POST 요청이면 로그인 시도
    if request.method == 'POST' and request.POST.get('action') == 'signin':
        username = request.POST.get('username').strip()
        password = request.POST.get('password').strip()

        user = authenticate(request, username=username, password=password)
        if not user:
            messages.error(request, '아이디 또는 비밀번호가 틀렸습니다.')
            return redirect('user-login-register')
        login(request, user)
        return redirect('chatbot-index')

    # POST 요청이면 회원가입 시도
    if request.method == 'POST' and request.POST.get('action') == 'signup':
        username = request.POST.get('username').strip()
        password = request.POST.get('password').strip()
        email    = request.POST.get('email').strip()

        if not username or not password or not email:
            messages.error(request, '아이디, 이메일, 비밀번호를 입력하세요.')
            return redirect('user-login-register')

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, '이미 존재하는 사용자입니다.')
            return redirect('user-login-register')

        try:
            new_user = CustomUser.objects.create_user(username=username, password=password, email=email)
            new_user.save()
            messages.success(request, '회원가입이 완료되었습니다.')
        except Exception:
            messages.error(request, '회원가입에 실패했습니다.')
        return redirect('user-login-register')
            
    return render(request, 'user/login_register.html')

def register(request):
    return render(request, 'user/register.html')

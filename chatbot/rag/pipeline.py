import subprocess
import re
from .classification import classify_category
from .multiquery import generate_multi_queries
from .relevance_check import is_relevant
from .internal_rag import search_documents, generate_answer_with_docs
from .external_rag import tavily_search

def strip_badge(text: str) -> str:
    """
    이미 붙은 badge를 제거하는 후처리 함수 (중복 제거 방지)
    """
    return re.sub(r"<br\s*/?><br\s*/?><span class=['\"]?badge['\"]?>.*?</span>", "", text, flags=re.IGNORECASE)

def sllm_answer(prompt: str, category: str = None, history: list = None) -> str:
    """
    로컬 Ollama에서 gemma3-wine:latest 모델을 사용하여 응답 생성.
    이전 히스토리와 함께 자연스럽고 전문적인 와인 관련 응답 생성.
    """
    system_prompt = (
        """
        당신은 와인 분야에 특화된 전문적인 AI 큐레이터입니다. 
        사용자 질문에 대해 다음의 정보를 바탕으로 정확하고 친절하게 답변해주세요.

        - 반드시 "HTML 형식"으로 출력해주세요.
        - 핵심 요약 → 목록(`<ul><li>`) → 본문 설명 순으로 구성합니다.
        - 줄바꿈(`<br>`)과 강조(`<b>`, `<i>`) 태그를 적절히 사용하여 가독성을 높입니다.
        - 사용자 질문과 직접적으로 관련된 정보만 추려서 사용하세요.
        - 답을 모를 경우 "정확한 정보가 없습니다."라고 솔직하게 말해주세요.
        - "저는 AI입니다"라는 문구는 절대 포함하지 마세요.

        예시 형식:
        요약 문장<br>
        <ul>
        <li>핵심 포인트 1</li>
        <li>핵심 포인트 2</li>
        </ul>
        <br><br>본문 설명 문단<br><br>

        질문: {question}
        """
    )

    # 시스템 프롬프트와 유저 입력을 하나로 연결
    full_prompt = f"{system_prompt}\n\n{prompt}"

    try:
        # Ollama 명령어로 subprocess 실행
        result = subprocess.run(
            ["ollama", "run", "gemma3-wine:latest"],
            input=full_prompt.encode(),  # 프롬프트를 바이트로 변환하여 전달
            stdout=subprocess.PIPE,      # 표준 출력을 캡처
            stderr=subprocess.PIPE,      # 오류 출력을 캡처
            timeout=300                    # 타임아웃 설정 (300초)
        )
        
        # 오류가 발생하면 stderr를 출력
        if result.returncode != 0:
            return f"[오류] Ollama 실행 실패: {result.stderr.decode()}"

        # 표준 출력에서 응답 내용 추출
        return result.stdout.decode()

    except Exception as e:
        return f"[오류] subprocess 실행 중 예외 발생: {e}"




def get_final_answer(user_question: str, history: list) -> str:
    """
    전체 질문 흐름을 처리하는 메인 파이프라인 함수.
    카테고리에 따라 분기하며,
    내부 문서 검색, LLM 서브질문, 외부 검색 등을 단계적으로 활용.
    """
    print(f"[💬] 질문: {user_question}")
    category = classify_category(user_question)
    print(f"[💬] 분류된 카테고리: {category}")

    answer = ""
    badge = ""

    if category == "greeting":
        answer = sllm_answer(user_question, category, history)
        badge = "🧠 LLM"

    elif category == "etc":
        temp = sllm_answer(user_question, category, history)
        if is_relevant(user_question, temp):
            answer, badge = temp, "🧠 LLM"
        else:
            docs = search_documents("wine", user_question)
            if docs:
                temp = generate_answer_with_docs(user_question, docs)
                if is_relevant(user_question, temp):
                    answer, badge = temp, "📁 내부 문서"
        if not answer:
            answer = tavily_search(user_question)
            badge = "🌐 외부 문서"

    else:  # wine, grape, region, producer
        sub_questions = generate_multi_queries(user_question)
        print(f"[💬] 생성된 서브 질문들: {sub_questions}")

        docs = search_documents(category, user_question)
        if docs:
            temp = generate_answer_with_docs(user_question, docs)
            if is_relevant(user_question, temp):
                answer, badge = temp, "📁 내부 문서"

        if not answer:
            for sub_q in sub_questions:
                temp = sllm_answer(sub_q, category, history)
                print(f"[💬] '{sub_q}' → 응답: {temp[:60]}...")
                if is_relevant(user_question, temp):
                    answer, badge = temp, "🧠 LLM"
                    break

        if not answer:
            answer = tavily_search(user_question)
            badge = "🌐 외부 문서"

    cleaned = strip_badge(answer.strip())
    return cleaned + f"<br><br><span class='badge'>{badge}</span>"

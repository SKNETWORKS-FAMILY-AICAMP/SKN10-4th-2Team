from .classification import classify_category
from .multiquery import generate_multi_queries
from .answer_llm import llm_answer
from .relevance_check import is_relevant
from .internal_rag import search_documents, generate_answer_with_docs
from .external_rag import tavily_search

def get_final_answer(user_question: str, history: list) -> str:
    print(f"[💬] 질문: {user_question}")
    category = classify_category(user_question)
    print(f"[💬] 분류된 카테고리: {category}")

    def format_answer(answer: str, badge: str):
        return answer.strip() + f"<br><br><span class='badge'>{badge}</span>"

    # 1. 인사
    if category == "greeting":
        return format_answer(llm_answer(user_question, category, history), "🧠 LLM")

    # 2. 일반 질문 처리
    if category == 'etc':
        answer = llm_answer(user_question, category, history)
        print(f"[💬] 응답: {answer[:60]}...")
        if is_relevant(user_question, answer):
            return format_answer(answer, "🧠 LLM")

        docs = search_documents("wine", user_question)
        if docs:
            rag_answer = generate_answer_with_docs(user_question, docs)
            if is_relevant(user_question, rag_answer):
                return format_answer(rag_answer, "📁 내부 문서")

        return format_answer(tavily_search(user_question), "🌐 외부 문서")

    # 3. wine/grape/region/producer의 경우
    sub_questions = generate_multi_queries(user_question)
    print(f"[💬] 생성된 서브 질문들: {sub_questions}")

    llm_sub_answers = []

    for sub_q in sub_questions:
        sub_answer = llm_answer(sub_q, category, history)
        print(f"[💬] '{sub_q}' → 응답: {sub_answer[:100]}...")
        if is_relevant(user_question, sub_answer):
            llm_sub_answers.append(sub_answer)

    # ✅ RAG 검색은 반드시 시도
    docs = search_documents(category, user_question)
    if docs:
        rag_answer = generate_answer_with_docs(user_question, docs)
        if is_relevant(user_question, rag_answer):
            return format_answer(rag_answer, "📁 내부 문서")

    # ✅ 내부 문서 없을 경우에만 서브 질문 기반 LLM 응답 중 가장 관련성 높은 것 선택
    if llm_sub_answers:
        return format_answer(llm_sub_answers[0], "🧠 LLM")

    # ✅ 최후의 외부 검색
    return format_answer(tavily_search(user_question), "🌐 외부 문서")

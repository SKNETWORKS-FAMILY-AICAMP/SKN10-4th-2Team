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

    answer = ""
    badge = ""

    # 1. 인사
    if category == "greeting":
        answer = llm_answer(user_question, category, history)
        badge = "🧠 LLM"

    # 2. etc → LLM → 내부 문서 → 외부 검색
    elif category == "etc":
        temp = llm_answer(user_question, category, history)
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

    # 3. wine/grape/region/producer → 내부 문서 → LLM 서브 → 외부
    else:
        sub_questions = generate_multi_queries(user_question)
        print(f"[💬] 생성된 서브 질문들: {sub_questions}")

        docs = search_documents(category, user_question)
        if docs:
            temp = generate_answer_with_docs(user_question, docs)
            if is_relevant(user_question, temp):
                answer, badge = temp, "📁 내부 문서"

        if not answer:
            for sub_q in sub_questions:
                temp = llm_answer(sub_q, category, history)
                if is_relevant(user_question, temp):
                    answer, badge = temp, "🧠 LLM"
                    break

        if not answer:
            answer = tavily_search(user_question)
            badge = "🌐 외부 문서"

    # ✅ 최종 응답에만 뱃지를 단 한 번만 붙인다
    return answer.strip() + f"<br><br><span class='badge'>{badge}</span>"

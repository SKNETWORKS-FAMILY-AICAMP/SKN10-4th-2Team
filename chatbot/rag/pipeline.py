from .classification import classify_category
from .multiquery import generate_multi_queries
from .answer_llm import llm_answer
from .relevance_check import is_relevant
from .internal_rag import search_documents, generate_answer_with_docs
from .external_rag import tavily_search

def get_final_answer(user_question: str, history: list) -> str:
    """
    대화 이력을 포함한 전체 RAG 파이프라인.
    항상 history를 기준으로 LLM 답변 생성.
    """
    print(f"[💬] 질문: {user_question}")
    
    category = classify_category(user_question)
    print(f"[💬] 분류된 카테고리: {category}")

    if category == "greeting":
        answer = llm_answer(user_question, category=category, history=history)
        return answer.strip() + "<br><span class='badge'>🧠 LLM</span>"

    if category == 'etc':
        answer = llm_answer(user_question, category=category, history=history)
        print(f"[💬] 응답: {answer[:60]}...")
        if is_relevant(user_question, answer):
            return answer.strip() + "<br><span class='badge'>🧠 LLM</span>"

        docs = search_documents("wine", user_question)
        if docs:
            rag_answer = generate_answer_with_docs(user_question, docs)
            if is_relevant(user_question, rag_answer):
                return rag_answer.strip() + "<br><span class='badge'>📁 내부 문서</span>"

        external_answer = tavily_search(user_question)
        return external_answer.strip() + "<br><span class='badge'>🌐 외부 문서</span>"

    sub_questions = generate_multi_queries(user_question)
    print(f"[💬] 생성된 서브 질문들: {sub_questions}")

    for sub_q in sub_questions:
        answer = llm_answer(sub_q, category=category, history=history)
        print(f"[💬] '{sub_q}' → 응답: {answer[:60]}...")
        if is_relevant(user_question, answer):
            return answer.strip() + "<br><span class='badge'>🧠 LLM</span>"

    docs = search_documents(category, user_question)
    if docs:
        rag_answer = generate_answer_with_docs(user_question, docs)
        if is_relevant(user_question, rag_answer):
            return rag_answer.strip() + "<br><span class='badge'>📁 내부 문서</span>"

    external_answer = tavily_search(user_question)
    return external_answer.strip() + "<br><span class='badge'>🌐 외부 문서</span>"

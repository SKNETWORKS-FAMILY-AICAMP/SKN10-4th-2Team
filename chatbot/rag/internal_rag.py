import os
from langchain_community.vectorstores import FAISS
from langchain_community.cross_encoders import HuggingFaceCrossEncoder
from langchain.retrievers.document_compressors import CrossEncoderReranker
from langchain.retrievers import ContextualCompressionRetriever
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document

from .answer_llm import llm_answer

def load_faiss_db(category: str):
    """
    카테고리에 맞는 FAISS vector DB 불러오기
    """
    db_path = f"VectorDB/faiss_db/{category}"
    return FAISS.load_local(db_path, embeddings=OpenAIEmbeddings(model="text-embedding-3-small"), index_name=category, allow_dangerous_deserialization=True)

def search_documents(category: str, query: str, top_n: int = 3) -> list[Document]:
    """
    FAISS + CrossEncoder reranker를 이용해 유사 문서 검색 및 재정렬
    """
    db = load_faiss_db(category)
    cross_encoder = HuggingFaceCrossEncoder(model_name="BAAI/bge-reranker-v2-m3")
    reranker = CrossEncoderReranker(model=cross_encoder, top_n=top_n)
    retriever = ContextualCompressionRetriever(base_compressor=reranker, base_retriever=db.as_retriever())
    return retriever.get_relevant_documents(query)

def generate_answer_with_docs(query: str, documents: list[Document]) -> str:
    context = ""
    sources = []

    for doc in documents:
        context += f"{doc.page_content}\n\n"
        url = doc.metadata.get("url")
        if url and url not in sources:
            sources.append(url)

    prompt = f"""
    당신은 와인 분야에 특화된 전문 큐레이터입니다.  
    아래는 신뢰할 수 있는 내부 데이터베이스에서 추출한 자료입니다:

    {context}

    이 자료를 바탕으로 사용자 질문에 대해 다음 조건을 충실히 반영해 정리해 주세요:

    1. **반드시 위의 문서(context)에 포함된 정보만 사용**하세요.  
    2. 내용을 항목별로 요약 정리하되, **빠짐없이 정확하게** 구성하세요.  
    3. 출력은 HTML 형식으로 하며, 다음과 같은 구성 순서를 지킵니다:
    - <b>요약:</b> 한두 문장으로 핵심 정리 후 `<br><br>` 줄바꿈
    - `<ul><li>` 형식으로 주요 특징을 나열
    - 그 아래에 문단 형태로 부가 설명을 덧붙이세요.
    4. 불필요한 수식어, 감성 표현, 문학적 묘사는 피하고 **정보 중심의 간결하고 명확한 설명**을 작성하세요.
    5. 내용이 없거나 불충분한 항목은 생략하지 말고, 가능한 범위 내에서 정리하세요.

    질문: {query}
    """

    answer = llm_answer(prompt)

    # ✅ 하나의 대표 URL만 보여주기
    if sources:
        source_url = sources[0]  # 가장 관련성 높은 하나만 사용
        source_text = f"<br><br><a href='{source_url}' target='_blank'>🔗 참고 링크</a>"
    else:
        source_text = ""

    return answer.strip() + source_text




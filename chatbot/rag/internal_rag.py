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
    """
    검색된 문서들을 기반으로 Gemma 모델로 답변 생성.
    관련 문서 출처 URL이 있으면 가장 관련성 높은 것 하나만 함께 포함.
    """
    context = ""
    first_url = None

    for i, doc in enumerate(documents):
        context += f"{doc.page_content}\n\n"
        if i == 0 and doc.metadata.get("url"):
            first_url = doc.metadata["url"]

    prompt = f"""당신은 와인 소믈리에입니다.

    다음은 와인 관련 참고 문서들이야:

    {context}

    위 정보를 참고하여 사용자 질문에 대해 정확하고 신뢰감 있게 답변해줘.
    질문: {query}
    """

    answer = llm_answer(prompt)

    if first_url:
        answer += f"\n\n📎 참고 링크:\n- {first_url}"

    return answer



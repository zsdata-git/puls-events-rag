import faiss
import mistralai
from langchain_community.vectorstores import FAISS


def test_imports():
    assert faiss is not None
    assert mistralai is not None
    assert FAISS is not None
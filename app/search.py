from elasticsearch import Elasticsearch
es = Elasticsearch("http://localhost:9200")

def index_document(index: str, doc_id: str, document: dict):
    es.index(index=index, id=doc_id, document=document)

def search_documents(index: str, query: str):
    response = es.search(index=index, query={"match": {"content": query}})
    return response['hits']['hits']

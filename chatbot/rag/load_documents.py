from PyPDF2 import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import chromadb

def get_vectordb(file_name='policy.pdf'):
    file_obj = PdfReader(file_name)
    text = ''
    for p in file_obj.pages:
        text = text + ' ' + p.extract_text()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size = 500, chunk_overlap=50)
    chunks = text_splitter.split_text(text)
    client = chromadb.Client()
    vectordb = client.get_or_create_collection(name='android_vdb')
    vectordb.add(
        ids = ['id_'+str(i) for i in range(len(chunks))],
        documents=chunks)
    return vectordb
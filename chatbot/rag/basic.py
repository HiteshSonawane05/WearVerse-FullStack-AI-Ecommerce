from PyPDF2 import PdfReader
from langchain_groq import ChatGroq
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
import chromadb
import os

load_dotenv()

# Read PDF
file_obj = PdfReader(os.path.join(os.path.dirname(__file__), 'policy.pdf'))

# Extract text
text = ''
for p in file_obj.pages:
    text = text + ' ' + p.extract_text()

# Split into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=75)
chunks = text_splitter.split_text(text)

# Vector DB
client = chromadb.Client()
collection = client.get_or_create_collection(name='policy')
collection.add(
    ids=['id_'+str(i) for i in range(len(chunks))],
    documents=chunks)

# LLM
llm = ChatGroq(model='llama-3.3-70b-versatile')

def get_rag_response(question):
    search_result = collection.query(query_texts=[question], n_results=1)
    
    prompt = f'''You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise.
Question: {question}
Context: {search_result['documents'][0]}'''
    
    response = llm.invoke(prompt)
    return response.content



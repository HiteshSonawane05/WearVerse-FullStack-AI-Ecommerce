from model import get_llm
from load_documents import get_vectordb
collection = get_vectordb()
llm = get_llm()
def generate_answer(question,history):
    search_results = collection.query(query_texts=[question], n_results=1)
    prompt = f'''You are an assistant for question-answering tasks. Use the following pieces of retrieved context and previous chat history to answer the question. If you don't know the answer, just say that you don't know. Use two sentences maximum and keep the answer concise.
    Question: {question} 
    Context: {search_results['documents'][0]}
    history:{history} '''
    response = llm.invoke(prompt)
    return response.content, search_results['documents'][0]

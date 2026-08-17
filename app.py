import streamlit as st
import tempfile
import os

try:
    from langchain.prompts import PromptTemplate
except ModuleNotFoundError:
    from langchain_core.prompts import PromptTemplate

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.llms import Ollama

try:
    from langchain.chains import RetrievalQA
except ModuleNotFoundError:
    from langchain_classic.chains import RetrievalQA

st.set_page_config(page_title="RAG Local", page_icon="🔐")
st.title("Demo RAG 100% Local 🔐")
st.write("Nenhum dado sai da sua máquina.")

# 1. Upload do Arquivo
uploaded_file = st.file_uploader("Faça upload de um PDF", type="pdf")

if uploaded_file:
    # Salvando o arquivo temporariamente para o PyPDFLoader ler
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.getvalue())
        tmp_path = tmp.name
    
    with st.spinner("Lendo, cortando e vetorizando o documento..."):
        # 2. Leitura e Divisão do Texto
        loader = PyPDFLoader(tmp_path)
        docs = loader.load()
        
        # Corta o texto em pedaços pequenos para a IA não se perder
        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        chunks = splitter.split_documents(docs)
        
        # 3. Embeddings (Transforma texto em números - Roda 100% local)
        # Na primeira execução, ele vai baixar um modelo pequeno (~80MB) automaticamente
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        
        # 4. Banco de Dados Vetorial (ChromaDB em memória)
        vector_store = Chroma.from_documents(chunks, embeddings)
        
    st.success("Documento processado com sucesso! O sistema já estudou o texto.")
    
    # 5. Interface de Chat
    question = st.text_input("Faça uma pergunta sobre o documento:")
    
    if question:
        with st.spinner("Buscando no texto e gerando resposta..."):
            llm = Ollama(model="qwen2.5:3b") # Ou o modelo que você escolheu
            
            # 1. Aqui criamos a regra de ferro (System Prompt)
            template_regras = """Você é um assistente focado em análise de documentos.
            Responda à pergunta de forma MUITO curta, direta e objetiva.
            Use APENAS os fatos fornecidos no contexto abaixo.
            Se a resposta não estiver no contexto, diga APENAS: "Não encontrei essa informação no documento".
            NÃO invente dados e NÃO puxe informações de fora.
            
            Contexto do Documento:
            {context}
            
            Pergunta do Usuário: 
            {question}
            
            Resposta:"""
            
            prompt_personalizado = PromptTemplate(
                template=template_regras, 
                input_variables=["context", "question"]
            )
            
            # 2. Conecta o banco de dados, a IA e o nosso Prompt
            qa_chain = RetrievalQA.from_chain_type(
                llm=llm,
                retriever=vector_store.as_retriever(search_kwargs={"k": 3}),
                chain_type_kwargs={"prompt": prompt_personalizado} # <--- A MÁGICA ACONTECE AQUI
            )
            
            resposta = qa_chain.invoke({"query": question})
            
            st.markdown("### Resposta:")
            st.info(resposta["result"])
            
    # Limpa o arquivo temporário
    os.remove(tmp_path)
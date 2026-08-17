\# Challenge Alura: Agente RAG 100% Local 🔐



\## Descrição Geral

Este projeto é um agente inteligente desenvolvido com Python e Streamlit que permite aos usuários fazer upload de arquivos PDF e realizar perguntas sobre o conteúdo do documento. O diferencial desta solução é ser 100% local, garantindo a privacidade dos dados ("Nenhum dado sai da sua máquina").



\## Arquitetura da Solução

A aplicação utiliza a arquitetura RAG (Retrieval-Augmented Generation) com as seguintes etapas:

1\. \*\*Ingestão de Dados:\*\* Leitura de arquivos PDF utilizando `PyPDFLoader`.

2\. \*\*Processamento:\*\* O texto é fatiado usando `RecursiveCharacterTextSplitter` para manter o contexto sem estourar o limite de tokens da IA.

3\. \*\*Vetorização (Embeddings):\*\* Os fragmentos de texto são convertidos em números usando o modelo `all-MiniLM-L6-v2` via HuggingFace.

4\. \*\*Armazenamento:\*\* Os vetores são salvos temporariamente em memória usando o ChromaDB.

5\. \*\*Geração de Resposta:\*\* O modelo `qwen2.5:3b` (rodando via Ollama) recebe o contexto recuperado pelo banco vetorial e formula uma resposta curta e objetiva.



\## Tecnologias e Ferramentas Utilizadas

\* \*\*Frontend:\*\* Streamlit

\* \*\*Orquestração de IA:\*\* LangChain

\* \*\*Embeddings:\*\* HuggingFace (`all-MiniLM-L6-v2`)

\* \*\*Banco de Dados Vetorial:\*\* ChromaDB

\* \*\*LLM (Large Language Model):\*\* Ollama (Modelo `qwen2.5:0.5b`)



\## Instruções para Executar o Projeto



\*\*Pré-requisitos:\*\*

1\. Instalar o \[Ollama](https://ollama.com/).

2\. No terminal, baixar o modelo utilizado na aplicação:

&#x20;  `ollama pull qwen2.5:0.5b`



\*\*Rodando a aplicação:\*\*

1\. Clone este repositório.

2\. Instale as dependências:

&#x20;  `pip install -r requirements.txt`

3\. Inicie o Streamlit:

&#x20;  `streamlit run app.py`



## Exemplos de Interação

Para testar estes exemplos na aplicação, faça o upload do arquivo `Política Interna de Trabalho e Benefícios - InovaTech.pdf` (disponível neste repositório).

**Cenário de Exemplo:** Upload de um PDF sobre "Política Interna de Trabalho e Benefícios - InovaTech"[cite: 2].

* **Pergunta do Usuário:** Quais são os dias obrigatórios no escritório?
* **Resposta do Agente:** Os colaboradores devem comparecer presencialmente ao escritório obrigatoriamente às terças e quintas-feiras[cite: 2].

* **Pergunta do Usuário:** Qual é o valor do auxílio home office e quando é pago?
* **Resposta do Agente:** O auxílio home office é de R$ 450,00 e cai na conta no dia 15 de cada mês[cite: 2].

* **Pergunta do Usuário:** Qual é a marca e modelo do notebook padrão da empresa?
* **Resposta do Agente:** O modelo padrão é o Dell Latitude 5420[cite: 2].

* **Pergunta do Usuário:** Como funciona o plano de saúde?
* **Resposta do Agente:** Não encontrei essa informação no documento.



## Evidência do Deploy na OCI

A aplicação foi implantada na Oracle Cloud Infrastructure (OCI) e está rodando em uma instância virtual.

**Link público de acesso:** http://163.176.178.81:8501/

![Print do App rodando na OCI]<img width="833" height="630" alt="image" src="https://github.com/user-attachments/assets/6b6587d6-150b-4d77-b852-891e43e1f4c7" />

import os
from dotenv import load_dotenv
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.tools.tavily_search import TavilySearchResults

load_dotenv()
os.environ["TAVILY_API_KEY"] = os.getenv("TAVILY_API_KEY")

def load_documents_from_folder(folder_path):
    all_docs = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            loader = TextLoader(os.path.join(folder_path, filename), encoding='utf-8')
            docs = loader.load()
            for doc in docs:
                doc.metadata['source'] = filename  # Track filename as source
            all_docs.extend(docs)
    return all_docs

documents = load_documents_from_folder("docs/")
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
docs = splitter.split_documents(documents)

embedding_model = OpenAIEmbeddings()
vectorstore = Chroma.from_documents(
    documents=docs,
    embedding=embedding_model,
    persist_directory="chroma_store"
)
vectorstore.persist()
retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

llm = ChatOpenAI(model_name="gpt-4", temperature=0)

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    return_source_documents=True
)

tavily_tool = TavilySearchResults(k=5)

def ask_with_tavily(query):
    results = tavily_tool.run(query)
    if not results:
        return "No relevant web results found."

    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template="""
Answer the question below using only the web results provided.

Web Results:
{context}

Question: {question}

Answer:
"""
    )

    context = "\n\n".join([r['content'] for r in results])
    chain = LLMChain(llm=llm, prompt=prompt)
    return chain.run(context=context, question=query)

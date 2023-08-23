import os, dotenv
import nest_asyncio
from langchain.document_loaders import WebBaseLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import Chroma
from langchain.prompts import ChatPromptTemplate
from links import urls
nest_asyncio.apply()
os.environ["OPENAI_API_KEY"] = dotenv.dotenv_values()["OPENAI_API_KEY"]


def chat_query(question: str):
    loader = WebBaseLoader(
       urls)

    data = loader.aload()
    text_spliter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200
    )

    docs = text_spliter.split_documents(data)
    print(docs)
    prompt = """You are chatting with a specialized AI 
    designed to assist with questions related to the Kazakh
    National Unified Test (ENT) and university admissions 
    in Kazakhstan. Please feel free to ask any questions related 
    to these topics, such as ENT questions, university admissions 
    procedures, or guidance on choosing a university or specialty. 
    If you have a different question, please note that I 
    cannot provide an answer.
    
    question:{question}
    """

    prompt_template = ChatPromptTemplate.from_template(prompt)

    question = prompt_template.format_messages(question=question)
    embeddings = OpenAIEmbeddings()
    docsearch = Chroma.from_documents(docs, embeddings)
    retriever = docsearch.as_retriever(search_kwargs={"k": 3})

    llm = ChatOpenAI(model_name="gpt-3.5-turbo")
    qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)

    response = qa(question[0].content)
    return response["result"]



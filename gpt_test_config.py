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

def test_query(my_text: str):

    loader = WebBaseLoader(
        urls
    )

    data = loader.aload()
    text_spliter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200
    )

    docs = text_spliter.split_documents(data)

    prompt = """you are an expert in creating tests. I am giving you a text for constructing questions and with an answer. generate questions without asking unnecessary questions, 
    just generate questions in json format based on the given text
    for example
    "1. In 1768, Captain James Cook went to explore which ocean?
    A. Pacific Ocean
    B. Atlantic Ocean
    C. Indian Ocean
    D. Arctic Ocean
    
    the correct answer is: A
    "
    my text:{my_text}
        """

    prompt_template = ChatPromptTemplate.from_template(prompt)
    my_text = prompt_template.format_messages(my_text=my_text)
    embeddings = OpenAIEmbeddings()
    docsearch = Chroma.from_documents(docs, embeddings)
    retriever = docsearch.as_retriever(search_kwargs={"k": 3})
    llm = ChatOpenAI(model_name="gpt-3.5-turbo-16k-0613")
    qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)
    response = qa(my_text[0].content)
    return response["result"]
# print(test_query("Biology definition: Anatomy is the study of the structure of the body of an organism. It is the branch of biology that focuses on the bodily structure of living things. It is subdivided into two: (1) gross anatomy (or macroscopic anatomy) and (2) microscopic anatomy."))

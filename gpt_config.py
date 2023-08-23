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
        urls
    )

    data = loader.aload()
    text_spliter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200
    )

    docs = text_spliter.split_documents(data)
    prompt = """you are an expert on the issues of unified national testing and admission to universities in 
    Kazakhstan. Please do not hesitate to ask any questions related to these topics, university admission procedures 
    or recommendations for choosing a university or specialty, as well as preparing for the UNT. if the questions are 
    not about these topics, just answer I'm sorry, I do not know the answer to your question.
    вы являетесь экспертом по вопросам о едином национальном тестировании и о поступлении
    в университеты Казахстана. Пожалуйста, не стесняйтесь задавать любые вопросы, связанные
    с этими темами,
    процедурами поступления в университет или рекомендациями по выбору университета или специальности,
    а также по подготовке к ЕНТ. если задает не касательно этих тем просто ответь простите я не знаю ответ на ваш вопрос
        
    question:{question}
    """

    prompt_template = ChatPromptTemplate.from_template(prompt)

    question = prompt_template.format_messages(question=question)

    embeddings = OpenAIEmbeddings()
    docsearch = Chroma.from_documents(docs, embeddings)
    retriever = docsearch.as_retriever(search_kwargs={"k": 3})

    llm = ChatOpenAI(model_name="gpt-3.5-turbo-16k-0613")
    qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)

    response = qa(question[0].content)
    return response["result"]

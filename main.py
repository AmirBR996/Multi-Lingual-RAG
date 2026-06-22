from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from googletrans import Translator
from translator import preprocess_query
import ntr
from dotenv import load_dotenv

load_dotenv()

translator = Translator()

embedding = HuggingFaceEmbeddings(
    model_name="intfloat/multilingual-e5-base"
)

loader = TextLoader("output.txt", encoding="utf-8")
docs = loader.load()

splitter = RecursiveCharacterTextSplitter(
    chunk_size=600,
    chunk_overlap=50
)
chunks = splitter.split_documents(docs)

vector_store = FAISS.from_documents(chunks, embedding)

retriever = vector_store.as_retriever(
    search_type="mmr",
    search_kwargs={"k": 5, "lambda_mult": 0.9}
)

llm = ChatGroq(
    model="llama-3.3-70b-versatile"
)

prompt = PromptTemplate(
    template="""
तपाईंले दिइएको सन्दर्भ प्रयोग गरेर मात्र उत्तर दिनुहोस्।
यदि उत्तर सन्दर्भमा छैन भने "मलाई थाहा छैन" भन्नुहोस्।
सन्दर्भ:
{context}
प्रश्न:
{question}
उत्तर नेपाली भाषामा दिनुहोस्।
""",
    input_variables=["context", "question"]
)

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

chain = (
    {
        "context": retriever | format_docs,
        "question": RunnablePassthrough(),
    }
    | prompt | llm | StrOutputParser()
)

def chat(user_message):
    query, original_lang = preprocess_query(user_message)
    result = chain.invoke(query)
    answer = result

    if original_lang == "en":
        return translator.translate(
            answer,
            src="ne",
            dest="en"
        ).text
    elif original_lang == "roman":
        return ntr.nep_to_rom(answer)

    return answer
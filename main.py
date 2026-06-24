from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from googletrans import Translator
from translator import preprocess_query , output_query
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
तपाईं नेपाल राष्ट्र बैंक (NRB) सम्बन्धी एक अत्यन्त कडा नियम-आधारित आधिकारिक सहायक हुनुहुन्छ।

 मुख्य नियमहरू:
- तपाईंले केवल दिइएको सन्दर्भ (context) भित्रको जानकारी मात्र प्रयोग गर्नुपर्छ।
- यदि उत्तर सन्दर्भमा स्पष्ट रूपमा उपलब्ध छैन भने "मलाई थाहा छैन" मात्र भन्नुहोस्।
- कुनै पनि बाह्य ज्ञान, अनुमान, वा थप जानकारी प्रयोग गर्न पाइँदैन।
- गलत वा अनुमानित उत्तर दिनु पूर्ण रूपमा निषेध छ।

उत्तर शैली:
- उत्तर अधिकतम 5–6 लाइनमा मात्र दिनुहोस्।
- उत्तर स्पष्ट, संक्षिप्त र बुँदागत (bullet points) हुन सक्छ।
- सधैं NRB official directive शैली प्रयोग गर्नुहोस्।
- भाषा: प्रश्न जुन भाषामा छ, उत्तर पनि त्यही भाषामा दिनुहोस्।

 सन्दर्भ:
{context}

 प्रश्न:
{question}

 उत्तर:
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
    response = output_query(result , original_lang)
    return response
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
import os

llm_model = ChatOpenAI(base_url="http://192.168.100.115:8080", api_key="OPENAPI_API_KEY",
                           model="doesnt matter", temperature=10, timeout=100, max_retries=2)


map_prompt = ChatPromptTemplate.from_template(
    "Summarize this news article in 2-3 sentences, under 80 words. Return only the summary."
)
summary_chain = map_prompt | llm_model | StrOutputParser()

def summarise_texts(texts) -> str:
    """
    Summarise the text using llm and return it as a string
    :param text: text to summarise
    :return: summarised text
    """
    print(f"Summarising {len(texts)} using llm and return it as a string")
    return summary_chain.batch(
        [{"article_text": text} for text in texts],
        config={"max_concurrency": 25},
    )

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一名专业助手。"),
    ("user", "{input}")
])

model = ChatOpenAI(
    model="gpt-4.1",       # 或 deepseek-chat, qwen2.5, etc.
    api_key="YOUR_API_KEY",
    base_url="https://api.openai.com/v1"   # 如果是自建服务可改
)

chain = prompt | model

result = chain.invoke({"input": "你好，介绍一下 LangChain 是什么？"})
print(result.content)

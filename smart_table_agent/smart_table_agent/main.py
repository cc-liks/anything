
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

llm = ChatOpenAI(model_name="gpt-5-mini", temperature=0)

prompt = PromptTemplate(
    input_variables=["query_result"],
    template="根据下面的数据分析，帮我写一个总结：\n{query_result}"
)

chain = LLMChain(llm=llm, prompt=prompt)

# 把 LAMIndex 查询结果输入 LangChain
query_result = df_index.query("计算每列的平均值")
summary = chain.run(query_result)
print(summary)

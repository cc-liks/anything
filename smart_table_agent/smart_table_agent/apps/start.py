from smart_table_agent.file_processing.file_manager import FileManager
from smart_table_agent.models_manager.model_manager import ModelManager


class SmartTableAgent:

    def __init__(self):
        self.model_manager = ModelManager()
        self.file_manager = FileManager()
        self._init_info()

    def _init_info(self):
        self.model_manager.register_model("test_model", "DeepSeek")

    def run(self):
        pass


# # -----------------------------
# # 1. 读取本地文件
# # -----------------------------
# def read_file(path):
#     with open(path, "r", encoding="utf-8") as f:
#         return f.read()
#
#
# # -----------------------------
# # 2. 文本切分
# # -----------------------------
# def split_text(text, chunk_size=400):
#     chunks = []
#     start = 0
#     while start < len(text):
#         end = min(start + chunk_size, len(text))
#         chunks.append(text[start:end])
#         start = end
#     return chunks
#
#
# # -----------------------------
# # 3. 构建 Chroma 向量库
# # -----------------------------
# def build_chroma(chunks):
#     chroma_client = chromadb.Client(Settings(chroma_db_impl="duckdb+parquet",
#                                              persist_directory="./rag_db"))
#
#     collection = chroma_client.get_or_create_collection(
#         name="rag_collection",
#         metadata={"hnsw:space": "cosine"}  # 使用余弦相似度
#     )
#
#     ids = [f"doc_{i}" for i in range(len(chunks))]
#
#     print("正在生成 Embeddings ...")
#
#     embeddings = []
#     batch_size = 32
#
#     for i in range(0, len(chunks), batch_size):
#         batch = chunks[i:i + batch_size]
#
#         response = client.embeddings.create(
#             model="text-embedding-3-small",
#             input=batch
#         )
#         emb = [e.embedding for e in response.data]
#         embeddings.extend(emb)
#
#     collection.add(
#         documents=chunks,
#         ids=ids,
#         embeddings=embeddings
#     )
#
#     print("向量库构建完成。")
#     return collection
#
#
# # -----------------------------
# # 4. 检索 + 生成回答
# # -----------------------------
# def query_rag(collection, query):
#     # 生成 Query Embedding
#     query_emb = client.embeddings.create(
#         model="text-embedding-3-small",
#         input=query
#     ).data[0].embedding
#
#     # 检索相关片段
#     results = collection.query(
#         query_embeddings=[query_emb],
#         n_results=3
#     )
#
#     context = "\n\n".join(results["documents"][0])
#
#     # 将上下文 + 问题发给大模型
#     response = client.chat.completions.create(
#         model="gpt-4o-mini",
#         messages=[
#             {"role": "system", "content": "你是一个专业文档助手，请结合上下文回答问题。"},
#             {"role": "user", "content": f"文档内容：\n{context}\n\n问题：{query}"}
#         ]
#     )
#
#     return response.choices[0].message.content
#
#
# # -----------------------------
# # 5. 主运行流程
# # -----------------------------
# if __name__ == "__main__":
#     file_path = "example.txt"   # 修改为你的文件路径
#     text = read_file(file_path)
#
#     chunks = split_text(text)
#
#     collection = build_chroma(chunks)
#
#     print("\n========= RAG 问答系统 =========")
#     while True:
#         query = input("\n请输入你的问题（输入 exit 退出）：")
#         if query.lower() == "exit":
#             break
#         answer = query_rag(collection, query)
#         print("\n💡 回答：\n", answer)


def start_main():
    smart_table_agent = SmartTableAgent()
    smart_table_agent.run()

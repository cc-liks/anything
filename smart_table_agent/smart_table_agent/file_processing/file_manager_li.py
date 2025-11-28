import os
from typing import List, Dict, Any, Union

from llama_index.core import SimpleDirectoryReader


class FileManager_LI:
    """
    使用 LlamaIndex 的文件管理器：
    - 自动识别文件类型
    - 自动处理 pdf、docx、csv、txt、md 等
    - 自动递归文件夹
    - 输出 LlamaIndex Document 列表
    """

    def __init__(self):
        pass

    # --------------------------------------
    # 读取单个文件 → Document 列表
    # --------------------------------------
    def load_file(self, file_path: str):
        if not os.path.isfile(file_path):
            raise ValueError(f"不是有效文件: {file_path}")

        reader = SimpleDirectoryReader(input_files=[file_path])
        docs = reader.load_data()

        return {
            "path": file_path,
            "type": "document",
            "documents": docs,
        }

    # --------------------------------------
    # 递归读取文件夹 → Document 列表
    # --------------------------------------
    def load_folder(self, folder_path: str):
        if not os.path.isdir(folder_path):
            raise ValueError(f"不是有效目录: {folder_path}")

        reader = SimpleDirectoryReader(folder_path, recursive=True)
        docs = reader.load_data()

        return {
            "folder": folder_path,
            "count": len(docs),
            "documents": docs
        }

    # --------------------------------------
    # 自动根据输入路径选择文件 or 文件夹
    # --------------------------------------
    def load_path(self, path: str):
        if os.path.isfile(path):
            return self.load_file(path)
        elif os.path.isdir(path):
            return self.load_folder(path)
        else:
            raise ValueError(f"路径无效: {path}")

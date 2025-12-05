import inspect
from typing import get_type_hints, List, Dict, Any, Union


# Python 类型 → JSON Schema 类型映射
type_map = {
    str: "string",
    int: "integer",
    float: "number",
    bool: "boolean",
    list: "array",
    dict: "object"
}


def python_type_to_schema(py_type):
    """
    将 Python 类型转换为 JSON Schema
    """
    origin = getattr(py_type, "__origin__", None)

    # List[X]
    if origin is list or origin is List:
        item_type = py_type.__args__[0]
        return {
            "type": "array",
            "items": python_type_to_schema(item_type)
        }

    # Dict[str, X]
    if origin is dict or origin is Dict:
        key_type, val_type = py_type.__args__
        return {
            "type": "object",
            "additionalProperties": python_type_to_schema(val_type)
        }

    # 基础类型
    return {"type": type_map.get(py_type, "string")}


def tool(func):
    """
    装饰器：标记可导出的方法
    """
    func._is_tool = True
    return func


class FunctionManager:
    tools = []

    def __init__(self):
        self._build_tools()

    def _build_tools(self):
        for name, method in inspect.getmembers(self, predicate=inspect.ismethod):
            if hasattr(method, "_is_tool"):
                signature = inspect.signature(method)
                type_hints = get_type_hints(method)

                # 从 docstring 获取 description
                doc = inspect.getdoc(method)
                description = doc.split("\n")[0] if doc else f"{name} function"

                # 构建 JSON Schema 参数
                props = {}
                required = []
                for param_name, param in signature.parameters.items():
                    if param_name == "self":
                        continue

                    # 获取注解
                    annotation = type_hints.get(param_name, str)
                    schema = python_type_to_schema(annotation)

                    props[param_name] = {
                        **schema,
                        "description": f"Parameter: {param_name}"
                    }
                    required.append(param_name)

                tool_schema = {
                    "type": "function",
                    "function": {
                        "name": name,
                        "description": description,
                        "parameters": {
                            "type": "object",
                            "properties": props,
                            "required": required
                        }
                    }
                }
                self.tools.append(tool_schema)

    def function_call(self, function_name, args):
        if hasattr(self, function_name):
            return getattr(self, function_name)(**args)

    # ---------------------
    #     示例函数
    # ---------------------
    @tool
    def get_weather(self, location: str) -> str:
        """
        Get weather of a given location
        """
        print(f"===========方法开始调用--传参：{location}=======================")
        return "24℃"

    @tool
    def add(self, a: int, b: int) -> int:
        """
        Return a + b
        """
        return a + b

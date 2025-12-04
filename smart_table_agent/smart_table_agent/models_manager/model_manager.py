from importlib import import_module
from typing import Optional


class ModelManager:
    """
    通用模型管理器
    - 可以注册任何模型类（DeepSeek / Claude / Qwen / GLM / 本地模型）
    - 模型类只需要有 chat(prompt) 方法即可
    """

    def __init__(self):
        self.models = {}
        self.active_model = None

    # 注册模型实例
    def register_model(self, name: str, llm_class_str: str, model_name: str = None, api_key: Optional[str] = None):
        """
        注册模型实例
        :param name: manager 内部代称
        :param llm_class_str: 模型类名称字符串，例如 "DeepSeek"
        :param model_name: 模型名称
        :param api_key: 模型 key（可选）
        """
        # 动态导入本地模块 models
        models_module = import_module(".models", package=__package__)
        print("模块:", models_module)
        print("模块内所有属性:", dir(models_module))
        print("模块内类:")
        for attr_name in dir(models_module):
            attr = getattr(models_module, attr_name)
            if isinstance(attr, type):
                print(f" - {attr_name} -> {attr}")

        # 从模块中获取类
        if not hasattr(models_module, llm_class_str):
            raise ValueError(f"models 模块中不存在类 {llm_class_str}")

        llm_class = getattr(models_module, llm_class_str)

        instance = llm_class(model_name=model_name, api_key=api_key)

        self.models[name] = instance

    # 列出模型
    def list_models(self):
        return list(self.models.keys())

    # 选择当前模型
    def set_active(self, name):
        if name not in self.models:
            raise ValueError(f"模型 '{name}' 未找到")
        self.active_model = name

    # 调用当前模型
    def run(self, prompt):
        if not self.active_model:
            raise RuntimeError("未设置任何活动模型，请调用 set_active(name)")

        model_instance = self.models[self.active_model]

        # 模型类只需要实现 chat(prompt)
        if not hasattr(model_instance, "chat"):
            raise RuntimeError(f"模型 '{self.active_model}' 缺少 chat() 方法")

        return model_instance.chat(prompt)

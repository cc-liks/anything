import os
from abc import ABC

from openai import OpenAI
from .llm_base import LLMBase

__all__ = ["DeepSeek"]


class DeepSeek(LLMBase, ABC):
    base_url = "https://api.deepseek.com"

    def __init__(self, model_name=None, api_key=None):
        if api_key is None:
            api_key = os.environ.get("DEEPSEEK_API_KEY", None)
        if model_name is None:
            model_name = "deepseek-chat"
        super().__init__(model_name, api_key)
        self.client = OpenAI(api_key=self._api_key, base_url=self.base_url)
        # self.model_name="deepseek-reasoner",

    def single_request(self, user_input, stream=False, stream_callback=None):
        """
        模型单次请求
        :param user_input:
        :param stream: stream=True的时候，启用流示返回
        :param stream_callback:
        :return:
        """
        messages = [{"role": "user", "content": user_input}]
        response = self._send_request(messages, stream=stream)
        response_content = self._response_handle(response, stream=stream, stream_callback=stream_callback)
        return response_content

    def multiple_requests(self, user_input_info: str = "", restart: bool = False, stream: bool = False,
                          stream_callback=None):
        """
        多轮聊天信息请求
        :param user_input_info:
        :param restart: 是否重新开启会话
        :param stream:
        :param stream_callback:
        :return:
        """
        if restart:
            self.reset()
            self.chat_history = [{"role": "user", "content": user_input_info}]
        else:
            self.chat_history.append({"role": "user", "content": user_input_info})
        response = self._send_request(self.chat_history, stream=stream)
        response_content = self._response_handle(response, stream=stream, stream_callback=stream_callback)
        return response_content

    def _send_request(self, messages: list[dict], stream=False):
        """
        发送请求信息
        :param messages: 聊天信息
        :param stream: 是否开启流式输出
        :return:
        """
        request_times = 0
        while True:
            try:
                response = self.client.chat.completions.create(
                    model=self._model_name,
                    messages=messages,
                    stream=stream
                )
                return response
            except Exception as e:
                print(e)
            request_times += 1
            if request_times >= 4:
                break
        return {"role": "assistant", "content": "不好意思，出错了。请重新请求。"}

    @staticmethod
    def _response_handle(response, stream: bool = False, stream_callback=None):
        """
        结果反馈处理
        :param response:
        :param stream:
        :param stream_callback:
        :return:
        """
        if stream:
            final_resp = ""
            for chunk in response:
                delta = chunk.choices[0].delta

                # 某些 chunk 会是控制信号，没有 content
                text = getattr(delta, "content", None)
                if not text:
                    continue
                # 将片段累积到最终结果
                final_resp += text
                # 如果提供了回调，则传递片段
                if stream_callback:
                    stream_callback(text)
                # 或者在此处打印
                # print(text, end="", flush=True)
            return final_resp

            # ------------------------------
            # 普通非流式模式
            # ------------------------------
        return response.choices[0].message.content

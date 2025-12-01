import os
from openai import OpenAI


class DeepSeek:
    api_key = os.environ.get("DEEPSEEK_API_KEY")
    base_url = "https://api.deepseek.com"

    def __init__(self, model_name="deepseek-chat"):
        self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)
        self.model_name = model_name
        # self.model_name="deepseek-reasoner",
        self.messages = []

    def request(self, user_input, stream=False):
        """
        模型请求
        :param user_input:
        :param stream: stream=True的时候，启用流示返回
        :return:
        """
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "user", "content": user_input},
            ],
            stream=stream  # True 是流逝返回，False是非流逝返回
        )
        if stream:
            resp = ""
            for chunk in response:
                resp += chunk.choices[0].delta.content
        else:
            resp = response.choices[0].message.content
        return resp

    def multiple_rounds_dialogue(self, user_input, restart=False):
        if restart:
            self.messages = [{"role": "user", "content": user_input}]
        else:
            self.messages.append({"role": "user", "content": user_input})
        response = self.multiple_requests()
        if isinstance(response, dict):
            self.messages.append(response)
            return response
        else:
            self.messages.append(response.choices[0].message)
        resp = response.choices[0].message.content
        return resp

    def multiple_requests(self):
        request_times = 0
        while True:
            try:
                response = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=self.messages
                )
                return response
            except Exception as e:
                print(e)
            request_times += 1
            if request_times >= 4:
                break
        return {"role": "assistant", "content": "不好意思，出错了。请重新请求。"}

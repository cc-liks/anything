class FunctionManager:
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_weather",
                "description": "Get weather of a location, the user should supply a location first.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The city and state, e.g. San Francisco, CA",
                        }
                    },
                    "required": ["location"]
                },
            }
        },
    ]

    def __init__(self):
        pass

    def function_call(self, function_name, args):
        if hasattr(self, function_name):
            return getattr(self, function_name)(**args)

    @staticmethod
    def get_weather(location):
        print(f"===========方法开始调用--传参：{location}=======================")
        return "24℃"

import os
import json

from openai import OpenAI
from dotenv import load_dotenv

from tools import (
    get_weather,
    get_stock_price,
    calculate_bmi,
    search_recipe
)


# 加载 .env
load_dotenv()


# 初始化 DeepSeek 客户端
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)


# 告诉大模型有哪些工具可以使用
tools = [

    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "查询城市天气信息",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "城市名称"
                    }
                },
                "required": ["city"]
            }
        }
    },


    {
        "type": "function",
        "function": {
            "name": "get_stock_price",
            "description": "查询公司股票价格",
            "parameters": {
                "type": "object",
                "properties": {
                    "company": {
                        "type": "string",
                        "description": "公司名称"
                    }
                },
                "required": ["company"]
            }
        }
    },


    {
        "type": "function",
        "function": {
            "name": "calculate_bmi",
            "description": "根据身高和体重计算BMI",
            "parameters": {
                "type": "object",
                "properties": {
                    "weight": {
                        "type": "number",
                        "description": "体重，公斤"
                    },
                    "height": {
                        "type": "number",
                        "description": "身高，米"
                    }
                },
                "required": [
                    "weight",
                    "height"
                ]
            }
        }
    },


    {
        "type": "function",
        "function": {
            "name": "search_recipe",
            "description": "根据食材查询菜谱",
            "parameters": {
                "type": "object",
                "properties": {
                    "food": {
                        "type": "string",
                        "description": "食材名称"
                    }
                },
                "required": ["food"]
            }
        }
    }

]


# 模拟用户输入
messages = [
    {
        "role": "user",
        "content": "什么是Python？"
    }
]


# 第一次请求大模型
response = client.chat.completions.create(
    model="deepseek-chat",
    messages=messages,
    tools=tools
)


msg = response.choices[0].message


print("第一次模型返回:")
print(msg)


# 判断模型是否选择工具
if msg.tool_calls:


    # 取第一个工具调用
    tool_call = msg.tool_calls[0]


    # 获取参数
    args = json.loads(
        tool_call.function.arguments
    )


    print("\n模型选择工具:")
    print(tool_call.function.name)


    print("\n模型传入参数:")
    print(args)


    # 根据工具名称执行对应函数

    if tool_call.function.name == "get_weather":

        result = get_weather(
            args["city"]
        )


    elif tool_call.function.name == "get_stock_price":

        result = get_stock_price(
            args["company"]
        )


    elif tool_call.function.name == "calculate_bmi":

        result = calculate_bmi(
            args["weight"],
            args["height"]
        )


    elif tool_call.function.name == "search_recipe":

        result = search_recipe(
            args["food"]
        )


    else:

        result = "未知工具"


    print("\n工具返回:")
    print(result)



    # 把工具调用加入消息历史
    messages.append(msg)


    # 把工具结果返回给模型
    messages.append(
        {
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": result
        }
    )


    # 第二次调用大模型
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        tools=tools
    )


    final_message = response.choices[0].message


    print("\n最终回答:")
    print(final_message.content)


else:

    print("\n模型直接回答:")
    print(msg.content)
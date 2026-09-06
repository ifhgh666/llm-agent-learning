import os
import json

from openai import OpenAI
from dotenv import load_dotenv

from tool_registry import tool_map


# 加载 .env 文件中的环境变量
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
                "required": ["weight", "height"]
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
    },
    {
    "type": "function",
    "function": {
        "name": "loop_test",
        "description": "用于测试Agent连续工具调用。工具返回结果后应再次调用本工具。",
        "parameters": {
            "type": "object",
            "properties": {
                "message": {
                    "type": "string",
                    "description": "测试内容"
                }
            },
            "required": ["message"]
        }
    }
}
]


def run_agent(user_input):
    messages=[
        {
            "role":"user",
            "content":user_input
        }
    ]
    max_steps = 10

    for step in range(max_steps):
        #请求模型
        response=client.chat.completions.create(
            model="deepseek-v4-flash",
            messages=messages,
            tools=tools
        )
        msg=response.choices[0].message

        #如果模型不再需要工具，说明任务完成
        if not msg.tool_calls:
            print("\nAgent: ")
            print(msg.content)

            break
        #保存模型要求调用的所有工具
        messages.append(msg)

        for tool_call in msg.tool_calls:
            tool_name = tool_call.function.name
            args=json.loads(
                tool_call.function.arguments
            )
            print("\n模型调用工具： ")
            print(tool_name)

            print("\n参数：")
            print(args)

            #查找工具
            tool_function = tool_map.get(tool_name)

            if tool_function is None:
                result ="未知工具"
            else:
                result = tool_function(**args)
            print("\n工具结果：")
            print (result)

            #把结果反馈给模型
            messages.append({
                "role":"tool",
                "tool_call_id":tool_call.id,
                "content":str(result)
            })
user_input = input("你：")

run_agent(user_input)
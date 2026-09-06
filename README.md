# LLM Agent 学习系统

这是一个使用 **Python、DeepSeek API 和 OpenAI Python SDK** 构建的 LLM Agent 学习项目。

本项目用于逐步学习和理解大模型 Agent 的核心机制，包括：

- Function Calling（函数调用）
- Tool Registry（工具注册表）
- 动态工具执行
- Tool Routing（工具路由）
- Agent Loop（Agent 循环）
- 最大执行步数保护
- 多工具调用
- 消息历史管理

---

## 项目简介

这个项目主要演示：

> 大语言模型如何从“只会生成文本”，升级为“可以调用外部 Python 工具完成任务”。

当前 Agent 可以：

1. 理解用户输入
2. 判断是否需要调用工具
3. 选择合适的工具
4. 自动生成工具参数
5. 动态执行 Python 函数
6. 将工具执行结果返回给大模型
7. 根据工具结果继续推理
8. 必要时继续调用其他工具
9. 在任务完成后自动结束
10. 通过最大执行步数避免无限循环

---

## Agent 工作流程

```text
用户
 |
 v
DeepSeek 大模型
 |
 | 判断是否需要工具
 v
Function Calling
 |
 v
Tool Registry
 |
 | 根据工具名找到 Python 函数
 v
执行工具
 |
 | 返回结果
 v
messages 消息历史
 |
 v
DeepSeek 大模型
 |
 | 继续推理
 |
 +------ 是否还需要工具？ ------+
 |                               |
 是                              否
 |                               |
 v                               v
继续执行工具                 输出最终答案
 |
 +---------- Agent Loop ----------+
## 当前功能
DeepSeek API 接入
OpenAI Python SDK 调用
Function Calling
多个自定义 Python 工具
动态 Tool Registry
动态 Python 函数执行
Tool Routing
支持多个 Tool Call
Agent Loop
最大执行步数保护
环境变量管理
基础异常处理
命令行交互输入
## 当前工具

当前 Agent 中包含以下测试工具：

get_weather

查询城市天气信息。

get_stock_price

查询公司股票价格。

calculate_bmi

根据身高和体重计算 BMI。

search_recipe

根据食材查询菜谱。

loop_test

用于测试 Agent 连续工具调用和最大执行步数保护。

这些工具目前主要用于学习和测试 Agent 的运行机制。

## 技术栈
Python 3.12
DeepSeek API
OpenAI Python SDK
python-dotenv
JSON
Function Calling
Tool Registry
Agent Loop
## 项目结构
llm-agent-learning
│
├── 111
│   ├── main.py
│   │   └── Agent 主程序和 Agent Loop
│   │
│   ├── tools.py
│   │   └── Python 工具函数
│   │
│   └── tool_registry.py
│       └── 工具名称和 Python 函数的映射
│
├── .env
│   └── API Key 配置
│
├── requirements.txt
│   └── Python 依赖
│
└── README.md
## 核心文件说明
main.py

主要负责：

接收用户输入
调用 DeepSeek
判断模型是否请求工具
执行 Agent Loop
调用 Tool Registry
把工具结果返回给模型
控制最大执行步数
输出最终答案
tools.py

这里保存 Agent 真正可以执行的 Python 工具。

例如：

def calculate_bmi(weight, height):
    bmi = weight / (height ** 2)
    return f"BMI指数是{bmi:.2f}"

需要注意：

大模型本身不会真正执行 Python 函数。

模型只负责：

判断是否需要工具
选择工具
生成参数

真正执行函数的是 Python 程序。

tool_registry.py

工具注册表负责：

根据大模型返回的工具名称，找到对应的 Python 函数。

例如：

tool_map = {
    "get_weather": get_weather,
    "get_stock_price": get_stock_price,
    "calculate_bmi": calculate_bmi,
    "search_recipe": search_recipe,
    "loop_test": loop_test
}

这样就不需要写大量：

if tool_name == "get_weather":
    ...
elif tool_name == "calculate_bmi":
    ...
elif tool_name == "search_recipe":
    ...

而是可以动态执行：

tool_function = tool_map.get(tool_name)

result = tool_function(**args)

这样代码更加简洁，也更容易扩展。

## 安装
1. 克隆仓库
git clone https://github.com/ifhgh666/llm-agent-learning.git

进入项目目录：

cd llm-agent-learning
2. 创建虚拟环境
python -m venv venv

Windows 激活虚拟环境：

venv\Scripts\activate
3. 安装依赖
pip install -r requirements.txt
环境变量配置

在项目根目录创建：

.env

内容：

DEEPSEEK_API_KEY=your_api_key_here

注意：

不要把真实 API Key 上传到 GitHub。

建议在 .gitignore 中加入：

.env
venv/
__pycache__/
运行项目

进入代码目录：

cd 111

运行：

python main.py

终端会显示：

你：

然后输入问题即可。

## 示例 1：简单工具调用

输入：

我身高1.75米，体重90公斤，帮我计算BMI。

模型可能生成：

模型调用工具：
calculate_bmi

参数：
{'height': 1.75, 'weight': 90}

Python 实际执行：

calculate_bmi(
    height=1.75,
    weight=90
)

工具返回：

BMI指数是29.39

然后工具结果会重新加入 messages，再次发送给大模型。

最终由大模型生成自然语言回答。

## 示例 2：多步骤 Agent 任务

输入：

我身高1.75米，体重90公斤。
请先帮我计算BMI。

如果BMI大于等于24，
就给我推荐一道以牛肉为食材的菜。

如果BMI小于24，
就推荐一道以鸡蛋为食材的菜。

Agent 可能经历以下过程：

第 1 步

DeepSeek
 |
 v
calculate_bmi
 |
 v
BMI = 29.39

然后进入下一轮：

第 2 步

DeepSeek 读取上一步工具结果
 |
 v
判断 29.39 >= 24
 |
 v
调用 search_recipe
 |
 v
food = "牛肉"

再进入下一轮：

第 3 步

DeepSeek
 |
 v
不再调用工具
 |
 v
输出最终答案

这就是 Agent Loop。

Agent Loop

Agent 不会在第一次工具调用后直接结束。

它会继续执行：

思考
 ↓
调用工具
 ↓
获得结果
 ↓
再次思考
 ↓
必要时继续调用工具
 ↓
最终回答

当前代码会限制最大执行次数，例如：

max_steps = 10

for step in range(max_steps):
    ...

这样可以避免模型出现无限循环：

模型
 ↓
工具
 ↓
模型
 ↓
工具
 ↓
模型
 ↓
工具
 ↓
......

从而避免：

API 持续消耗
程序无法退出
资源被不断占用
最大执行步数保护

Agent 有两种退出方式。

正常退出

当模型不再返回：

msg.tool_calls

说明模型认为任务已经完成。

程序会输出最终答案并结束。

强制退出

如果模型连续多轮都还在调用工具：

第1步
第2步
第3步
...
第10步

达到：

max_steps

之后程序会强制停止。

例如：

Agent 已达到最大执行步数，强制停止任务。
Tool Registry

早期版本中，工具调用使用硬编码：

if tool_name == "get_weather":
    ...
elif tool_name == "calculate_bmi":
    ...
elif tool_name == "search_recipe":
    ...

随着工具越来越多，这种方式会越来越难维护。

所以当前版本使用：

tool_function = tool_map.get(tool_name)

result = tool_function(**args)

整体流程变成：

模型返回工具名称
        ↓
Tool Registry
        ↓
找到 Python 函数
        ↓
动态执行
**args 的作用

假设模型返回：

args = {
    "weight": 90,
    "height": 1.75
}

执行：

tool_function(**args)

相当于：

calculate_bmi(
    weight=90,
    height=1.75
)

也就是说：

**args 会把 Python 字典展开成函数参数。

messages 的作用

messages 不只是简单的聊天记录。

它还保存了 Agent 当前任务的执行状态。

例如：

用户：
帮我计算BMI，然后根据结果推荐菜

↓

assistant：
我要调用 calculate_bmi

↓

tool：
BMI指数是29.39

↓

assistant：
根据BMI结果继续决定下一步

下一轮调用大模型时，会重新传入整个 messages：

client.chat.completions.create(
    messages=messages,
    ...
)

因此模型能够看到：

前面发生了什么，以及工具返回了什么。

这也是后续学习 Agent Memory 的基础。

Function Calling 和 Agent 的区别

简单 Function Calling：

用户
 ↓
LLM
 ↓
调用一个工具
 ↓
返回结果
 ↓
结束

Agent：

用户
 ↓
LLM
 ↓
工具
 ↓
结果
 ↓
LLM继续判断
 ↓
可能继续调用其他工具
 ↓
最终完成任务

因此 Agent 的核心不只是 Tool Calling。

还包括：

LLM
+
Tools
+
Messages
+
Agent Loop
##学习收获

通过目前这个项目，我已经学习了：

如何调用 LLM API
Function Calling 的基本原理
LLM 如何判断是否需要工具
Tool Schema 如何定义
如何解析模型生成的 JSON 参数
Python 字典如何实现 Tool Registry
如何动态调用 Python 函数
Tool Routing 的基本思想
Agent Loop 如何运行
工具结果如何加入 messages
为什么 Agent 需要最大执行步数
Function Calling 和 Agent 的区别
基础 Agent 工程化拆分
版本记录
v1.0 - Function Calling Agent

完成：

DeepSeek API 接入
基础 Function Calling
自定义 Python 工具
工具结果返回给大模型
v2.0 - Tool Registry

完成：

增加动态 Tool Registry
删除硬编码 if / elif 工具路由
动态执行 Python 函数
增加终端用户输入
v3.0 - Agent Loop

完成：

Agent 多步骤执行
多 Tool Call 支持
最大执行步数保护
loop_test 循环测试工具
Tool Result 写回消息历史
下一步计划
 支持多轮对话
 实现短期 Memory
 学习消息历史管理
 完善异常处理
 增加 Tool 日志
 学习 RAG
 构建 RAG Agent
 学习 LangGraph
 学习 MCP
 构建更加复杂的 Agent
 增加 Web 界面
## 学习路线

当前进度：

LLM API
   ↓
Function Calling
   ↓
Tool Registry
   ↓
Agent Loop
   ↓
最大执行步数保护
   ↓
【当前进度】
   ↓
短期 Memory
   ↓
多轮对话
   ↓
RAG
   ↓
LangGraph
   ↓
MCP
   ↓
更完整的生产级 Agent

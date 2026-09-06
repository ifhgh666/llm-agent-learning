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
```

---

## 当前功能

- DeepSeek API 接入
- OpenAI Python SDK 调用
- Function Calling
- 多个自定义 Python 工具
- 动态 Tool Registry
- 动态 Python 函数执行
- Tool Routing
- 支持多个 Tool Call
- Agent Loop
- 最大执行步数保护
- 环境变量管理
- 命令行交互输入

---

## 当前工具

当前 Agent 包含以下测试工具：

- `get_weather`：查询城市天气信息
- `get_stock_price`：查询公司股票价格
- `calculate_bmi`：根据身高和体重计算 BMI
- `search_recipe`：根据食材查询菜谱
- `loop_test`：测试 Agent 连续工具调用和最大执行步数保护

这些工具目前主要用于学习 Agent 的运行机制。

---

## 技术栈

- Python 3.12
- DeepSeek API
- OpenAI Python SDK
- python-dotenv
- JSON
- Function Calling
- Tool Registry
- Agent Loop

---

## 项目结构

```text
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
```

---

## 核心文件说明

### `main.py`

主要负责：

- 接收用户输入
- 调用 DeepSeek
- 判断模型是否请求工具
- 执行 Agent Loop
- 调用 Tool Registry
- 把工具结果返回给模型
- 控制最大执行步数
- 输出最终答案

---

### `tools.py`

这里保存 Agent 真正可以执行的 Python 工具。

例如：

```python
def calculate_bmi(weight, height):
    bmi = weight / (height ** 2)
    return f"BMI指数是{bmi:.2f}"
```

需要注意：

> 大模型本身不会真正执行 Python 函数。

模型负责：

1. 判断是否需要工具
2. 选择工具
3. 生成调用参数

真正执行函数的是 Python 程序。

---

### `tool_registry.py`

Tool Registry 负责：

> 根据大模型返回的工具名称，找到真正对应的 Python 函数。

例如：

```python
tool_map = {
    "get_weather": get_weather,
    "get_stock_price": get_stock_price,
    "calculate_bmi": calculate_bmi,
    "search_recipe": search_recipe,
    "loop_test": loop_test
}
```

之前可能需要：

```python
if tool_name == "get_weather":
    ...
elif tool_name == "calculate_bmi":
    ...
elif tool_name == "search_recipe":
    ...
```

现在可以直接：

```python
tool_function = tool_map.get(tool_name)

result = tool_function(**args)
```

这样更加容易扩展。

---

## 安装

### 1. 克隆仓库

```bash
git clone https://github.com/ifhgh666/llm-agent-learning.git
```

进入项目：

```bash
cd llm-agent-learning
```

---

### 2. 创建虚拟环境

```bash
python -m venv venv
```

Windows 激活：

```bash
venv\Scripts\activate
```

---

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

---

## 环境变量配置

在项目根目录创建 `.env`：

```env
DEEPSEEK_API_KEY=your_api_key_here
```

不要把真实 API Key 上传到 GitHub。

建议 `.gitignore` 中加入：

```gitignore
.env
venv/
__pycache__/
```

---

## 运行项目

进入代码目录：

```bash
cd 111
```

运行：

```bash
python main.py
```

终端会显示：

```text
你：
```

输入问题即可。

---

## 示例 1：简单工具调用

输入：

```text
我身高1.75米，体重90公斤，帮我计算BMI。
```

模型可能返回：

```text
模型调用工具：
calculate_bmi

参数：
{'height': 1.75, 'weight': 90}
```

Python 实际执行：

```python
calculate_bmi(
    height=1.75,
    weight=90
)
```

工具返回：

```text
BMI指数是29.39
```

工具结果会重新加入 `messages`，然后再次交给大模型。

---

## 示例 2：多步骤 Agent

输入：

```text
我身高1.75米，体重90公斤。

请先帮我计算BMI。

如果BMI大于等于24，
就给我推荐一道以牛肉为食材的菜。

如果BMI小于24，
就推荐一道以鸡蛋为食材的菜。
```

可能执行：

```text
第 1 步

DeepSeek
   ↓
calculate_bmi
   ↓
BMI = 29.39
```

然后：

```text
第 2 步

DeepSeek 读取 BMI 结果
   ↓
判断 29.39 >= 24
   ↓
search_recipe
   ↓
food = 牛肉
```

最后：

```text
第 3 步

DeepSeek
   ↓
不再调用工具
   ↓
输出最终答案
```

---

## Agent Loop

Agent 不会在调用一次工具之后立即结束。

它的基本过程是：

```text
思考
 ↓
调用工具
 ↓
获得工具结果
 ↓
再次思考
 ↓
必要时继续调用工具
 ↓
最终回答
```

例如代码中：

```python
max_steps = 10

for step in range(max_steps):
    ...
```

意味着 Agent 最多执行 10 轮。

---

## 为什么需要最大执行步数？

如果没有限制，模型理论上可能出现：

```text
LLM
 ↓
Tool
 ↓
LLM
 ↓
Tool
 ↓
LLM
 ↓
Tool
 ↓
……
```

不断循环。

可能导致：

- API 持续消耗
- 程序无法结束
- 浪费计算资源

因此需要：

```python
max_steps = 10
```

作为安全保护。

---

## Agent 的两种退出方式

### 正常退出

如果：

```python
msg.tool_calls
```

为空，说明模型认为：

> 已经不需要继续调用工具了。

这时输出最终答案并结束。

---

### 强制退出

如果连续执行达到：

```python
max_steps
```

则程序强制结束。

例如：

```text
Agent 已达到最大执行步数，强制停止任务。
```

---

## `**args` 的作用

假设模型返回：

```python
args = {
    "weight": 90,
    "height": 1.75
}
```

执行：

```python
tool_function(**args)
```

相当于：

```python
calculate_bmi(
    weight=90,
    height=1.75
)
```

也就是说：

> `**args` 会把字典中的键和值展开成函数参数。

---

## `messages` 的作用

`messages` 不只是聊天记录。

它同时保存 Agent 当前任务的执行过程。

例如：

```text
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
继续根据结果判断下一步
```

下一轮调用模型时：

```python
client.chat.completions.create(
    messages=messages,
    ...
)
```

模型会重新看到之前所有重要信息。

因此它知道：

> 上一步调用了什么工具，以及工具返回了什么结果。

这也是后续学习 Agent Memory 的基础。

---

## Function Calling 和 Agent 的区别

简单 Function Calling：

```text
用户
 ↓
LLM
 ↓
调用工具
 ↓
返回结果
 ↓
结束
```

Agent：

```text
用户
 ↓
LLM
 ↓
调用工具
 ↓
获得结果
 ↓
LLM继续判断
 ↓
可能继续调用其他工具
 ↓
最终完成任务
```

所以一个最基本的 Agent 可以理解为：

```text
LLM
+
Tools
+
Messages
+
Agent Loop
```

---

## 学习收获

目前已经学习：

- LLM API 的调用方式
- Function Calling 原理
- Tool Schema 定义
- JSON 参数解析
- Tool Registry
- Tool Routing
- Python 动态函数调用
- `**args`
- Agent Loop
- 多步骤工具调用
- `messages` 消息历史
- 最大执行步数保护
- Agent 基础工程化拆分

---

## 版本记录

### v1.0 - Function Calling

完成：

- DeepSeek API 接入
- Function Calling
- 自定义 Python 工具
- Tool Result 返回模型

---

### v2.0 - Tool Registry

完成：

- Tool Registry
- 删除硬编码 `if / elif`
- 动态执行 Python 函数
- 命令行用户输入

---

### v3.0 - Agent Loop

完成：

- Agent 多步骤执行
- 多 Tool Call 支持
- 最大执行步数保护
- `loop_test`
- Tool Result 写回 `messages`

---

## 下一步计划

- [ ] 多轮对话
- [ ] Short-Term Memory（短期记忆）
- [ ] 消息历史管理
- [ ] 完善异常处理
- [ ] Tool 日志
- [ ] RAG
- [ ] RAG Agent
- [ ] LangGraph
- [ ] MCP
- [ ] 更复杂的 Agent
- [ ] Web 页面

---

## 学习路线

```text
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
生产级 Agent
```

---

## License

MIT License

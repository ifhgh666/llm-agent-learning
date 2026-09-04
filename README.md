# LLM Agent Learning

一个基于 DeepSeek API 的简单 Agent 学习项目。

通过 OpenAI SDK 调用 DeepSeek 大模型，实现 Function Calling（工具调用），让大模型根据用户需求选择并调用 Python 工具。

---

## 项目介绍

本项目用于学习大语言模型（LLM）Agent 的基本工作流程。

实现流程：

用户输入问题：

```
北京天气怎么样？
```

↓

大模型理解用户意图

↓

选择工具：

```
get_weather()
```

↓

Python 执行工具函数

↓

返回工具结果

↓

大模型生成最终回答

---

## 技术栈

- Python 3.12
- DeepSeek API
- OpenAI Python SDK
- python-dotenv
- Function Calling
- LLM Agent

---

## 项目结构

```
llm-agent-learning
│
├── 111
│   ├── main.py        # Agent主程序
│   └── tools.py       # 工具函数
│
├── .env               # API Key配置
│
├── requirements.txt   # 项目依赖
│
└── README.md
```

---

## 环境配置

### 1. 创建虚拟环境

```bash
python -m venv venv
```

激活：

Windows:

```bash
venv\Scripts\activate
```

---

### 2. 安装依赖

```bash
pip install openai python-dotenv
```

---

### 3. 配置 API Key

创建 `.env` 文件：

```env
DEEPSEEK_API_KEY=你的API_KEY
```

---

## 运行项目

进入项目目录：

```bash
cd 111
```

运行：

```bash
python main.py
```

---

## Agent 工作流程

```
             用户
              |
              ↓
        DeepSeek LLM
              |
       判断是否需要工具
              |
              ↓
       Tool Calling
              |
              ↓
        Python函数
              |
              ↓
        返回结果
              |
              ↓
        LLM生成回答
```

---

## 示例

用户：

```
北京天气怎么样？
```

模型生成工具调用：

```json
{
    "name": "get_weather",
    "arguments": {
        "city": "北京"
    }
}
```

Python执行：

```python
get_weather("北京")
```

返回：

```
晴天，25度
```

模型最终生成：

```
北京今天晴天，25度。
天气比较舒适，适合户外活动。
```

---

## 学习目标

通过本项目学习：

- 如何调用大语言模型 API
- 如何使用环境变量保存 API Key
- 如何使用 Function Calling
- 如何设计 AI Tool
- 理解 Agent 基本工作机制

---

## 后续计划

- [ ] 增加更多工具
- [ ] 实现自动 Tool Router
- [ ] 支持多轮对话
- [ ] 加入记忆功能
- [ ] 使用 LangChain 构建 Agent
- [ ] 开发实际 AI 应用

# LLM Agent Learning System

A simple Agent learning project built with DeepSeek API and OpenAI SDK.

This project demonstrates how Large Language Models (LLMs) can use **Function Calling** to select and execute Python tools based on user requests.

---

## Overview

This project is created for learning the basic workflow of LLM Agents.

The system allows an LLM to:

1. Understand user requests
2. Decide whether a tool is needed
3. Generate tool call arguments
4. Execute Python functions
5. Use tool results to generate final responses

Example workflow:

```
User
 |
 v
LLM (DeepSeek)
 |
 | Tool Calling
 v
Python Tool
 |
 | Return Result
 v
LLM
 |
 v
Final Answer
```

---

## Features

- DeepSeek API integration
- OpenAI Python SDK usage
- Function Calling implementation
- Custom Python tools
- Environment variable management
- Basic Agent workflow

---

## Tech Stack

- Python 3.12
- DeepSeek API
- OpenAI SDK
- python-dotenv
- Function Calling
- LLM Agent Architecture

---

## Project Structure

```
llm-agent-learning
│
├── 111
│   ├── main.py          # Main Agent program
│   └── tools.py         # Custom tools
│
├── .env                 # API key configuration
├── requirements.txt     # Dependencies
└── README.md
```

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-name/llm-agent-learning.git
```

Enter the project directory:

```bash
cd llm-agent-learning
```

---

### 2. Create virtual environment

```bash
python -m venv venv
```

Activate the environment:

Windows:

```bash
venv\Scripts\activate
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Configuration

Create a `.env` file:

```env
DEEPSEEK_API_KEY=your_api_key_here
```

---

## Running the Project

Navigate to the project folder:

```bash
cd 111
```

Run:

```bash
python main.py
```

---

## Example

User input:

```
How is the weather in Beijing?
```

The LLM generates a tool call:

```json
{
  "name": "get_weather",
  "arguments": {
    "city": "Beijing"
  }
}
```

Python executes:

```python
get_weather("Beijing")
```

Tool returns:

```
Sunny, 25°C
```

The LLM then generates the final response:

```
The weather in Beijing is sunny with a temperature of 25°C.
It is a good day for outdoor activities.
```

---

## How It Works

The Agent workflow:

```
          User
           |
           v
    DeepSeek LLM
           |
   Understand Intent
           |
           v
    Select Tool
           |
           v
  Execute Python Function
           |
           v
    Tool Result
           |
           v
 Generate Final Response
```

---

## Learning Goals

Through this project, I learned:

- How to call LLM APIs
- How Function Calling works
- How LLMs select tools
- How to build a simple Agent system
- How LLMs interact with external tools

---

## Future Improvements

- [ ] Add more tools
- [ ] Implement automatic tool routing
- [ ] Support multi-turn conversations
- [ ] Add memory system
- [ ] Build more advanced Agents
- [ ] Integrate LangChain / LangGraph

---

## License

MIT License

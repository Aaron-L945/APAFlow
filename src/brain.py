import os
import re
import json
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import JsonOutputParser
from utils.parse_action import parse_ai_output
from dotenv import load_dotenv

load_dotenv()


def extract_json(raw_output):
    match = re.search(r"\{.*?\}", raw_output, re.S)  # 非贪婪匹配
    if match:
        try:
            action_json = json.loads(match.group())
            print("解析成功:", action_json)
            return action_json
        except json.JSONDecodeError as e:
            print("JSON 解析失败:", e)
    else:
        print("未找到 JSON")


class APAFlowBrain:
    def __init__(self):
        # 推荐使用 gpt-4o-mini 或 deepseek-chat，识别网页结构非常精准
        self.llm = ChatOpenAI(
            model=os.getenv("MODEL"), # 或者 deepseek-chat
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            openai_api_base=os.getenv("OPENAI_API_BASE")
        )

    def decide_action(self, goal, dom_text):
        prompt = f"""
你是一个专业的网页自动化 Agent，负责从 DOM 结构中生成可以执行的 CSS Selector。

任务：
根据用户目标和提供的精简 DOM，生成实现任务所需的操作步骤。

用户目标：
{goal}

精简 DOM：
{dom_text}

请严格返回 JSON 数组，每个元素代表一个操作步骤。

返回格式：
[
  {{
    "selector": "CSS选择器",
    "action": "click 或 fill",
    "value": "输入内容（仅当 action=fill 时填写，否则为空字符串）",
    "description": "简短步骤描述"
  }}
]

规则：
1. **只返回 JSON 数组，不要输出任何解释、文字、Markdown 或代码块。**
2. 所有字符串必须使用 **双引号**。
3. 如果任务包含多个步骤（例如“依次点击”“逐个点击”），请返回多个对象。
4. selector 必须是 **稳定且唯一的 CSS 选择器**。
5. 优先使用：
   - id
   - name
   - class
   - data-* 属性
   - 结构定位（如 nth-child）
6. 如果列表元素需要区分顺序，请使用 `nth-child()`。
7. 如果 action 为 click，value 必须为 ""。
8. description 要简短明确。

示例：

[
  {{
    "selector": "tbody tr:nth-child(1) td:nth-child(2) a",
    "action": "click",
    "value": "",
    "description": "点击第1条热榜"
  }},
  {{
    "selector": "tbody tr:nth-child(2) td:nth-child(2) a",
    "action": "click",
    "value": "",
    "description": "点击第2条热榜"
  }}
]
"""
        # parser = JsonOutputParser()
        # chain = self.llm | parser
        raw_output = self.llm.invoke(prompt)
        text_output = raw_output.content
        print(f"{raw_output.content=}")
        return parse_ai_output(raw_output=text_output)


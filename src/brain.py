import os
import re
import json
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import JsonOutputParser
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
    你是一个网页自动化专家。请根据提供的精简 DOM 结构，找到实现用户目标所需的 CSS 选择器。

    用户目标: {goal}
    精简 DOM: {dom_text}

    请严格仅返回 JSON，格式如下：
    {{
        "selector": "准确的CSS选择器",
        "action": "fill 或 click",
        "value": "如果是fill，请提供输入内容；如果是click，此处为空"
    }}

    注意事项：
    1. 仅输出 JSON，**不要添加任何解释、文本、换行或注释**。
    2. 所有字符串必须用双引号。
    3. 示例：
    {{
        "selector": "#username",
        "action": "fill",
        "value": "admin"
    }}
    /no_think"""
        # parser = JsonOutputParser()
        # chain = self.llm | parser
        raw_output = self.llm.invoke(prompt)
        text_output = raw_output.content
        return extract_json(raw_output=text_output)


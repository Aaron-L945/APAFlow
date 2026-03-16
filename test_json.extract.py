import re
import json

# 模拟 LLM 输出
raw_output = """
Invalid json output: <think>

</think>
{ "selector": "#kw", "action": "fill", "value": "openclaw最新资讯" } For troubleshooting, visit: https://docs.langchain.com/oss/python/langchain/errors/OUTPUT_PARSING_FAILURE"""

# 使用正则提取第一个 JSON 对象
match = re.search(r"\{.*?\}", raw_output, re.S)  # 非贪婪匹配
if match:
    try:
        action_json = json.loads(match.group())
        print("解析成功:", action_json)
    except json.JSONDecodeError as e:
        print("JSON 解析失败:", e)
else:
    print("未找到 JSON")
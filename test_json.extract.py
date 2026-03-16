import re
import json
from utils.parse_action import parse_ai_output


# --- 测试用例 ---
test_cases = [
    # 单步测试
    '这是结果：{"selector": "button#id", "action": "click", "description": "点我"}',
    # 链式测试
    '多步任务如下：\n```json\n[\n  {"selector": "tr:nth-child(1) a", "action": "click"},\n  {"selector": "tr:nth-child(2) a", "action": "click"}\n]\n```'
]

for i, case in enumerate(test_cases):
    print(f"\n测试用例 {i+1}:")
    parsed_steps = parse_ai_output(case)
    for step in parsed_steps:
        print(f"执行步骤: {step.get('description', '无描述')} -> {step['selector']}")
import re
import json

def parse_ai_output(raw_output):
    """
    支持单步 {} 和 链式 [] 的通用解析器
    """
    # 1. 扩充正则：同时支持匹配 [] 和 {}
    # 使用 re.DOTALL (re.S) 让 . 匹配换行符
    match = re.search(r"(\[.*\]|\{.*\})", raw_output, re.S)
    
    if not match:
        print("❌ 未找到 JSON 结构")
        return []

    try:
        # 清洗掉 Markdown 代码块标识（如果有）
        clean_json = match.group().replace('```json', '').replace('```', '').strip()
        data = json.loads(clean_json)
        
        # 2. 归一化处理：统一转为 List
        if isinstance(data, dict):
            steps = [data]  # 单步转为单元素列表
        elif isinstance(data, list):
            steps = data    # 链式保持不变
        else:
            steps = []
            
        print(f"{steps=}")
        return steps
    except json.JSONDecodeError as e:
        print(f"❌ JSON 解析失败: {e}")
        return []
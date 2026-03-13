from typing import TypedDict, Optional, List, Any 
from notifier.robot import send_webhook_notification
from core.browser import Browser
from core.dom_tools import DOMTools
from core.vision_tools import VisionTools
from core.deepseek_tools import DeepSeekTools

class AgentState(TypedDict): 
    goal: str                # 用户目标 
    url: str                 # 当前页面 
    dom_snippet: str         # 瘦身后的HTML 
    screenshot: Optional[str]# 截图路径 
    last_error: str          # 错误信息 
    retry_count: int         # 重试次数 
    results: List[dict]      # 最终采集的数据
    browser: Any             # Browser 实例
 
# L1 节点逻辑 
async def l1_dom_node(state: AgentState): 
    # 调用 DeepSeek 尝试通过 DOM 获取选择器并点击 
    # 如果失败，抛出异常或返回特定状态 
    browser = state["browser"] # Get browser instance from state
    await browser.goto(state["url"])
    dom_content = await browser.get_dom_content()
    dom_tools = DOMTools(dom_content)
    state["dom_snippet"] = dom_tools.simplify_dom()

    deepseek_tools = DeepSeekTools() # Initialize DeepSeekTools
    deepseek_analysis = await deepseek_tools.analyze_dom(state["dom_snippet"], state["goal"])

    action_type = deepseek_analysis.get("action_type")
    selector = deepseek_analysis.get("selector")
    text = deepseek_analysis.get("text")

    if action_type == "click" and selector:
        try:
            await browser.click(selector)
            state["last_error"] = "" # Clear error on success
        except Exception as e:
            state["last_error"] = f"L1 DOM click failed: {e}"
            print(state["last_error"])
    elif action_type == "type" and selector and text:
        try:
            await browser.type(selector, text)
            state["last_error"] = "" # Clear error on success
        except Exception as e:
            state["last_error"] = f"L1 DOM type failed: {e}"
            print(state["last_error"])
    else:
        state["last_error"] = "DeepSeek did not provide a valid action or selector for L1 DOM node."
        print(state["last_error"])
    
    return state
 
# L2 节点逻辑 
async def l2_vision_node(state: AgentState): 
    # 调用 GPT-4o-mini 进行视觉分析并点击坐标 
    browser = state["browser"] # Get browser instance from state
    screenshot_path = "screenshot.png" # Define a path for the screenshot
    await browser.screenshot(screenshot_path)
    state["screenshot"] = screenshot_path # Update state with screenshot path

    vision_tools = VisionTools(api_key="YOUR_VISION_API_KEY") # Replace with actual API key
    analysis_result = await vision_tools.analyze_screenshot(screenshot_path)
    
    if "action_coordinates" in analysis_result:
        x = analysis_result["action_coordinates"]["x"]
        y = analysis_result["action_coordinates"]["y"]
        try:
            await vision_tools.click_coordinates(browser.page, x, y)
            print(f"Clicked on coordinates: ({x}, {y})")
            state["last_error"] = "" # Clear error on success
        except Exception as e:
            state["last_error"] = f"L2 Vision click failed: {e}"
            print(state["last_error"])
    else:
        print("No action coordinates found in vision analysis.")
        # Handle cases where vision analysis doesn't provide click coordinates
        # For example, set an error or retry
        state["last_error"] = "Vision analysis failed to provide action coordinates."
        state["retry_count"] += 1
    return state
 
# L3 节点逻辑 
async def l3_human_node(state: AgentState): 
    # 发送钉钉通知，并调用 page.pause() 等待人工操作 
    send_webhook_notification("🚨 APAFlow 请求人工介入") 
    # Assuming 'browser' instance is available, e.g., passed as part of state or globally
    # For now, we'll add a placeholder for browser.pause()
    # You will need to ensure the Browser instance is properly initialized and accessible here.
    # For example, by passing it as an argument or storing it in the AgentState.
    browser = state["browser"] # Get browser instance from state
    await browser.pause()
    pass
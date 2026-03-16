import streamlit as st
from io import BytesIO
from browser_engine import BrowserEngine
from brain import APAFlowBrain # 导入新大脑

st.title("🚀 APAFlow 智能助手")

# --- 原有配置区 ---
url = st.text_input("1. 目标网址", "https://www.baidu.com")
headless = st.checkbox("隐藏浏览器界面 (Headless)", value=False) # 建议交互时设为 False 观察过程

# --- 新增交互区 ---
user_goal = st.text_input("2. 你想做什么？", "在搜索框输入 'APAFlow' 并点击搜索")

if st.button("开始自动化执行", key="run_btn"):
    if not user_goal:
        st.warning("请先输入你的目标")
    else:
        with st.spinner("APAFlow 正在思考并执行..."):
            try:
                print("初始化大脑")
                brain = APAFlowBrain()
                print("初始化大脑完成！")
                with BrowserEngine(headless=headless) as engine:
                    # 1. 访问网页
                    engine.page.goto(url, wait_until="domcontentloaded", timeout=60000)
                    
                    # 2. 感知：获取精简 DOM (你第一阶段的成果)
                    dom_text = engine.distill_dom(engine.page.content())
                    # print(f"{dom_text=}")
                    
                    # 3. 决策：让 AI 找到搜索框的选择器
                    st.write("🧠 AI 正在分析网页结构...")
                    action_data = brain.decide_action(user_goal, dom_text)
                    
                    # 4. 执行：点击并输入
                    selector = action_data['selector']
                    action = action_data['action']
                    val = action_data.get('value', '')
                    
                    st.info(f"🎯 AI 决定：在 `{selector}` 执行 `{action}`")
                    
                    if action == "fill":
                        # 增加 :visible 伪类，确保只操作看得见的那个框
                        visible_selector = f"{selector} >> visible=true"
                        # import pdb;pdb.set_trace()
                        try:
                            # 强制等待元素出现并变得可操作
                            # engine.page.wait_for_selector(visible_selector, state="visible", timeout=5000)
                            engine.page.fill(selector, val, force=True) # 暴力尝试
                            engine.page.press(selector, "Enter")
                        except Exception as e:
                            # 如果还是不行，可能是被弹窗遮挡了，这是启动 L2 视觉修复的信号
                            st.warning("⚠️ 元素点击失败，开始尝试视觉定位...")
                    elif action == "click":
                        engine.page.click(selector)
                    
                    # 等待一下看结果
                    engine.page.wait_for_timeout(5000)
                    
                    # 5. 反馈结果
                    final_screenshot = engine.page.screenshot()
                    st.success("任务执行成功！")
                    st.image(BytesIO(final_screenshot), caption="执行后的结果截图")

            except Exception as e:
                st.error(f"自动化执行失败: {e}")
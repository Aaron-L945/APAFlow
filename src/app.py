import streamlit as st
from io import BytesIO
from urllib.parse import urlparse

from browser_engine import BrowserEngine
from brain import APAFlowBrain # 导入新大脑
from memory.memory_db import APAFlowMemory # 导入记忆模块

# 在代码最上方初始化记忆库
memory = APAFlowMemory()

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
        with st.spinner("APAFlow 正在处理..."):
            try:
                domain = urlparse(url).netloc # 提取域名作为记忆索引
                
                with BrowserEngine(headless=headless) as engine:
                    engine.page.goto(url, wait_until="domcontentloaded", timeout=60000)
                    
                    # --- 核心：记忆检索逻辑 ---
                    st.write("🔍 正在检索大脑记忆...")
                    action_data = memory.get_experience(domain, user_goal)
                    
                    if action_data:
                        st.success(f"💡 发现既往成功经验，正在复用选择器: `{action_data['selector']}`")
                    else:
                        st.info("🧠 记忆库为空或经验不匹配，启动 AI 逻辑分析...")
                        dom_text = engine.distill_dom(engine.page.content())
                        # 调用 AI 获取决策
                        brain = APAFlowBrain()
                        action_data = brain.decide_action(user_goal, dom_text)
                        # AI 识别到新方案，标记一下
                        st.write("✨ AI 已生成新方案，准备执行并记录...")

                    # --- 执行逻辑 (沿用你跑通的代码) ---
                    selector = action_data['selector']
                    action = action_data['action']
                    val = action_data.get('value', '')
                    
                    # 尝试执行
                    executed_successfully = False
                    try:
                        if action == "fill":
                            engine.page.fill(selector, val, force=True)
                            engine.page.press(selector, "Enter")
                        elif action == "click":
                            current_page = engine.page
                            try:
                                # 尝试捕获新页面，同时执行点击
                                with engine.context.expect_popup(timeout=3000) as popup_info:
                                    current_page.click(selector, force=True)
                                
                                # 成功捕获新窗口
                                engine.page = popup_info.value 
                                engine.page.wait_for_load_state("networkidle")
                                st.info("🚀 已追踪到新打开的页面")
                            except:
                                # 没有新窗口弹出，说明是原页面跳转
                                st.info("跳转至当前页面新链接...")
                                engine.page.wait_for_load_state("networkidle")
                        
                        executed_successfully = True # 标记执行成功
                    except Exception as e:
                        # 如果执行失败（比如位置变了导致老记忆失效）
                        st.warning(f"⚠️ 经验失效或执行受阻: {e}")
                        # 此处可触发“记忆自愈”：清空该记忆并强制 AI 重新分析（篇幅原因，建议先跑通入库）

                    # --- 核心：记忆入库逻辑 ---
                    print(f"{action_data=}")
                    print(f"{executed_successfully=}")
                    if  executed_successfully:
                        # 拿到现有的（如果有）
                        old_exp = memory.get_experience(domain, user_goal)
                        
                        # 只有当：库里没记录，或者 AI 给出的新选择器和旧的不一样时，才写入
                        if not old_exp or old_exp['selector'] != action_data['selector']:
                            memory.save_experience(domain, user_goal, action_data)
                            st.success("✅ 经验库已更新！")

                    # 反馈结果
                    engine.page.wait_for_timeout(20000)
                    final_screenshot = engine.page.screenshot()
                    st.image(BytesIO(final_screenshot), caption="执行后的结果截图")

            except Exception as e:
                st.error(f"自动化执行失败: {e}")
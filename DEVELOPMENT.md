# APAFlow 开发文档

本文档记录了 APAFlow 项目的初始化设置和核心组件的实现细节。

## 1. 项目结构概览

APAFlow 项目包含以下主要目录和文件：

- `core/`: 核心功能模块，包括浏览器操作、DOM 处理和视觉工具。
- `data/`: 用于存放数据文件（目前为空）。
- `graph/`: 定义了代理状态和工作流节点逻辑。
- `notifier/`: 通知相关模块。
- `main.py`: 应用程序的入口点和 LangGraph 工作流的定义。
- `requirements.txt`: 项目依赖列表。
- `LICENSE`: 项目许可证文件。
- `README.md`: 项目说明文件。

## 2. 核心组件实现

### 2.1. `graph/state.py`

- **`AgentState` TypedDict**: 定义了代理的状态，包括用户目标、当前 URL、DOM 片段、截图路径、错误信息、重试次数和最终采集的数据。
- **`l1_dom_node(state: AgentState)`**:
    - **职责**: 负责基于 DOM 的操作。
    - **实现**:
        - 导入 `Browser` 和 `DOMTools`。
        - 使用 `Browser` 导航到 `state["url"]`。
        - 获取当前页面的 DOM 内容。
        - 使用 `DOMTools` 简化 DOM 并更新 `state["dom_snippet"]`。
        - **待办**: 需要集成 DeepSeek 模型来获取选择器并执行点击操作。
- **`l2_vision_node(state: AgentState)`**:
    - **职责**: 负责基于视觉的分析和操作。
    - **实现**:
        - 导入 `Browser` 和 `VisionTools`。
        - 使用 `Browser` 拍摄当前页面的屏幕截图，并将其路径存储在 `state["screenshot"]` 中。
        - 使用 `VisionTools` 分析屏幕截图，以获取操作坐标。
        - 根据视觉分析结果，使用 `Browser` 执行点击操作。
        - **待办**: `VisionTools` 的 `api_key` 需要替换为实际的 API 密钥。
- **`l3_human_node(state: AgentState)`**:
    - **职责**: 在自动化流程受阻时，请求人工介入。
    - **实现**:
        - 导入 `send_webhook_notification` 和 `Browser`。
        - 调用 `send_webhook_notification` 发送通知。
        - 调用 `browser.pause()` 等待人工操作。
        - **注意**: `Browser` 实例的传递和生命周期管理需要进一步完善。

### 2.2. `main.py`

- **LangGraph 工作流定义**:
    - 导入 `StateGraph` 和 `END`。
    - 导入 `AgentState` 和所有节点函数 (`l1_dom_node`, `l2_vision_node`, `l3_human_node`)。
    - 定义了 `should_fallback_to_vision` 和 `should_fallback_to_human` 占位符函数，用于条件路由。
    - 构建了 `StateGraph` 工作流，添加了 `l1_dom`、`l2_vision` 和 `l3_human` 节点。
    - 设置了 `l1_dom` 为入口点。
    - 配置了条件边，实现了 L1 失败回退到 L2，L2 失败回退到 L3 的逻辑。
    - `app = workflow.compile()` 编译了工作流。
- **`main()` 函数**:
    - 示例性地初始化了一个 `AgentState`。
    - 打印“Workflow compiled. Ready to run.”，表示工作流已准备就绪。
    - **待办**: 需要实现实际的 LangGraph 工作流执行逻辑。
- **主执行块**: 使用 `asyncio.run(main())` 启动异步 `main` 函数。

### 2.3. `notifier/robot.py`

- **`send_webhook_notification(message: str)`**:
    - **职责**: 发送 Webhook 通知。
    - **实现**:
        - 导入 `requests`。
        - 使用 `requests.post` 向预定义的 `webhook_url` 发送 JSON 格式的消息。
        - 包含错误处理机制。
        - **待办**: `webhook_url` 需要替换为实际的 Webhook URL。

### 2.4. `core/browser.py`

- **`Browser` 类**:
    - **职责**: 封装 Playwright 浏览器操作。
    - **实现**:
        - 导入 `async_playwright` 和 `Page`。
        - 提供了 `start()`、`goto()`、`close()`、`screenshot()`、`get_dom_content()`、`click()`、`type()`、`wait_for_selector()`、`evaluate()` 和 `pause()` 等方法。
        - 包含了用于测试的 `if __name__ == "__main__":` 块。

### 2.5. `core/dom_tools.py`

- **`DOMTools` 类**:
    - **职责**: 提供 DOM 内容的解析和处理工具。
    - **实现**:
        - 导入 `BeautifulSoup`。
        - `__init__`: 使用 `BeautifulSoup` 解析 HTML 内容。
        - `extract_text()`: 提取纯文本内容。
        - `find_elements(selector: str)`: 根据 CSS 选择器查找元素并返回其信息。
        - `get_element_attribute(selector: str, attribute: str)`: 获取元素的指定属性。
        - `simplify_dom()`: 移除脚本、样式标签、注释和多余的空白，以简化 DOM 结构。
        - 包含了用于测试的 `if __name__ == "__main__":` 块。

### 2.6. `core/vision_tools.py`

- **`VisionTools` 类**:
    - **职责**: 提供基于视觉的分析和操作。
    - **实现**:
        - 导入 `base64`、`BytesIO`、`PIL.Image`。
        - `__init__`: 初始化视觉模型客户端（占位符）。
        - `analyze_screenshot(screenshot_path: str)`: 读取屏幕截图，将其转换为 base64 编码，并调用视觉模型 API 进行分析（占位符）。
        - `click_coordinates(page, x: int, y: int)`: 在指定坐标处执行点击操作。
        - 包含了用于测试的 `if __name__ == "__main__":` 块。

## 3. 依赖管理

- **`requirements.txt`**:
    - 包含了项目所需的所有 Python 依赖：`langgraph`、`playwright`、`beautifulsoup4`、`requests`、`Pillow`。
- **依赖安装**:
    - 通过在 `/tmp` 目录中创建虚拟环境并使用 `pip install -r requirements.txt` 成功安装了所有依赖。

## 4. 后续步骤

- 实现 `main.py` 中 `should_fallback_to_vision` 和 `should_fallback_to_human` 的实际逻辑。
- 集成 DeepSeek 模型到 `l1_dom_node`。
- 配置 `VisionTools` 的实际 API 密钥。
- 完善 `Browser` 实例在节点间的传递和生命周期管理。
- 配置 `send_webhook_notification` 的实际 Webhook URL。
- **Playwright 浏览器启动问题**:
    - **问题描述**: 在当前容器环境中，Playwright 启动 Chromium 浏览器失败，报错 `TargetClosedError` 和 `chrome_crashpad_handler: --database is required`。
    - **尝试的解决方案**:
        - 添加 `--disable-dev-shm-usage` 参数。
        - 添加 `--disable-crash-reporter` 参数。
        - 添加 `--disable-setuid-sandbox` 和 `--disable-gpu` 参数。
    - **结果**: 所有尝试均未能解决问题，Chromium 仍然无法正常启动。
    - **临时对策**: 暂时注释掉 `main.py` 中 `browser_instance.start()` 和 `browser_instance.close()`，以便工作流的其他部分可以运行。


---

# APAFlow MVP 开发文档 (Phase 1)

## 1. 项目愿景

**APAFlow** 旨在打造一个“零代码”的智能体自动化平台。即使是完全不会写代码的用户，也能通过自然语言指令完成复杂的网页自动化任务。系统具备“自进化”能力，能够通过既往成功经验自动适应网页布局的变化。

---

## 2. 技术选型

| 模块 | 技术栈 | 说明 |
| --- | --- | --- |
| **前端界面** | Streamlit | 提供极简的交互对话框，隐藏技术细节。 |
| **执行引擎** | Playwright | 支持 Stealth 模式，处理动态加载及反爬。 |
| **智能决策** | DeepSeek / GPT-4o-mini | L1 层 DOM 分析与选择器生成。 |
| **持久化层** | SQLite | 存储成功路径，实现“用一次变聪明”的自进化。 |
| **逻辑调度** | LangGraph (核心思想) | 实现从“记忆尝试”到“AI 重新分析”的降级流转。 |

---
## 3. 系统架构与执行流

### 执行逻辑：

1. **意图接收**：用户输入目标 URL 和自然语言任务。
2. **经验匹配**：根据 `Domain + Task` 查询 SQLite。
* **命中**：直接提取选择器执行。
* **未命中**：启动 L1 AI 分析。


3. **DOM 瘦身**：剔除无关标签（Script, Style 等），将万行代码压缩至数 KB。
4. **AI 决策**：LLM 根据瘦身后的 DOM 返回 JSON 格式的指令。
5. **自愈与进化**：
* 若旧记忆失效，自动触发 AI 重新分析。
* 执行成功后，将最新的正确路径覆盖旧记录。



---

## 4. 项目结构

```text
APAFlow/
├── app.py                  # 用户交互界面 (Streamlit 入口)
├── brain.py                # 逻辑大脑 (LLM 接口封装)
├── browser_engine.py       # 浏览器驱动 (Playwright & DOM 瘦身)
├── memory_db.py            # 经验数据库 (SQLite 操作), 在memory 目录下
├── .env                    # API 密钥配置

```

---

## 5. 核心模块说明

### 5.1 DOM 瘦身策略 (browser_engine.py)

为了节省 Token 并提高 AI 识别准确率，我们只保留具有语义信息的属性：

* **保留标签**：`a`, `button`, `input`, `div`, `span`。
* **保留属性**：`id`, `class`, `name`, `aria-label`, `placeholder`, `href`。
* **过滤规则**：移除所有样式相关属性及随机生成的长字符串类名。

### 5.2 自进化记忆 (memory_db.py)

使用 `experiences` 表记录成功路径：

* `domain`: 网站域名。
* `task`: 用户任务描述。
* `path_json`: 存储具体的动作（click/fill）及其对应的 CSS 选择器。

---

## 6. 环境配置与启动

### 6.1 安装依赖

```bash
pip install streamlit playwright playwright-stealth beautifulsoup4 langchain-openai python-dotenv
playwright install chromium

```

### 6.2 环境变量 (.env)

```text
OPENAI_API_KEY=your_key_here
BASE_URL=https://api.deepseek.com/v1  # 或 OpenAI 官方地址

```

### 6.3 启动方式

**对于开发者：**

```powershell
$env:PYTHONPATH = "."
streamlit run app.py

```

**对于非技术用户 (一键启动)：**
直接运行项目根目录下的 `start.ps1` 脚本。

---

## 7. 后续路线图 (Roadmap)

* **Phase 2 (视觉降级)**：引入 GPT-4o-mini Vision 解决复杂布局及 Canvas 元素定位。
* **Phase 3 (人工介入)**：实现钉钉/飞书消息推送，当 AI 迷茫时，用户点击手机即可远程指导。
* **Phase 4 (批量化)**：支持 Excel 导入多行数据进行循环自动化。

---


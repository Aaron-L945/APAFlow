# import asyncio
# from playwright.async_api import async_playwright

# async def test_launch_browser():
#     async with async_playwright() as p:
#         browser = await p.chromium.launch(headless=False)
#         page = await browser.new_page()
#         await page.goto("https://baidu.com")
#         import time; time.sleep(2)
#         print("Browser launched successfully and navigated to example.com")
#         await browser.close()

# if __name__ == "__main__":
#     asyncio.run(test_launch_browser())




from playwright.sync_api import sync_playwright
import time

def baidu_search():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        page = context.new_page()
        page.set_default_timeout(60000)
        
        try:
            # 打开百度
            page.goto("https://www.baidu.com", wait_until="networkidle")
            print("已打开百度首页")
            
            # 等待更长时间
            time.sleep(2)
            
            # 方法1：直接通过JavaScript输入
            print("尝试通过JavaScript输入...")
            page.evaluate("""
                document.getElementById('kw').value = 'openclaw';
                document.getElementById('kw').dispatchEvent(new Event('input', { bubbles: true }));
            """)
            time.sleep(1)
            
            # 验证是否输入成功
            input_value = page.evaluate("document.getElementById('kw').value")
            if input_value == "openclaw":
                print("通过JavaScript成功输入: openclaw")
            else:
                # 方法2：通过键盘输入
                print("通过键盘输入...")
                page.locator("#kw").click()
                page.keyboard.type("openclaw", delay=100)
            
            # 点击搜索
            page.locator("#su").click()
            print("已点击搜索")
            
            # 等待结果
            page.wait_for_load_state("networkidle")
            page.wait_for_selector("#content_left", state="visible", timeout=10000)
            print("搜索结果已加载")
            
            # 截图
            page.screenshot(path="search_result.png", full_page=True)
            print("截图已保存")
            
            time.sleep(3)
            
        except Exception as e:
            print(f"发生错误: {e}")
            try:
                page.screenshot(path="error.png")
                print("错误截图已保存")
            except:
                pass
                
        finally:
            browser.close()
            print("浏览器已关闭")

if __name__ == "__main__":
    baidu_search()
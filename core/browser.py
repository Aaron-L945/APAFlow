from playwright.async_api import async_playwright, Page
import asyncio

class Browser:
    def __init__(self):
        self.browser = None
        self.page: Page = None

    async def start(self):
        self.browser = await async_playwright().start()
        browser_instance = await self.browser.chromium.launch(headless=False, args=["--disable-dev-shm-usage", "--disable-crash-reporter", "--disable-setuid-sandbox", "--disable-gpu"])
        self.page = await browser_instance.new_page()

    async def goto(self, url: str):
        await self.page.goto(url)

    async def close(self):
        if self.browser:
            await self.browser.stop()

    async def screenshot(self, path: str):
        await self.page.screenshot(path=path)

    async def get_dom_content(self) -> str:
        return await self.page.content()

    async def click(self, selector: str):
        await self.page.click(selector)

    async def type(self, selector: str, text: str):
        await self.page.type(selector, text)

    async def wait_for_selector(self, selector: str, timeout: int = 30000):
        await self.page.wait_for_selector(selector, timeout=timeout)

    async def evaluate(self, expression: str):
        return await self.page.evaluate(expression)

    async def pause(self):
        await self.page.pause()

if __name__ == "__main__":
    async def test_browser():
        browser = Browser()
        await browser.start()
        await browser.goto("https://www.google.com")
        await browser.screenshot("google.png")
        print(await browser.get_dom_content())
        await browser.close()

    asyncio.run(test_browser())
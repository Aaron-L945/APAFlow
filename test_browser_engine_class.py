import asyncio
import os
import sys

# Add the src directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, "src")
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

from browser_engine import BrowserEngine

async def test_browser_engine():
    print("Testing BrowserEngine class...")
    async with BrowserEngine(headless=False) as page:
        print("BrowserEngine initialized successfully.")
        await page.goto("https://baidu.com")
        print("Navigated to example.com")
        title = await page.title()
        print(f"Page title: {title}")
        assert "Example Domain" in title
        print("Test passed: Browser launched and navigated successfully.")

if __name__ == "__main__":
    asyncio.run(test_browser_engine())
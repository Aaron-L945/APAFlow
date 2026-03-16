import asyncio
asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

import streamlit as st
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import re

class BrowserEngine:

    def __init__(self, headless=True, ignore_https_errors=True):
        self.headless = headless
        self.ignore_https_errors = ignore_https_errors
        self.pw = None
        self.browser = None
        self.context = None
        self.page = None

    def __enter__(self):
        self.pw = sync_playwright().start()
        self.browser = self.pw.chromium.launch(
            headless=self.headless,
            args=["--disable-blink-features=AutomationControlled"]
        )
        self.context = self.browser.new_context(ignore_https_errors=self.ignore_https_errors)
        self.page = self.context.new_page()
        return self

    def __exit__(self, exc_type, exc, tb):
        if self.context:
            self.context.close()
        if self.browser:
            self.browser.close()
        if self.pw:
            self.pw.stop()

    def distill_dom(self, html):
        soup = BeautifulSoup(html, "html.parser")

        # 删除不必要的标签
        for s in soup(["script", "style", "svg", "path", "header", "footer"]):
            s.decompose()

        allowed_attrs = ["id", "class", "name", "aria-label", "placeholder", "href"]

        for tag in soup.find_all(True):
            # 避免 tag.attrs 为 None
            tag.attrs = {k: v for k, v in (tag.attrs or {}).items() if k in allowed_attrs}

            # 删除空标签
            if not tag.get_text(strip=True) and not tag.attrs:
                tag.decompose()

        return re.sub(r"\s+", " ", soup.decode_contents()).strip()

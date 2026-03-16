import asyncio
asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

import streamlit as st
from playwright.sync_api import sync_playwright

st.write("Playwright Test")

if st.button("run"):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)

        # 忽略 HTTPS 错误
        context = browser.new_context(ignore_https_errors=True)
        page = context.new_page()

        page.goto("https://example.com")
        st.write(page.title())

        context.close()
        browser.close()
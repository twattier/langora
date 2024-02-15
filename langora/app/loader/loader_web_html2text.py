from playwright.sync_api import sync_playwright, Page
from langchain_community.document_transformers import Html2TextTransformer
import random

from loader.loader_web import LoaderWeb, Document

class LoaderHtml2Text(LoaderWeb):

    def load_html(self, url:str)->str:
        user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.2227.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.3497.92 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
        ]
        random_agent = user_agents[random.randint(0, len(user_agents)-1)]

        html = None
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=False)
            context = browser.new_context(user_agent = random_agent)
            page = context.new_page()

            page.goto(url, wait_until="domcontentloaded")
            self.check_accept_coockies(page)

            if len(page.frames)>0:
                html = page.frames[0].content()
            else:
                html = page.content()
            context.close()
            browser.close()
        return html
    
    def check_accept_coockies(self, page:Page):        
        button = None
        # if page.is_visible("//button[contains(@id, 'accept')]"):
        #     button = page.query_selector("//button[contains(@id, 'accept')]")
        # elif page.is_visible("//button[contains(class, 'accept')]"):
        #     button = page.query_selector("//button[contains(class, 'accept')]")            

        button = page.locator("//button[contains(@id, 'accept')]").wait_for(timeout=1000)
        if not button.is_visible():
            button = page.locator("//button[contains(class, 'accept')]")
        if button.is_visible():
            button.click()
            page.wait_for_timeout(2000)
    
    def create_document(self, html:str)->Document:
        html2text = Html2TextTransformer()
        docs_transformed = html2text.transform_documents(html)
        return docs_transformed[0]
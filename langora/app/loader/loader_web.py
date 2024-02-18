import random
from playwright.sync_api import sync_playwright, Page, expect
from langchain_community.document_loaders.base import Document

from db.datamodel import SourceText, SourceTextImage
from config.conf_tree_b4 import web_scrapper, default_list_click
from utils.functions import get_url_hostname

class LoaderWeb():
    def __init__(self) -> None:
        self.scrapper = None
    
    def load_html(self, url:str)->str:
        host = get_url_hostname(url)
        self.scrapper = web_scrapper.get(host)
        
        user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.2227.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.3497.92 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
        ]
        random_agent = user_agents[random.randint(0, len(user_agents)-1)]

        html = None
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=True)
            context = browser.new_context(user_agent = random_agent)
            page = context.new_page()

            try:
                page.goto(url, wait_until="networkidle")
            except:
                pass           
            try:
                self.check_accept_coockies(page)
            except:
                pass

            if len(page.frames)>0:
                html = page.frames[0].content()
            else:
                html = page.content()
            context.close()
            browser.close()
        return html
    
    def check_accept_coockies(self, page:Page):
        button = None
        selectors = []        
        selector = self.scrapper.get("click") if self.scrapper else None            
        if selector:
            selectors.append(selector)
        selectors.extend(default_list_click)
        for selector in selectors:
            button = page.query_selector(selector)
            if button:
                break
        if button:
            button.click()
            page.wait_for_timeout(2000)

    def load_document(self, url:str)->Document:
        html = self.load_html(url)
        return self.create_document(html)

    def create_document(self, html:str)->Document:
        raise NotImplementedError

class DocTree():
    def __init__(self, order:int=0, index:int=0, title:str=None, parent=None) -> None:
        self.order:int = order
        self.index:int = index
        self.title:str = title        
        self.text:str = ""
        self.images = []

        self.parent:DocTree = parent
        self.childs:list[DocTree] = []

    def __repr__(self):
        title = self.title if self.title else 'Root'
        return f"[{self.index}] {title}"

    def insert(self, order:int, index:int, title:str):
        new = DocTree(order=order, index=index, title=title)
        if index==self.index:
            self.parent.childs.append(new)
            new.parent = self.parent
        elif index>self.index:
            self.childs.append(new)
            new.parent = self
        elif index<self.index:
            up = self.parent
            while index<up.index:
                up = up.parent
            if up.index == 0:
                up.childs.append(new)
                new.parent = up
            else:
                up.parent.childs.append(new)
                new.parent = up.parent
        return new
    
    def clean_texts(self)->None:
        if self.title:            
            self.title = self.clean_text(self.title)
        self.text = self.clean_text(self.text)
        for child in self.childs:
            child.clean_texts()     

    def clean_text(self, txt:str)->str:
        txt = txt.strip()
        if txt.find("\n")==0:
            txt = txt[len("\n"):]
        while txt.find('  ')>=0:
            txt = txt.replace('  ', ' ')         
        return txt
    
    def create_source_texts(self)->list[SourceText]:
        list = []
        st = SourceText(
            order = self.order,
            index = self.index,
            title = self.title,
            text = self.text
        )
        order = 0
        for img in self.images:
            order += 1
            sti = SourceTextImage(
                order=order,
                url=img[0],
                alt=img[1]
            )
            st.images.append(sti)
        list.append(st)
        for child in self.childs:
            list.extend(child.create_source_texts())
        return list
    
class LoaderWebTree(LoaderWeb):
    
    def __init__(self) -> None:
        super().__init__()
        self.tree = None

    def load_tree(self, url:str)->DocTree:
        html = self.load_html(url) 
        self.tree = self.create_tree(html)
        return self.tree

    def create_tree(self, html:str)->DocTree:
        raise NotImplementedError
    
    def load_document(self, url:str)->Document:
        if not self.tree:
            self.load_tree(url)
        return self.tree.create_document()
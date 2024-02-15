from langchain_community.document_loaders import AsyncChromiumLoader
from bs4 import BeautifulSoup
import re

from loader.loader_web import DocTree, LoaderWebTree
from loader.loader_web_html2text import LoaderHtml2Text

class LoaderTreeB4(LoaderWebTree):
    def __init__(self) -> None:
        self.loader_web = LoaderHtml2Text()

    def load_html(self, url: str) -> str:
        return self.loader_web.load_html(url)
    
    def create_tree(self, html:str)->DocTree:
        soup = BeautifulSoup(html, 'html.parser')

        root = DocTree()
        level = root
        pattern_header = re.compile("^h[0-9]$")
        skip_next_text = False  
        order = 0      
        for tag in self.start(soup).descendants:            
            if isinstance(tag, str):
                if not self.is_empty(tag):
                    if skip_next_text:
                        skip_next_text=False
                        continue
                    level.text += self.clean_text(tag)
                continue
            if pattern_header.match(tag.name):
                idx = int(tag.name[1:])
                order += 1
                level = level.insert(order, idx, tag.text)
                skip_next_text = True
            elif tag.name == "img":
                img_url, alt = self.parse_img(tag)
                if img_url:
                    level.images.append((img_url, alt))
            elif tag.name == "li":
                if (not self.is_empty(tag.text)) and (not tag.find('p')):
                    level.text += "\n - "
            elif tag.name in ['p']:
                level.text += "\n"
            elif tag.name in ['span', 'div']:
                level.text += " "
            elif tag.name in ['script', 'sup']:
                skip_next_text=True

        root.clean_text() 
        return root
    
    def start(self, soup:BeautifulSoup):
        start = None
        if not start:
            start = soup.find('div', class_=lambda x: x and x.lower().find('container')>=0)
        if not start:
            start = soup.find('article')
        if not start:
            start = soup.find('div', class_=lambda x: x and x.lower().find('article')>=0)
        if not start:
            start = soup.find('div', id=lambda x: x and x.lower().find('content')>=0)
        if not start:
            start = soup.find('div', class_=lambda x: x and x.lower().find('content')>=0)                
        if not start:
            start = soup.find("body") 
        return start
    
    def parse_img(self, tag):
        url = tag.get('src')
        if not url:
            url = tag.get('data-src')
        alt = tag.get('alt')
        return url, alt
    
    def clean_text(self, txt):
        return txt.replace(u'\n', u'').replace(u'\xa0', u' ').strip()
    
    def is_empty(self, txt):
        return len(self.clean_text(txt))==0
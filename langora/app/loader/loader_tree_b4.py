from langchain_community.document_loaders import AsyncChromiumLoader
from bs4 import BeautifulSoup
import re

from loader.loader_web import DocTree, LoaderWebTree
from config.conf_tree_b4 import default_list_content, MIN_IMG_SIZE
from utils.functions import get_img_sizes

class LoaderTreeB4(LoaderWebTree):
    def __init__(self) -> None:
        super().__init__()
    
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

        root.clean_texts() 
        return root
    
    def start(self, soup:BeautifulSoup):
        start = None
        selectors = []
        #use config
        selector = self.scrapper.get("content") if self.scrapper else None
        if selector:
            selectors.append(selector)
        #default            
        selectors.extend(default_list_content)
        for selector in selectors:
            start = self.find(soup, selector)
            if start:
                break
        return start
    
    def parse_selector(self, crit):        
        ta = crit.split('/')
        tag = ta[0]
        key = value = None
        if len(ta)>1:
            av = ta[1].split('=')
            key = av[0]
            value = av[1]
        return (tag, key, value)
    
    def find(self, soup, selector):
        (tag, key, value) = self.parse_selector(selector)
        if not key:
            return soup.find(tag)
        elif key=='id':
            res = res = soup.find(tag, id=value)
            if not res:
                res = soup.find(tag, id=lambda x: x and x.lower().find('%value')>=0)
            return res
        elif key=='class':
            res = res = soup.find(tag, class_=value)
            if not res:
                res = soup.find(tag, class_=lambda x: x and x.lower().find('%value')>=0)
            return res
        return soup.find(lambda tag: tag.name=='%tag' and tag.has_attr('%key') and tag['%key'].lower().find('%value')>=0)
    
    def parse_img(self, tag):
        url = tag.get('src')
        if not url:
            url = tag.get('data-src')
        if url:
            kb, size = get_img_sizes(url)
            if not size \
                or (size[0]<MIN_IMG_SIZE and size[1]<MIN_IMG_SIZE):
                return None, None
        alt = tag.get('alt')           
        return url, alt
    
    def clean_text(self, txt):
        return txt.replace(u'\n', u'').replace(u'\xa0', u' ').strip()
    
    def is_empty(self, txt):
        return len(self.clean_text(txt))==0
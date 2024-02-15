from langchain_community.document_loaders.base import Document

from db.datamodel import SourceText, SourceTextImage

class LoaderWeb():
    
    def load_html(self, url:str)->str:
        raise NotImplementedError

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
    
    def clean_text(self):
        while self.text.find('  ')>=0:
            self.text = self.text.replace('  ', ' ')
        for child in self.childs:
            child.clean_text()    
    
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
            list.extend(child.create_source_texts)
        return list

    def create_document(self):
        return None
    
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
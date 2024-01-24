from datetime import datetime
from typing import List

from langchain_core.documents import Document

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Text, DateTime, Boolean, JSON
from sqlalchemy import ForeignKey

class Base(DeclarativeBase):
    pass

class Knowledge(Base):
    __tablename__ = "knowledge"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    agent: Mapped[str] = mapped_column(String, nullable=False)
    topics: Mapped[list] = mapped_column(JSON, nullable=False)

class Search(Base):
    __tablename__ = "search"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    query: Mapped[str] = mapped_column(String, nullable=False)
    from_user: Mapped[bool] = mapped_column(Boolean, default=True)
    search_sources: Mapped[List["SearchSource"]] = relationship(back_populates="search", order_by='SearchSource.rank')

    def contains_source(self, source_id:int)->bool:
        for ss in self.search_sources:
            if ss.source.id == source_id:
                return True
        return False

class Source(Base):
    __tablename__ = "source"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True) 
    
    url: Mapped[str] = mapped_column(String, nullable=True)   
    site: Mapped[str] = mapped_column(String, nullable=True)
    title: Mapped[str] = mapped_column(String, nullable=True)
    snippet: Mapped[str] = mapped_column(Text, nullable=True)
    extract: Mapped[str] = mapped_column(Text, nullable=True)
    date_created: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    summary: Mapped[str] = mapped_column(Text, nullable=True)
    date_summary: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    search_sources: Mapped[List["SearchSource"]] = relationship(back_populates="source", order_by='SearchSource.rank')

    def document_extract(self)->Document:
        return Document(
                page_content=self.extract, metadata={"source": self.url}
            )

class SearchSource(Base):
    __tablename__ = "search_source"

    id_search: Mapped[int] = mapped_column(Integer, ForeignKey(Search.id), primary_key=True)
    search:Mapped["Search"] = relationship(back_populates="search_sources")
    
    id_source: Mapped[int] = mapped_column(Integer, ForeignKey(Source.id), primary_key=True)
    source: Mapped["Source"] = relationship(back_populates="search_sources")

    rank: Mapped[int] = mapped_column(Integer, nullable=False)
    date_created: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
from datetime import datetime
from typing import List

from langchain_core.documents import Document

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Text, DateTime, Boolean, JSON
from sqlalchemy import Table, Column, ForeignKey


# ---------------------------------------------------------------------------
# ORM
# ---------------------------------------------------------------------------
class Base(DeclarativeBase):
    pass

class Knowledge(Base):
    __tablename__ = "knowledge"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    agent: Mapped[str] = mapped_column(String, nullable=False)
    date_created: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

association_search_topic = Table(
    "search_topic",
    Base.metadata,
    Column("search_id", ForeignKey("search.id"), primary_key=True),
    Column("topic_id", ForeignKey("topic.id"), primary_key=True),
)

class Topic(Base):
    __tablename__ = "topic"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)

    searches: Mapped[List["Search"]] = relationship(
        secondary=association_search_topic, back_populates="topics"
    )

class Search(Base):
    __tablename__ = "search"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    query: Mapped[str] = mapped_column(String, nullable=False)
    date_created: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    topics: Mapped[List["Topic"]] = relationship(
        secondary=association_search_topic, back_populates="searches"
    )

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
    date_extract: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    summary: Mapped[str] = mapped_column(Text, nullable=True)
    date_summary: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    search_sources: Mapped[List["SearchSource"]] = relationship(back_populates="source", order_by='SearchSource.rank')

    def get_name(self):
        return f'{self.title} [{self.site}]'

    def document_extract(self)->Document:
        return Document(
                page_content=self.extract, metadata={"source": self.url}
            )

class SearchSource(Base):
    __tablename__ = "search_source"

    search_id: Mapped[int] = mapped_column(Integer, ForeignKey(Search.id), primary_key=True)
    search:Mapped["Search"] = relationship(back_populates="search_sources")
    
    source_id: Mapped[int] = mapped_column(Integer, ForeignKey(Source.id), primary_key=True)
    source: Mapped["Source"] = relationship(back_populates="search_sources")

    rank: Mapped[int] = mapped_column(Integer, nullable=False)
    date_created: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

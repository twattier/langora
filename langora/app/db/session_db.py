import numbers
from langchain_core.embeddings import Embeddings
from sqlalchemy import Connection
from sqlalchemy.orm import Session
from sqlalchemy import select, delete, text, func, and_, or_

from db.datamodel import Base, Topic, Knowledge, Search, Source, SearchSource, SourceText
from db.dbvector import DbVector

class SessionDB():
    def __init__(self, connection:Connection, embeddings:Embeddings)->None:        
        self.connection = connection
        self.session = Session(bind=connection)
        self.vector = DbVector(self, embeddings)
        self.vector.init_stores()
    
    def close(self)->None:   
        try:
            print("Commit session")     
            self.session.commit()
        finally:
            self.session.close()         
            self.session = None
            self.connection.close()
            self.connection = None
            self.vector = None

    # ---------------------------------------------------------------------------
    # ORM
    # ---------------------------------------------------------------------------

    # ---------------------------------------------------------------------------
    # Knowledge
    
    def select_knowledge(self)->Knowledge:
        stmt = select(Knowledge)
        return self.select_one(stmt)
    
    # ---------------------------------------------------------------------------
    # Topic
    
    def select_topic_by_name(self, name:str)->Topic:        
        stmt = select(Topic).where(Topic.name == name)
        return self.select_one(stmt)

    def select_topics_by_ids(self, ids:list[int])->list[Topic]:
        if len(ids)==0:
            return []
        stmt = select(Topic).where(Topic.id.in_(ids))
        return self.select_many(stmt)
    
    def select_topics(self)->list[Topic]:
        stmt = select(Topic)
                # , func.count(Table("search_topic", Column('search_id'))).label('total')) \
                # .join(Topic.searches) \
                # .group_by(Topic).order_by(text('total DESC')).limit(max)
        topics = self.select_many(stmt)       
        topics.sort(key=lambda t: len(t.searches), reverse=True)     
        return topics

    # ---------------------------------------------------------------------------
    # Search 
        
    def select_search_by_id(self, id:int)->Search:
        stmt = select(Search).where(Search.id==id)
        return self.select_one(stmt)
    
    def select_searches_by_ids(self, ids:list[int])->list[Search]:
        if len(ids)==0:
            return []
        #TODO fix in_
        # stmt = select(Search).where(Search.id.in_(ids))
        # return self.select_many(stmt)
        list = []
        for id in ids:
            list.append(self.select_search_by_id(id))
        return list
        
    def select_search_by_query(self, query)->Search:
        stmt = select(Search).where(func.lower(Search.query)==func.lower(query))
        return self.select_one(stmt)
    
    def select_searches(self)->list[Search]:
        stmt = select(Search)
        return self.select_many(stmt)
    
    def select_top_searches(self, max=5)->list[Search]:
        stmt = select(Search, func.count(SearchSource.source_id).label('total')) \
                .join(Source.search_sources).group_by(Search).order_by(text('total DESC')).limit(max)
        return self.select_many(stmt)    
    
    # ---------------------------------------------------------------------------
    # Sources

    def select_source_by_id(self, id:int)->Source:
        stmt = select(Source).where(Source.id==id)
        return self.select_one(stmt)
    
    def select_source_by_url(self, url)->Source:
        stmt = select(Source).where(func.lower(Source.url)==func.lower(url))
        return self.select_one(stmt)
    
    def select_sources(self)->list[Source]:
        stmt = select(Source)
        return self.select_many(stmt)
    
    def select_top_sources(self, max=5)->list[Source]:
        stmt = select(Source, func.count(SearchSource.search_id).label('total')) \
                .join(Source.search_sources).group_by(Source).order_by(text('total DESC')).limit(max)
        return self.select_many(stmt)
    
    def select_not_extracted_sources(self)->list[Source]:
        # stmt = select(Source).where(Source.nb_source_texts() == 0)
        # return self.select_many(stmt)
        return list(filter(lambda x: len(x.source_texts) == 0, self.select_sources()))
    
    def select_not_summarized_sources(self)->list[Source]:
        # stmt = select(Source).where(
        #     and_(Source.nb_source_texts() > 0, Source.summary == None)
        #     )
        # return self.select_many(stmt)
        stmt = select(Source).where(Source.summary == None)
        return list(filter(lambda x: len(x.source_texts) > 0, self.select_many(stmt)))
    
    def delete_all_source_texts(self, source_id):
        stmt = delete(SourceText).where(SourceText.source_id==source_id)
        self.session.execute(stmt)
    def delete_source_text(self, source_text_id):
        stmt = delete(SourceText).where(SourceText.id==source_text_id)
        self.session.execute(stmt)
    def select_source_text(self, source_text_id):
        stmt = select(SourceText).where(SourceText.id==source_text_id)
        return self.select_one(stmt)

    # ---------------------------------------------------------------------------
    # Execute
    # ---------------------------------------------------------------------------
    def add(self, obj:Base)->None:
        self.session.add(obj)

    def exists(self, table, **kargs):
        criteria = ""
        for key, value in kargs:
            if criteria != "": criteria += " AND "
            criteria += f"{key} = "
            criteria = str(value) if isinstance(value, numbers.Number) else f"'{value}'"
        stmt = text(f"SELECT 1 from {table} WHERE {criteria}")
        return self.session.execute(stmt).first() != None

    def select_one(self, stmt):        
        return self.session.execute(stmt).scalar_one_or_none()
    
    def select_many(self, stmt):
        return self.session.execute(stmt).scalars().all()
    
    def execute_sql(self, query:str):
        stmt = text(query)
        self.session.execute(stmt)
    
    def save(self)->None:        

        nb_new = len(self.session.new)
        nb_update = len(self.session.dirty)
        nb_delete = len(self.session.deleted)
        nb_change = nb_new + nb_update + nb_delete

        if nb_change == 0:
            print("Flush : No change")
            return 
          
        print("Flush : new objects  : {} , updated objects : {}, deleted objects : {}"
              .format(nb_new, nb_update, nb_delete))                        
        self.session.flush()
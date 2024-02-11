import numbers
from langchain.vectorstores.pgvector import PGVector
from sqlalchemy import Engine
from sqlalchemy import select, text, func, and_
from sqlalchemy.orm import Session

from config.env import Config
from db.datamodel import Base, Topic, Knowledge, Search, Source, SearchSource

class SessionDB():
    def __init__(self, engine:Engine)->None:
        self.engine = engine
        self.connection = self.engine.connect()            
        # self.session = Session(bind=self.connection,
        #                        expire_on_commit=False, 
        #                        autocommit=False,
        #                        join_transaction_mode="create_savepoint"
        #                     )
        self.session  = Session(self.engine, 
                                expire_on_commit=False, 
                                autocommit=False
                                )
    
    def close(self)->None:
        self.session.close() 
        self.connection.close()

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
        stmt = select(Source).where(Source.extract == None)
        return self.select_many(stmt)
    
    def select_not_summarized_sources(self)->list[Source]:
        stmt = select(Source).where(
            and_(Source.extract != None, Source.summary == None)
            )
        return self.select_many(stmt)

    # ---------------------------------------------------------------------------
    # Create Database
    # ---------------------------------------------------------------------------

    def recreate_database(self):
        self.clean_database()        
        self.create_schema()

    def clean_database(self):
        print('Clean Database if needed')       
        for dm in ["knowledge", "search_topic", "topic", "search_source", "source", "search"]:
            query = "DROP TABLE IF EXISTS " + dm
            self.raw_execute(query)
        for em in ["langchain_pg_embedding"]: #, "langchain_pg_collection"]:
            query = "TRUNCATE " + em
            self.raw_execute(query)        

    def create_schema(self):
        print('Create schema')
        Base.metadata.create_all(self.engine)

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
    
    def save(self)->None:        

        nb_new = len(self.session.new)
        nb_update = len(self.session.dirty)
        nb_delete = len(self.session.deleted)
        nb_change = nb_new + nb_update + nb_delete

        if nb_change == 0:
            print("Commit : No change")
            return 
          
        print("Commit : new objects  : {} , updated objects : {}, deleted objects : {}"
              .format(nb_new, nb_update, nb_delete))        
        self.session.commit()

    def raw_execute(self, query:str)->None:
        try:
            connection = self.engine.raw_connection()
            cursor = connection.cursor()
            command = query
            cursor.execute(command)
            connection.commit()            
        except:
            print("SQL Execute Error : " + query)
        finally:
            cursor.close()
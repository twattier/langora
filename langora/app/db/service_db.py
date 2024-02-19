from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool

from db.dbvector import DbVector, CONNECTION_STRING
from db.session_db import SessionDB

class ServiceDB():
    def __init__(self)->None:
        self.engine = create_engine(CONNECTION_STRING, echo=False, poolclass=NullPool)
        self.vector = DbVector()
        self.vector.init_stores()

    def create_session(self)->SessionDB:
        return SessionDB(self.engine)
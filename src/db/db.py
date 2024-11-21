from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from config import settings

database_url = settings.db.uri

engine = create_engine(database_url)
session_factory = sessionmaker(bind=engine)
session = scoped_session(session_factory)

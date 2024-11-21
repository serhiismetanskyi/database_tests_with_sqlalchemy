import factory

from src.db.db import session


class BaseFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        sqlalchemy_session = session
        sqlalchemy_session_persistence = "commit"

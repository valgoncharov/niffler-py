from sqlalchemy import create_engine, Engine, select
from sqlalchemy.orm import Session
from model.spend_db_model import Category


class SpendDb:

    engine: Engine

    def __init__(self, db_url: str):
        self.engine = create_engine(db_url, pool_size=10, max_overflow=20)

    def get_user_categories(self, username: str):
        with Session(self.engine) as session:
            statement = select(Category).where(Category.username == username)
            return session.exec(statement).all()

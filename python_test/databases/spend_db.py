from typing import Sequence
from sqlalchemy import create_engine, Engine, select
from sqlalchemy.orm import Session
from model.db.spend import Category


class SpendDb:

    engine: Engine

    def __init__(self, db_url: str):
        self.engine = create_engine(db_url, pool_size=10, max_overflow=20)

    def get_user_categories(self, username: str) -> Sequence[Category]:
        with Session(self.engine) as session:
            statement = select(Category).where(Category.username == username)
            return session.exec(statement).all()

    def delete_category(self, category_id: int):
        with Session(self.engine) as session:
            category = session.get(Category, category_id)
            session.delete(category)
            session.commit()

    def delete_spends(self, spend_ids: list[str]):
        with Session(self.engine) as session:
            statement = select(Spend).where(Spend.id.in_(spend_ids))
            session.exec(statement).all()
            session.commit()

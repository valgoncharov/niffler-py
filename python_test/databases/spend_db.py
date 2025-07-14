from typing import Sequence
from sqlalchemy import create_engine, Engine
from sqlmodel import Session, select
from python_test.model.db.spend import Category, Spend


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

    def get_category_by_id(self, category_id: str) -> Category:
        with Session(self.engine) as session:
            statement = select(Category).where(Category.id == category_id)
            return session.exec(statement).first()

    def get_spend_by_id(self, spend_id: str) -> Spend:
        with Session(self.engine) as session:
            statement = select(Spend).where(Spend.id == spend_id)
            return session.exec(statement).first()

    def delete_categories_by_ids(self, categories_ids: list[str]):
        for category_id in categories_ids:
            self.delete_category(category_id)
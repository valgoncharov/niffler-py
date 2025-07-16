from typing import Sequence

import allure
from allure_commons.types import AttachmentType
from sqlalchemy import create_engine, Engine, event
from sqlmodel import Session, select
from python_test.model.db.spend import Category, Spend


class SpendDb:

    engine: Engine

    def __init__(self, db_url: str):
        self.engine = create_engine(db_url, pool_size=10, max_overflow=20)
        event.listen(self.engine, "do_execute", fn=self.attach_sql)

    @staticmethod
    def attach_sql(cursor, statement, parameters, context):
        statement_with_params = statement % parameters
        name = statement.split(" ")[0] + " " + context.engine.url.database
        allure.attach(statement_with_params, name=name, attachment_type=AttachmentType.TEXT)

    @allure.step("Получить все категории пользователя из БД")
    def get_user_categories(self, username: str) -> Sequence[Category]:
        with Session(self.engine) as session:
            statement = select(Category).where(Category.username == username)
            return session.exec(statement).all()

    @allure.step("Удалить категорию из БД")
    def delete_category(self, category_id: int):
        with Session(self.engine) as session:
            category = session.get(Category, category_id)
            session.delete(category)
            session.commit()

    @allure.step("Удалить расход из БД")
    def delete_spends(self, spend_ids: list[str]):
        with Session(self.engine) as session:
            statement = select(Spend).where(Spend.id.in_(spend_ids))
            session.exec(statement).all()
            session.commit()

    @allure.step("Получиие категории из БД")
    def get_category_by_id(self, category_id: str) -> Category:
        with Session(self.engine) as session:
            statement = select(Category).where(Category.id == category_id)
            return session.exec(statement).first()

    @allure.step("Получиние id расхода из БД")
    def get_spend_by_id(self, spend_id: str) -> Spend:
        with Session(self.engine) as session:
            statement = select(Spend).where(Spend.id == spend_id)
            return session.exec(statement).first()

    @allure.step("Удалеине списка ids категорий из БД")
    def delete_categories_by_ids(self, categories_ids: list[str]):
        for category_id in categories_ids:
            self.delete_category(category_id)

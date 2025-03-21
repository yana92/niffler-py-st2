from typing import Sequence

from sqlalchemy import create_engine, Engine
from sqlmodel import Session, select

from models.spend import Category, Spend


class SpendDb:

    engine: Engine

    def __init__(self, db_url: str):
        self.engine = create_engine(db_url)

    def get_user_categories(self, username: str) -> Sequence[Category]:
        with Session(self.engine) as session:
            statement = select(Category).where(Category.username == username)
            return session.exec(statement).all()

    def delete_category(self, id: str):
        with Session(self.engine) as session:
            category = session.get(Category, id)
            session.delete(category)
            session.commit()

    def get_category_spends(self, category_id: str) -> Sequence[Spend]:
        with Session(self.engine) as session:
            statement = select(Spend).where(Spend.category_id == category_id)
            return session.exec(statement).all()

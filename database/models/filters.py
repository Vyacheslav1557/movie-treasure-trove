import sqlalchemy
from database.models.db_session import SqlAlchemyBase


class Filter(SqlAlchemyBase):
    __tablename__ = 'filters'

    filter_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    country = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    genre = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    type = sqlalchemy.Column(sqlalchemy.String, default="ALL", nullable=False)
    rating_from = sqlalchemy.Column(sqlalchemy.Integer, default=5, nullable=False)
    rating_to = sqlalchemy.Column(sqlalchemy.Integer, default=10, nullable=False)
    year_from = sqlalchemy.Column(sqlalchemy.Integer, default=1000, nullable=False)
    year_to = sqlalchemy.Column(sqlalchemy.Integer, default=3000, nullable=False)

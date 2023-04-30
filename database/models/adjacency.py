import sqlalchemy
from database.models.db_session import SqlAlchemyBase


class Adjacency(SqlAlchemyBase):
    __tablename__ = 'adjacency'

    film_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    title = sqlalchemy.Column(sqlalchemy.String)

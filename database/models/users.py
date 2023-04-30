import sqlalchemy
from database.models.db_session import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = 'users'

    telegram_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    filter_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("filters.filter_id"))
    liked = sqlalchemy.Column(sqlalchemy.String, default="", nullable=False)
    disliked = sqlalchemy.Column(sqlalchemy.String, default="", nullable=False)
    wanna_watch = sqlalchemy.Column(sqlalchemy.String, default="", nullable=False)
    favourite = sqlalchemy.Column(sqlalchemy.String, default="", nullable=False)
    registered_datetime = sqlalchemy.Column(sqlalchemy.DateTime)

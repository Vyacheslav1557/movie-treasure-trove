from database.models import db_session
from database.models.all_models import User, Filter, Adjacency
from datetime import datetime


class BotUserQuery:
    def __init__(self, telegram_id: int) -> None:
        self.session = db_session.create_session()
        self.telegram_id = telegram_id

    def create_user(self):
        user = User()
        search_filter = Filter()

        self.session.add(search_filter)
        self.session.commit()

        user.telegram_id = self.telegram_id
        user.filter_id = search_filter.filter_id
        user.registered_datetime = datetime.now()

        self.session.add(user)
        self.session.commit()

        return self

    def register(self):
        user = self.user
        if user is None:
            self.create_user()
        return self

    @property
    def user(self):
        return self.session.query(User).filter(User.telegram_id == self.telegram_id).first()

    @property
    def filter(self):
        filter_id = self.user.filter_id
        return self.session.query(Filter).filter(Filter.filter_id == filter_id).first()

    def commit(self):
        self.session.commit()
        return self

    def close(self):
        self.session.close()


class BotFilmQuery:
    def __init__(self, film_id: int) -> None:
        self.session = db_session.create_session()
        self.film_id = film_id

    @property
    def film_title(self) -> Adjacency:
        film_title = self.session.query(Adjacency).filter(Adjacency.film_id == self.film_id).first()
        if film_title is None:
            film_title = Adjacency(film_id=self.film_id, title="")
            self.session.add(film_title)
        return film_title

    @film_title.setter
    def film_title(self, title: str) -> None:
        self.film_title.title = title

    def commit(self):
        self.session.commit()
        return self

    def close(self):
        self.session.close()

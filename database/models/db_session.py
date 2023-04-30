import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session
from sqlalchemy.orm import declarative_base

SqlAlchemyBase = declarative_base()
__factory: Session | None = None

PATH_TO_DB = "database/bot_database.db"


def global_init(db_file: str = PATH_TO_DB):
    global __factory
    if __factory is not None:
        return
    if not db_file or not db_file.strip():
        raise Exception("Необходимо указать файл базы данных.")
    conn_str = f'sqlite:///{db_file.strip()}?check_same_thread=False'
    engine = sa.create_engine(conn_str, echo=False)
    __factory = orm.sessionmaker(bind=engine)
    SqlAlchemyBase.metadata.create_all(engine)


def create_session(db_file: str = PATH_TO_DB) -> Session:
    global __factory
    if __factory is None:
        global_init(db_file)
    return __factory()

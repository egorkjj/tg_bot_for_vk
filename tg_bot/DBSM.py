from environs import Env
from sqlalchemy import create_engine, Column, Integer, String, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

env = Env()
env.read_env(".env")
user = env.str("DB_USER")
passw = env.str("DB_PASSWORD")
host = env.str("DB_HOST")
name = env.str("DB_NAME")


DATABASE_URL = f"postgresql+psycopg2://{user}:{passw}{host}/{name}"

# Создание объекта Engine
engine = create_engine(DATABASE_URL)

# Создание базового класса для моделей
Base = declarative_base()

# Определение модели User
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    step = Column(Integer, nullable=True)


class Links(Base):
    __tablename__ = "links"
    id = Column(Integer, primary_key=True, autoincrement=True)
    link = Column(String(255), nullable=True)


def all_user() -> list[dict]:
    arr = []
    Session = sessionmaker()
    session = Session(bind = engine)
    users = session.query(User).all()
    session.close()
    for i in users:
        arr.append({
            "id": i.id,
            "user": i.username,
            "step": i.step
        })
    
    for i in range(len(arr) - 1):
        for j in range(len(arr) - 1 - i):
            if arr[j]["id"] > arr[j + 1]["id"]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]

    return arr


def all_link() -> list[dict]:
    arr = []
    Session = sessionmaker()
    session = Session(bind = engine)
    users = session.query(Links).all()
    session.close()
    for i in users:
        arr.append({
            "id": i.id,
            "link": i.link
        })
    return arr


def delete_link(id) -> None:
    Session = sessionmaker()
    session = Session(bind = engine)
    session.query(Links).filter(Links.id == id).delete()
    session.commit()
    session.close()
    return 


def add_link(link) -> None:
    Session = sessionmaker()
    session = Session(bind = engine)
    new_link = Links(link = link)
    session.add(new_link)
    session.commit()
    session.close()
    return


def delete_users_range(start, end) -> None:
    Session = sessionmaker()
    session = Session(bind = engine)
    for i in range(start, end+1):
        session.query(User).filter(User.id == i).delete()
        session.commit()
    session.close()
    return




Base.metadata.create_all(engine)

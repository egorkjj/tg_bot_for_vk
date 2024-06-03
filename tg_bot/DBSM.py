from environs import Env
from sqlalchemy import create_engine, Column, Integer, String, Sequence, Boolean
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
    message_sent = Column(Boolean, nullable=True)
    no_stat = Column(Boolean, nullable = True)

class Links(Base):
    __tablename__ = "links"
    id = Column(Integer, primary_key=True, autoincrement=True)
    link = Column(String(255), nullable=True)

class time_loop(Base): #временная шкала для отчетов
    __tablename__ = "time_loop"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    step2 = Column(String(50), nullable=True)
    step3 = Column(String(50), nullable=True)
    step4 = Column(String(50), nullable=True)
    step5 = Column(String(50), nullable=True)
    step6 = Column(String(50), nullable=True)
    step7 = Column(String(50), nullable=True)
    step10 = Column(String(50), nullable=True)
    no_stat = Column(Boolean, nullable = True)



def all_user() -> list[dict]:
    arr = []
    Session = sessionmaker()
    session = Session(bind = engine)
    users = session.query(User).filter(User.no_stat == False).all()
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

#
def add_link(link) -> None:
    Session = sessionmaker()
    session = Session(bind = engine)
    new_link = Links(link = link)
    session.add(new_link)
    session.commit()
    session.close()
    return

#удаление пользователей из статы
def delete_users_range(start, end) -> None:
    Session = sessionmaker()
    session = Session(bind = engine)
    try:
        for i in range(start, end+1):
            curr = session.query(User).filter(User.id == i).first()
            curr.no_stat = True
            session.commit()
    except:
        pass
    session.close()
    return


def all_time_loop() -> list[dict]:
    arr = []
    Session = sessionmaker()
    session = Session(bind = engine)
    loops = session.query(time_loop).filter(time_loop.no_stat == False).all()
    session.close()
    for i in loops:
        arr.append({
            "id": i.id,
            "user": i.username,
            "step2": i.step2 if i.step2 != None else "Не дошел",
            "step3": i.step3 if i.step3 != None else "Не дошел",
            "step4": i.step4 if i.step4 != None else "Не дошел",
            "step5": i.step5 if i.step5 != None else "Не дошел",
            "step6": i.step6 if i.step6 != None else "Не дошел",
            "step7": i.step7 if i.step7 != None else "Не дошел",
            "step10": i.step10 if i.step10 != None else "Не дошел"
        })
    for i in range(len(arr) - 1):
        for j in range(len(arr) - 1 - i):
            if arr[j]["id"] > arr[j + 1]["id"]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

def delete_loop_range(start, end) -> None:
    Session = sessionmaker()
    session = Session(bind = engine)
    try:
        for i in range(start, end+1):
            curr = session.query(time_loop).filter(time_loop.id == i).first()
            curr.no_stat = True
            session.commit()
    except: 
        pass
    session.close()

Base.metadata.create_all(engine)

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

def create_session():
    engine = create_engine('sqlite:///data/forumvision.db',
                echo=False,
                connect_args={'check_same_thread': False})
    session = Session(engine)

    return engine, session
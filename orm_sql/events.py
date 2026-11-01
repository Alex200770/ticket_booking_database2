from config import get_database_url
from database import get_engine
from sqlalchemy import Engine, select
from sqlalchemy.orm import Session

from models import Event
from orm_sql.init_db import seet_data


def list_events(engine: Engine) -> List[Event]:
    with Session(engine) as session:
        statement = select(Event).order_by(Event.id)
        return list(session.scalars(statement))

if __name__ == '__main__':
    db_url = get_database_url()
    engine = get_engine(db_url)
    events = list_events(engine)

    for event in events:
        print(event.id, event.title, event.starts_at)
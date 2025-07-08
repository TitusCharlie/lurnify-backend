from app.core.database import init_db, engine
from sqlmodel import inspect

def test_db_init():
    init_db()
    inspector = inspect(engine)
    assert inspector is not None
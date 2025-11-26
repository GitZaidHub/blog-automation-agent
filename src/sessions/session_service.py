import asyncio
import os
import json
import logging
from sqlalchemy import create_engine, Table, Column, String, MetaData, Text
from sqlalchemy.sql import select, insert, update
from sqlalchemy.exc import NoResultFound

logger = logging.getLogger(__name__)

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./data/db.sqlite3")

# Ensure database directory exists
if "sqlite" in DATABASE_URL:
    try:
        # Extract path from URL (handle sqlite:/// and sqlite+aiosqlite:///)
        db_path = DATABASE_URL.split("///")[-1]
        db_dir = os.path.dirname(db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir)
            logger.info(f"Created database directory: {db_dir}")
    except Exception as e:
        logger.error(f"Failed to create database directory: {e}")

# Light persist via SQLAlchemy synchronous engine for simplicity
engine = create_engine(str(DATABASE_URL).replace("+aiosqlite", ""), connect_args={"check_same_thread": False})
metadata = MetaData()
sessions_table = Table(
    "sessions",
    metadata,
    Column("sid", String, primary_key=True),
    Column("payload", Text, nullable=False),
    Column("state", String, nullable=False),
    Column("data", Text, nullable=False),
)
metadata.create_all(engine)

class SessionService:
    def __init__(self):
        self._inmem_tasks = {}

    def create_session(self, sid: str, payload: dict):
        with engine.connect() as conn:
            conn.execute(insert(sessions_table).values(
                sid=sid, payload=json.dumps(payload), state="running", data=json.dumps({})
            ))
            conn.commit()
        logger.info(f'{{"event":"session_created","sid":"{sid}"}}')

    def set_task(self, sid: str, task):
        self._inmem_tasks[sid] = task

    def set_state(self, sid: str, state: str):
        with engine.connect() as conn:
            conn.execute(update(sessions_table).where(sessions_table.c.sid == sid).values(state=state))
            conn.commit()

    def update(self, sid: str, data: dict):
        with engine.connect() as conn:
            res = conn.execute(select(sessions_table.c.data).where(sessions_table.c.sid == sid)).fetchone()
            cur = json.loads(res[0]) if res and res[0] else {}
            cur.update(data)
            conn.execute(update(sessions_table).where(sessions_table.c.sid == sid).values(data=json.dumps(cur)))
            conn.commit()

    def get_session_payload(self, sid: str):
        with engine.connect() as conn:
            res = conn.execute(select(sessions_table.c.payload).where(sessions_table.c.sid == sid)).fetchone()
            return json.loads(res[0])

    def get_session(self, sid: str):
        with engine.connect() as conn:
            res = conn.execute(select(sessions_table.c.data).where(sessions_table.c.sid == sid)).fetchone()
            return json.loads(res[0]) if res and res[0] else {}

    def get_status(self, sid: str):
        with engine.connect() as conn:
            r = conn.execute(select(sessions_table.c.state, sessions_table.c.data).where(sessions_table.c.sid == sid)).fetchone()
            if not r:
                return {"state": "not_found"}
            state, data = r
            return {"state": state, "data": json.loads(data) if data else {}}

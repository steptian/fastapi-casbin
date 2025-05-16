from celery import Celery
from sqlalchemy import create_engine, text
import os
from datetime import datetime

app = Celery('tasks', broker=os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0'))
DB_URL = os.getenv('CASBIN_DB_URL', 'sqlite:///casbin.db')

@app.task
def clean_expired_policies():
    engine = create_engine(DB_URL)
    now_str = datetime.now().isoformat()
    with engine.connect() as conn:
        conn.execute(text("""
            DELETE FROM casbin_rule WHERE expire_at IS NOT NULL AND expire_at != '*' AND expire_at < :now
        """), {"now": now_str}) 
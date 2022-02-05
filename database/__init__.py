import logging
from gino import Gino

from loader import POSTGRES_URI

logging.getLogger('gino.engine._SAEngine').setLevel(logging.ERROR)

db: Gino = Gino()


async def connect_db() -> None:
    await db.set_bind(POSTGRES_URI)
    await db.gino.create_all()
    logging.info('Connected to DB')

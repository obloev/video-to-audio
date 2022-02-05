import logging

from database import connect_db
from loader import client, ADMIN
from plugins import set_plugins


async def on_startup():
    bot = await client.get_me()
    logging.info(f'{bot.first_name} [@{bot.username}]')
    await connect_db()
    set_plugins()
    await client.send_message(ADMIN, 'Bot launched')

if __name__ == "__main__":
    client.parse_mode = 'HTML'
    client.start()
    client.loop.run_until_complete(on_startup())
    client.run_until_disconnected()

from datetime import datetime, timezone

import aiosqlite
import time
from loguru import logger

create_users_table_users = ("CREATE TABLE IF NOT EXISTS users (telegram_id TEXT, username TEXT, name TEXT, "
                            "dates TEXT, number_of_requests INT);")


class Database:
    def __init__(self):
        self.db_path = "users.db"
        self.connection = None

    async def connect(self):
        try:
            if not self.connection:
                self.connection = await aiosqlite.connect(self.db_path)
                await self.connection.execute("PRAGMA journal_mode=WAL;")
                await self.connection.commit()
            """Подключение к базе данных."""
            return self.connection
        except Exception as e:
            logger.exception('Ошибка в database/Database().connect', e)

    async def close(self):
        """Закрывает подключение к базе данных."""
        if self.connection:
            await self.connection.close()
            self.connection = None

    async def chek_tables(self):
        conn = await self.connect()
        try:
            await conn.execute(create_users_table_users)
            await conn.commit()
        except Exception as e:
            logger.exception('Ошибка в database/Database().chek_tables', e)

    async def search_in_table(self, search_telegram_id, table="users"):
        conn = await self.connect()
        try:
            async with conn.execute(f"SELECT * FROM {table} WHERE telegram_id = ?", (search_telegram_id,)) as cursor:
                result = await cursor.fetchall()
                return [True, result] if result else False
        except Exception as e:
            logger.exception('Ошибка в database/Database().search_in_table', e)

    async def add_user(self, update_telegram_id, update_username, update_name, update_dates):
        conn = await self.connect()
        try:
            await conn.execute(
                f"INSERT INTO users (telegram_id, username, name, dates, number_of_requests) "
                f"VALUES (?, ?, ?, ?, ?);",
                (update_telegram_id, update_username, update_name, update_dates, 1),
            )
            await conn.commit()
        except Exception as e:
            logger.exception('Ошибка в database/Database().add_user', e)
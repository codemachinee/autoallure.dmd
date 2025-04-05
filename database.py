import aiosqlite
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
                "INSERT INTO users (telegram_id, username, name, dates, number_of_requests) "
                "VALUES (?, ?, ?, ?, ?);",
                (update_telegram_id, update_username, update_name, update_dates, 1),
            )
            await conn.commit()
        except Exception as e:
            logger.exception('Ошибка в database/Database().add_user', e)

    async def update_table(self, telegram_id, update_dates=None,
                           update_number_of_requests=None):
        try:
            conn = await self.connect()
            if update_dates is not None:
                await conn.execute("UPDATE users SET dates=? WHERE telegram_id=?", (update_dates, telegram_id))
            if update_number_of_requests is not None:
                await conn.execute("UPDATE users SET number_of_requests=? WHERE telegram_id=?",
                                   (update_number_of_requests, telegram_id))
            await conn.commit()
        except Exception as e:
            logger.exception('Ошибка в database/Database().update_table', e)

    async def delete_all_users(self, table='users'):
        conn = await self.connect()
        try:
            await conn.execute(f'DELETE FROM {table}')
            await conn.commit()
        except Exception as e:
            logger.exception('Ошибка в database/Database().delete_all_users', e)

    async def return_base_data(self):
        conn = await self.connect()
        try:
            async with conn.execute("SELECT telegram_id, username, name, dates, number_of_requests "
                                    "FROM users") as cursor:
                rows = await cursor.fetchall()
                if len(rows) == 0:
                    return False
                return rows
        except Exception as e:
            logger.exception('Ошибка в database/Database().return_base_data', e)


db = Database()

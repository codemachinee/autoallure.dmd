import asyncio

from passwords import *


class Admin_acc:
    def __init__(self):
        self.__admin = kostya

    async def get_admin(self):
        return self.__admin

    async def set_admin(self, value):
        self.__admin = value


admin_class = Admin_acc()


async def main():
    print(await admin_class.get_admin())  # Выведет "kostya"
    await admin_class.set_admin("igor")  # Меняем значение
    print(await admin_class.get_admin())  # Выведет "igor"


asyncio.run(main())
import asyncio

from passwords import *


class Admin_acc:
    def __init__(self):
        self.admin = kostya

    async def get_admin(self):
        return self.admin

    async def set_admin(self, value):
        self.admin = value


admin_class = Admin_acc()
admin_account = admin_class.admin

asyncio.run(admin_class.set_admin("test"))
print(admin_account)
print(admin_class.admin)
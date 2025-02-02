import asyncio
import json

import aiofiles


async def test():
    async with aiofiles.open('price.json', "r", encoding="utf-8") as file:
        content = await file.read()
        data = json.loads(content)
        print(list(data.keys()))


asyncio.run(test())
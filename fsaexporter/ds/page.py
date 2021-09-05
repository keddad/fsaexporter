import asyncio

import fsaexporter.utils as utils
from fsaexporter.ds.declaration import Declaration


class DeclarationPage:

    def __init__(self):
        self.declarations = []

    def __iter__(self):
        return self.declarations

    def empty(self):
        return len(self.declarations) == 0

    @classmethod
    async def init(cls, payload: dict, page: int, session: utils.FsaDownloader):
        payload["page"] = page
        data = (await session.post("https://pub.fsa.gov.ru/api/v1/rds/common/declarations/get", payload))

        dp = DeclarationPage()
        dp.declarations = await asyncio.gather(*[Declaration.init(x["id"], session) for x in data["items"]])

        return dp

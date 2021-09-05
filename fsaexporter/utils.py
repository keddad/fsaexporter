import atexit
from datetime import datetime

import aiohttp
import aiohttp.web
from tenacity import retry, stop_after_attempt, wait_exponential


def datetime_to_fsa(d: datetime.date):
    if not d:
        return None

    return d.strftime("%Y-%m-%d")


def fsa_to_datetime(s: str):
    if not s:
        return None

    return datetime.strptime(s, "%Y-%m-%d")


class FsaDownloader:
    """
    Downloads anything from FSA API. If request fails with HTTP 401, retries request with new Header/Cookies
    """

    def __init__(self):
        self.session = aiohttp.ClientSession()
        self.headers = {}
        atexit.register(self.destructor)

    def destructor(self):
        self.session.close()

    async def login(self):
        login_r = await self.session.post("https://pub.fsa.gov.ru/login",
                                          json={"username": "anonymous", "password": "hrgesf7HDR67Bd"})
        self.headers["Authorization"] = login_r.headers["Authorization"]

    @retry(stop=stop_after_attempt(10), wait=wait_exponential(multiplier=1, min=1, max=10))
    async def get(self, url: str, data: dict, retry=False):
        req = await self.session.get(url, json=data, headers=self.headers)

        if req.status == 401 or req.status == 403:
            if retry:
                raise RuntimeError

            await self.login()

            return await self.get(url, data, retry=True)

        return await req.json()

    @retry(stop=stop_after_attempt(10), wait=wait_exponential(multiplier=1, min=1, max=10))
    async def post(self, url: str, data: dict, retry=False):
        req = await self.session.post(url, json=data, headers=self.headers)

        if req.status == 401 or req.status == 403:
            if retry:
                raise RuntimeError

            await self.login()

            return await self.post(url, data, retry=True)

        return await req.json()

import asyncio

import tqdm
from aiohttp import ClientSession
import requests
from sqlalchemy import text

from WtfAspirator.src.Objects.Film import Film
from WtfAspirator.src.Services.Service import ServiceTMDB


class ServiceFilmAsync(ServiceTMDB):

    def __init__(self, session_orm):
        super().__init__()
        self.orm_session = session_orm
        self.p_bar = None

    async def _fetch(self, p_id, session):
        url = self.base_url + "movie/" + str(p_id) + "?api_key=" + self.api_key + "&language=" + self.language + "&append_to_response=casts"
        self.p_bar.update()
        async with session.get(url) as reponse:
            if reponse.status == 200:
                json = await reponse.json()
                return Film(json).save(self.orm_session)

    async def _bound_fetch(self, sem, pid, session):
        async with sem:
            await self._fetch(pid, session)

    async def run_fetching(self, number: int = None, report_progress: bool = True):
        tasks = []
        if self.delta == 0:
            return
        if number is None:
            number = self.delta
        else:
            if (self.min + number) > self.max:
                number = self.max - self.min
        if report_progress:
            self.p_bar = tqdm.tqdm(total=number)
        async with ClientSession() as session:
            sem = asyncio.Semaphore(10)
            for i in range(self.min, self.min + number):
                task = asyncio.ensure_future(self._bound_fetch(sem, i, session))
                tasks.append(task)
            for task in await asyncio.gather(*tasks):
                print(task)

    @property
    def max(self):
        response = requests.get(self.base_url + "movie/latest?api_key=" + self.api_key + "&language=" + self.language + "&append_to_response=casts")
        if response.status_code == 200:
            video = Film(response.json())
            return video.id_video

    @property
    def min(self):
        return (self.orm_session.query(Film).order_by(text("id_video desc, id_video")).first().id_video + 1)if self.orm_session.query(Film).count() > 0 else 0

    @property
    def delta(self):
        return self.max - self.min






import asyncio

from .AbstractController import AbstractContoller
from ..AsyncService.ServiceSerieAsync import ServiceSerieAsync
from ..Objects.Serie import Serie
from ..Services.SerieService import SerieService
from sqlalchemy import text


class SerieControllerAsync(AbstractContoller):

    def __init__(self,  session):
        super().__init__(session)
        self.serviceFilm = SerieService()
        self.serviceFilmAsync = ServiceSerieAsync()
        self.model = Serie

    '''
    Permet prend le dernier id des séries en base de données.
    Et insert d'autres séries qui n'existe pas en base.
    '''
    def post(self, nb_series: int):
        dernier_id = self.session.query(Serie).order_by(text("id_video desc, id_video")).first().id_video if self.session.query(Serie).count() > 0 else 0
        last_tmdb_id = self.serviceSerie.get_last_inserted().id_video
        if dernier_id + nb_series > last_tmdb_id:
            nb_series = last_tmdb_id - dernier_id
        loop = asyncio.get_event_loop()
        urls = ["https://api.themoviedb.org/3/tv/" + str(p_id) + "?api_key=6a3276ee2f7c509f53b55cd3d576030c&language=FR" for p_id in range(dernier_id + 1, nb_series)]
        results = loop.run_until_complete(self.serviceSerieAsync.get(urls))
        for result in results:
            if result is not None:
                Serie(result).save(self.session)

    def get(self, *args, **kwargs):
        pass

    def get_queryset(self):
        return self.session.query(Serie).all()

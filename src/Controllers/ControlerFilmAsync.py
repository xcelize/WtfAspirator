import asyncio

from .AbstractController import AbstractContoller
from ..AsyncService.ServiceFilmAsync import ServiceFilmAsync
from ..Objects.Film import Film
from ..Services.VideoService import FilmService
from tqdm import tqdm
from sqlalchemy import text


class FilmControllerAsync(AbstractContoller):

    def __init__(self,  session):
        super().__init__(session)
        self.serviceFilm = FilmService()
        self.serviceFilmAsync = ServiceFilmAsync()
        self.model = Film

    '''
    Permet prend le dernier id des films en base de données.
    Et insert d'autres films qui n'existe pas en base.
    '''
    def post(self, nb_films: int):
        dernier_id = self.session.query(Film).order_by(text("id_video desc, id_video")).first().id_video if self.session.query(Film).count() > 0 else 0
        last_tmdb_id = self.serviceFilm.get_last_inserted().id_video
        if dernier_id + nb_films > last_tmdb_id:
            nb_films = last_tmdb_id - dernier_id
        loop = asyncio.get_event_loop()
        urls = ["https://api.themoviedb.org/3/movie/" + str(p_id) + "?api_key=6a3276ee2f7c509f53b55cd3d576030c&language=FR" for p_id in range(dernier_id + 1, nb_films)]
        results = loop.run_until_complete(self.serviceFilmAsync.get(urls))
        for result in results:
            if result is not None:
                Film(result).save(self.session)

    def get(self, *args, **kwargs):
        pass

    def get_queryset(self):
        return self.session.query(Film).all()

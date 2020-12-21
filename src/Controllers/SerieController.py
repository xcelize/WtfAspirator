from .AbstractController import AbstractContoller
from ..Objects.Serie import Serie
from ..Services.SerieService import SerieService
from tqdm import tqdm
from sqlalchemy import text


class SerieController(AbstractContoller):

    def __init__(self,  session):
        super().__init__(session)
        self.service = SerieService()
        self.model = Serie

    '''
    Permet prend le dernier id des séries en base de données.
    Et insert d'autres séries qui n'existe pas en base.
    '''
    def post(self, *args, **kwargs):
        last_bd_id: int = 0
        if self.session.query(self.model).count() > 0:
            last_bd_id = self.session.query(Serie).order_by(text("id_video desc, id_video")).first().id_video
        last_tmdb_id = self.service.get_last_inserted().id_video
        if last_bd_id < last_tmdb_id:
            for i in tqdm(range(last_bd_id + 1, last_tmdb_id, 1), desc="Progression"):
                try:
                    serie = self.service.get_by_id(i)
                    serie.save(self.session)
                except Exception as e:
                    pass

    def get(self, *args, **kwargs):
        pass

    def get_queryset(self):
        return self.session.query(Serie).all()




from sqlalchemy import Column, String, Integer, ForeignKey

from .Base import Base
from .baseORM import BaseORM


class Saison(Base, BaseORM):

    __tablename__ = "saisons"
    id_saison = Column(Integer, primary_key=True, autoincrement=False)
    nb_episode = Column(String)
    nom = Column(String)
    num_saison = Column(String)
    id_serie = Column(Integer, ForeignKey("series.id_video"))

    def __init__(self, json_objects):
        super().__init__(json_objects)

        self.id_saison: int = 0
        self.nb_episode: int = 0
        self.nom: str = ""
        self.num_saison: int = 0

        self.mapping_attr = {
            'id_saison': 'id',
            'nb_episode': 'episode_count',
            'nom': 'name',
            'num_saison': 'season_number'
        }
        self._assign_attr(json_objects)

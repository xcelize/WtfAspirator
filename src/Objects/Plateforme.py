from sqlalchemy import Column, String, Integer

from .Base import Base
from .baseORM import BaseORM


class Plateforme(Base, BaseORM):

    __tablename__ = "plateformes"
    id_plateforme = Column(Integer, primary_key=True, autoincrement=False)
    nom = Column(String)
    logo = Column(String)

    def __init__(self, json_object):
        super().__init__(json_object)
        self.id_plateforme: int = 0
        self.nom: str = ""
        self.logo: str = ""
        self.mapping_attr = {
            'id_plateforme': 'id',
            'nom': 'name',
            'logo': 'logo_path'
        }
        self._assign_attr(json_object)

from sqlalchemy import Column, String, Integer

from .Base import Base
from .baseORM import BaseORM


class Production(Base, BaseORM):

    __tablename__ = "productions"
    id_production = Column(Integer, primary_key=True, autoincrement=False)
    logo = Column(String)
    nom = Column(String)
    pays = Column(String)

    def __init__(self, json_object):
        super().__init__(json_object)
        self.id_production: int = 0
        self.logo: str = ""
        self.nom: str = ""
        self.pays: str = ""
        self.mapping_attr = {
            'id_production': 'id',
            'logo': 'logo_path',
            'nom': 'name',
            'pays': 'origin_country'
        }
        self._assign_attr(json_object)

    def __str__(self):
        return f'{self.id_production} -- {self.nom}'

    def Pk(self):
        return self.id_production

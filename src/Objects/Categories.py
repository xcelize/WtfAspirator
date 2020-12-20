from sqlalchemy import Column, String, Integer

from .Base import Base
from .baseORM import BaseORM


class Categorie(Base, BaseORM):

    __tablename__ = "categories"
    id_categ = Column(Integer, primary_key=True, autoincrement=False)
    libelle = Column(String)

    def __init__(self, json_object):
        super().__init__(json_object)
        self.id_categ = 0
        self.libelle = ""
        self.mapping_attr = {
            'id_categ': 'id',
            'libelle': 'name'
        }
        self._assign_attr(json_object)

    def __str__(self):
        return f'{self.libelle}'

    def getId(self):
        return self.id_categ

    @classmethod
    def Pk(cls):
        return cls.id_categ

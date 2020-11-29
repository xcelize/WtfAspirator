import time

from sqlalchemy.orm import object_session
from .Base import Base
from .baseORM import Session, engine, BaseORM
from sqlalchemy import Column, String, Integer, Date, Table, ForeignKey, event


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

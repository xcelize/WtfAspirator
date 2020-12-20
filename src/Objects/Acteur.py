from .Base import Base
from .baseORM import Session, engine, BaseORM
from sqlalchemy import Column, String, Integer, Float, Date, Table, ForeignKey, event
from sqlalchemy.orm import object_session


class Acteur(Base, BaseORM):

    __tablename__ = "acteurs"
    id_personne = Column(Integer, primary_key=True, autoincrement=False)
    nom = Column(String)
    photo_profil = Column(String)
    popularite = Column(Float)
    personnage = Column(String)

    def __init__(self, json_object):
        super().__init__(json_object)
        self.id_personne = 0
        self.nom = ""
        self.photo_profil = ""
        self.popularite = 0
        self.personnage = ""

        self.mapping_attr = {
            'id_personne': 'id',
            'nom': 'original_name',
            'photo_profil':'profile_path',
            'popularite': 'popularity',
            'personnage': 'character'
        }

        self._assign_attr(json_object)

    def __str__(self):
        return f'{self.nom}'

    def getId(self):
        return self.id_personne

    @classmethod
    def Pk(cls):
        return cls.id_personne

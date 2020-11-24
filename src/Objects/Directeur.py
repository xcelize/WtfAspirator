from .Base import Base
from .baseORM import Session, engine, BaseORM
from sqlalchemy import Column, String, Integer, Float, Date, Table, ForeignKey, event
from sqlalchemy.orm import object_session


class Directeur(Base, BaseORM):

    __tablename__ = "directeurs"
    id_personne = Column(Integer, primary_key=True, autoincrement=False)
    nom = Column(String)
    photo_profil = Column(String)
    popularite = Column(Float)
    departement = Column(String)
    job = Column(String)

    def __init__(self, json_object):
        super().__init__(json_object)
        self.id_personne = 0
        self.nom = ""
        self.photo_profil = ""
        self.popularite = 0
        self.departement = ""
        self.job = ""

        self.mapping_attr = {
            'id_personne': 'id',
            'nom': 'original_name',
            'photo_profil':'profile_path',
            'popularite': 'popularity',
            'departement': 'department',
            'job': 'job'
        }

        self._assign_attr(json_object)

    def __str__(self):
        return f'{self.nom}'
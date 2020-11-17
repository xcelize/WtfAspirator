from sqlalchemy import Column, String, Integer, Table, ForeignKey, event
from sqlalchemy.orm import relationship, object_session

from .Base import Base
from .Categories import Categorie
from .Production import Production
from .baseORM import BaseORM

movies_categorie_association = Table(
    'film_categories', BaseORM.metadata,
    Column('film_id', Integer, ForeignKey('films.id_video')),
    Column('categorie_id', Integer, ForeignKey('categories.id_categ'))
)
movies_production_association = Table(
    'film_productions', BaseORM.metadata,
    Column('film_id', Integer, ForeignKey('films.id_video')),
    Column('production_id', Integer, ForeignKey('productions.id_production'))
)


class Film(Base, BaseORM):

    __tablename__ = "films"
    id_video = Column(Integer, primary_key=True, autoincrement=False)
    titre = Column(String)
    date_sortie = Column(String)
    poster = Column(String)
    plot = Column(String)
    vo = Column(String)
    duree = Column(String)
    categories = relationship("Categorie", secondary=movies_categorie_association, cascade='all')
    productions = relationship("Production", secondary=movies_production_association)

    def __init__(self, json_object):
        super().__init__(json_object)
        self.id_video = 0
        self.titre = ""
        self.date_sortie = ""
        self.poster = ""
        self.plot = ""
        self.vo = ""
        self.duree = ""
        self.categories: [Categorie] = []
        self.productions: [Production] = []
        self.mapping_attr = {
            'id_video': 'id',
            'titre': 'title',
            'poster': 'poster_path',
            'plot': 'overview',
            'date_sortie': 'release_date',
            'duree': 'runtime',
            'vo': 'original_language',
        }
        self.mapping_nested = {
            'categories': {
                'json_attr': 'genres',
                'object_attr': self.categories,
                'model': Categorie,
            },
            'productions': {
                'json_attr': 'production_companies',
                'object_attr': self.productions,
                'model': Production
            }
        }
        self._assign_attr(json_object)
        self._assign_nested(json_object)

    def __str__(self):
        return f'{self.id_video}, {self.titre}, {self.vo}, {self.duree}, {self.plot}'

    def save(self, session):
        for k, categorie in enumerate(self.categories):
            if session.query(Film).filter(Categorie.id_categ == categorie.id_categ).count() > 0:
                self.categories[k] = session.query(Categorie).get(categorie.id_categ)
        for k, production in enumerate(self.productions):
            if session.query(Film).filter(Production.id_production == production.id_production).count() > 0:
                self.productions[k] = session.query(Production).get(production.id_production)
        session.add(self)
        session.commit()

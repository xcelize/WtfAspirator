from sqlalchemy import Column, String, Integer, Table, ForeignKey, inspect
from sqlalchemy.orm import relationship

from .Base import Base
from .Categories import Categorie
from .Plateforme import Plateforme
from .Production import Production
from .Saison import Saison
from .baseORM import BaseORM

series_categorie_association = Table(
    'serie_categories', BaseORM.metadata,
    Column('serie_id', Integer, ForeignKey('series.id_video')),
    Column('categorie_id', Integer, ForeignKey('categories.id_categ'))
)
serie_productions_association = Table(
    'serie_productions', BaseORM.metadata,
    Column('serie_id', Integer, ForeignKey('series.id_video')),
    Column('production_id', Integer, ForeignKey('productions.id_production'))
)
serie_plateformes_association = Table(
    'serie_plateformes', BaseORM.metadata,
    Column('serie_id', Integer, ForeignKey('series.id_video')),
    Column('plateforme_id', Integer, ForeignKey('plateformes.id_plateforme'))
)


class Serie(Base, BaseORM):

    __tablename__ = "series"
    id_video = Column(Integer, primary_key=True, autoincrement=False)
    titre = Column(String)
    date_sortie = Column(String)
    poster = Column(String)
    plot = Column(String)
    vo = Column(String)
    nb_saison = Column(Integer)
    categories = relationship("Categorie", secondary=series_categorie_association)
    productions = relationship("Production", secondary=serie_productions_association)
    plateformes = relationship("Plateforme", secondary=serie_plateformes_association)
    saisons = relationship("Saison")

    def __init__(self, json_object):
        super().__init__(json_object)
        self.session = inspect(self).session
        self.id_video = 0
        self.titre = ""
        self.date_sortie = ""
        self.poster = ""
        self.plot = ""
        self.vo = ""
        self.nb_saison = 0
        self.categories: [Categorie] = []
        self.productions: [Production] = []
        self.plateformes: [Plateforme] = []
        self.saisons: [Saison] = []

        self.mapping_attr = {
            'id_video': 'id',
            'titre': 'name',
            'date_sortie': 'first_air_date',
            'nb_saison': 'number_of_seasons',
            'plot': 'overview',
            'poster': 'poster_path',
            'vo': 'original_language'
        }

        self.mapping_nested = {
            'categories': {
                'json_attr': 'genres',
                'object_attr': self.categories,
                'model': Categorie
            },
            'productions': {
                'json_attr': 'production_companies',
                'object_attr': self.productions,
                'model': Production
            },
            'plateformes': {
                'json_attr': 'networks',
                'object_attr': self.plateformes,
                'model': Plateforme
            },
            'saisons': {
                'json_attr': 'seasons',
                'object_attr': self.saisons,
                'model': Saison
            }
        }
        self._assign_attr(json_object)
        self._assign_nested(json_object)

    def __str__(self):
        return f'{self.titre}'

    def save(self, session):
        for k, categorie in enumerate(self.categories):
            if session.query(Serie).filter(Categorie.id_categ == categorie.id_categ).count() > 0:
                self.categories[k] = session.query(Categorie).get(categorie.id_categ)
        for k, production in enumerate(self.productions):
            if session.query(Serie).filter(Production.id_production == production.id_production).count() > 0:
                self.productions[k] = session.query(Production).get(production.id_production)
        for k, plateforme in enumerate(self.plateformes):
            if session.query(Serie).filter(Plateforme.id_plateforme == plateforme.id_plateforme).count() > 0:
                self.plateformes[k] = session.query(Plateforme).get(plateforme.id_plateforme)
        session.add(self)
        session.commit()



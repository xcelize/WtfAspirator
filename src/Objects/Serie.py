from sqlalchemy.orm import relationship, object_session
from .Base import Base
from .Categories import Categorie
from .Production import Production
from .Plateforme import Plateforme
from .Acteur import Acteur
from .Equipe import Equipe
from .Saison import Saison
from .baseORM import Session, engine, BaseORM
from sqlalchemy import Column, String, Integer, Date, Table, ForeignKey, event

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
        self.acteurs: [Acteur] = []
        self.equipe: [Equipe] = []

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
            },
            'acteurs': {
                'json_attr': 'cast',
                'object_attr': self.acteurs,
                'model': Acteur
            },
            'equipe': {
                'json_attr': 'crew',
                'object_attr': self.equipe,
                'model': Equipe
            }
        }
        self._assign_attr(json_object)
        self._assign_nested(json_object)

    def __str__(self):
        return f'{self.titre}'

    def save(self, session):
        deliveryDataToTable(Categorie, Serie, 'id_categ', self.categories, session)
        deliveryDataToTable(Production, Serie, 'id_production', self.productions, session)
        deliveryDataToTable(Plateforme, Serie, 'id_plateforme', self.plateformes, session)
        deliveryDataToTable(Acteur, Serie, 'id_personne', self.acteurs, session)
        deliveryDataToTable(Equipe, Serie, 'id_personne', self.equipe, session)
        session.add(self)
        session.commit()



def deliveryDataToTable(table_destination, table_original, pk, nested_elements, session):
    for k, element in enumerate(nested_elements):
        if session.query(table_original).filter(table_destination[pk] == element[pk]).count() > 0:
            nested_elements[k] = session.query(table_destination).get(element[pk])


from .Categories import Categorie
from .Base import Base
from .Directeur import Directeur
from .Acteur import Acteur
from .Production import Production
from .baseORM import Session, engine, BaseORM
from sqlalchemy import Column, String, Integer, Date, Table, ForeignKey, event
from sqlalchemy.orm import relationship, object_session
import sqlalchemy.event

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
movies_acteur_association = Table(
    'film_acteurs', BaseORM.metadata,
    Column('film_id', Integer, ForeignKey('films.id_video')),
    Column('acteur_id', Integer, ForeignKey('acteurs.id_personne'))
)
movies_directeur_association = Table(
    'film_directeurs', BaseORM.metadata,
    Column('film_id', Integer, ForeignKey('films.id_video')),
    Column('directeur_id', Integer, ForeignKey('directeurs.id_personne'))
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
    acteurs = relationship("Acteur", secondary=movies_acteur_association)
    directeurs = relationship("Directeur", secondary=movies_directeur_association)

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
        self.acteurs: [Acteur] = []
        self.directeurs: [Directeur] = []

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
            },
            'acteurs': {
                'json_attr': 'cast',
                'object_attr': self.acteurs,
                'model': Acteur
            },
            'directeurs': {
                'json_attr': 'crew',
                'object_attr': self.directeurs,
                'model': Directeur
            }
        }
        self._assign_attr(json_object)
        self._assign_nested(json_object)

    def __str__(self):
        return f'{self.id_video}, {self.titre}, {self.vo}, {self.duree}, {self.plot}'

    def save(self, session):
        '''
        for k, categorie in enumerate(self.categories):
            if session.query(Film).filter(Categorie.id_categ == categorie.id_categ).count() > 0:
                self.categories[k] = session.query(Categorie).get(categorie.id_categ)
        for k, production in enumerate(self.productions):
            if session.query(Film).filter(Production.id_production == production.id_production).count() > 0:
                self.productions[k] = session.query(Production).get(production.id_production)
        '''
        deliveryDataToTable(Categorie, Film, 'id_categ', self.categories, session)
        deliveryDataToTable(Production, Film, 'id_production', self.productions, session)
        deliveryDataToTable(Acteur, Film, 'id_personne', self.directeurs, session)
        deliveryDataToTable(Directeur, Film, 'id_personne', self.directeurs, session)

        session.add(self)
        session.commit()


@event.listens_for(Film, 'before_insert')
def my_load_listener(mapper, connection, target):
    session = object_session(target)
    target.id_video = 100


def deliveryDataToTable(table_destination, table_original, pk, nested_elements, session):
    for k, element in enumerate(nested_elements):
        if session.query(table_original).filter(table_destination[pk] == element[pk]).count() > 0:
            nested_elements[k] = session.query(table_destination).get(element[pk])


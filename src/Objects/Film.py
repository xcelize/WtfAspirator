from .Categories import Categorie
from .Base import Base
from .Equipe import Equipe
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
movies_equipe_association = Table(
    'film_equipe', BaseORM.metadata,
    Column('film_id', Integer, ForeignKey('films.id_video')),
    Column('equipe_id', Integer, ForeignKey('equipe.id_personne'))
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
    equipe = relationship("Equipe", secondary=movies_equipe_association)

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
        self.equipe: [Equipe] = []

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
                'model': Categorie
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
            'equipe': {
                'json_attr': 'crew',
                'object_attr': self.equipe,
                'model': Equipe
            }
        }
        self._assign_attr(json_object)
        self._assign_nested(json_object)

    def __str__(self):
        return f'{self.id_video}, {self.titre}, {self.vo}, {self.duree}, {self.plot}'

    def Pk(self):
        return self.id_video

    def save(self, session):
        self.deliveryDataToTable(Categorie, Film, Categorie.id_categ, self.categories, session)
        self.deliveryDataToTable(Production, Film, Production.id_production, self.productions, session)
        self.deliveryDataToTable(Acteur, Film, Acteur.id_personne, self.acteurs, session)
        self.deliveryDataToTable(Equipe, Film, Equipe.id_personne, self.equipe, session)
        session.add(self)
        session.commit()

    def deliveryDataToTable(self, table_destination, table_original, pk, nested_elements, session):
        for k, element in enumerate(nested_elements):
            if session.query(table_original).filter(pk == element.Pk()).count() > 0:
                nested_elements[k] = session.query(table_destination).get(element.Pk())

@event.listens_for(Film, 'before_insert')
def my_load_listener(mapper, connection, target):
    session = object_session(target)
    target.id_video = 100






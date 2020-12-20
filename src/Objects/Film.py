from sqlalchemy import Column, String, Integer, Table, ForeignKey
from sqlalchemy.orm import relationship

from .Base import Base
from .Categories import Categorie
from .Production import Production
from .baseORM import BaseORM
from .Acteur import Acteur
from .Directeur import Directeur

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
movies_acteurs_association = Table(
    'film_acteurs', BaseORM.metadata,
    Column('film_id', Integer, ForeignKey('films.id_video')),
    Column('acteur_id', Integer, ForeignKey('acteurs.id_personne'))
)
movies_directeurs_association = Table(
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
    duree = Column(Integer)
    categories = relationship("Categorie", secondary=movies_categorie_association, cascade='all')
    productions = relationship("Production", secondary=movies_production_association)
    acteurs = relationship("Acteur", secondary=movies_acteurs_association)
    directeurs = relationship("Directeur", secondary=movies_directeurs_association)

    def __init__(self, json_object):
        super().__init__(json_object)
        self.id_video = 0
        self.titre = ""
        self.date_sortie = ""
        self.poster = ""
        self.plot = ""
        self.vo = ""
        self.duree = 0
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
        }
        self._assign_attr(json_object)

        self.append_to_list_object(self.acteurs, Acteur, json_object, 'casts', 'cast')
        self.append_to_list_object(self.directeurs, Directeur, json_object, 'casts', 'crew')

        self._assign_nested(json_object)

    def append_to_list_object(self, list_objects, model, json_object, key_json_1, key_json_2):
        """
        Pour les listes d'objets Acteur et Directeur.
        """
        for json in json_object[key_json_1][key_json_2]:
             obj = model(json)
             list_id_obj = self.list_id(list_objects)
             if obj.getId() not in list_id_obj:
                # pour directeur il faut vérifier en plus le département et le job.
                if isinstance(obj, Directeur) and obj.departement == 'Directing' and obj.job == 'Director':
                        list_objects.append(obj)
                else:
                    list_objects.append(obj)

    def list_id(self, list_data):
        ids = list()
        for data in list_data:
            data_id = data.id_personne
            ids.append(data_id)
        return ids

    def __str__(self):
        return f'id:{self.id_video}, titre:{self.titre}, duree: {self.duree}, plot:{self.plot}'

    def save(self, session):
        self.deliveryDataToTable(Film, Categorie, self.categories, session)
        self.deliveryDataToTable(Film, Production, self.productions, session)
        self.deliveryDataToTable(Film, Acteur, self.acteurs, session)
        self.deliveryDataToTable(Film, Directeur, self.directeurs, session)
        session.add(self)
        session.commit()


    def deliveryDataToTable(self, table_root, table_destination, list_data, session):
        for k, data in enumerate(list_data):
            if session.query(table_root).filter(table_destination.Pk() == data.getId()).count() > 0:
                list_data[k] = session.query(table_destination).get(data.getId())


from sqlalchemy import Column, String, Integer, Table, ForeignKey
from sqlalchemy.orm import relationship

from .Base import Base
from .Categories import Categorie
from .Plateforme import Plateforme
from .Production import Production
from .Saison import Saison
from .Acteur import Acteur
from .Directeur import Directeur
from .baseORM import BaseORM
from .Film import acteur_id_list_commun, directeur_id_list_commun, categ_id_list_commun, production_id_list_commun

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
serie_acteurs_association = Table(
    'serie_acteurs', BaseORM.metadata,
    Column('serie_id', Integer, ForeignKey('series.id_video')),
    Column('acteur_id', Integer, ForeignKey('acteurs.id_personne'))
)
serie_directeurs_association = Table(
    'serie_directeurs', BaseORM.metadata,
    Column('serie_id', Integer, ForeignKey('series.id_video')),
    Column('directeur_id', Integer, ForeignKey('directeurs.id_personne'))
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
    acteurs = relationship("Acteur", secondary=serie_acteurs_association)
    serie_directeurs_association = relationship("Directeur", secondary=serie_directeurs_association)

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
        self.directeurs: [Directeur] = []

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

        self.append_to_list_object(self.categories, categ_id_list_commun, Categorie, json_object, 'genres', None)
        self.append_to_list_object(self.productions, production_id_list_commun, Production, json_object,
                                   'production_companies', None)
        self.append_to_list_object(self.acteurs, acteur_id_list_commun, Acteur, json_object, 'credits', 'cast')
        self.append_to_list_object(self.directeurs, directeur_id_list_commun, Directeur, json_object, 'credits', 'crew')

        self._assign_nested(json_object)

    def append_to_list_object(self, list_objects, list_id_commun, model, json_object, key_json_1, key_json_2):
        """
        Pour les listes d'objets Categorie, Production, Acteur et Directeur
        """
        # Pour Categorie et Production
        if key_json_2 is None:
            for json in json_object[key_json_1]:
                obj = model(json)
                list_id_obj = self.list_id(list_objects)
                if obj.getId() not in list_id_obj and obj.getId() not in list_id_commun:
                    list_objects.append(obj)
                    list_id_commun.append(obj.getId())

        # Pour Acteur et Directeur
        else:
            for json in json_object[key_json_1][key_json_2]:
                obj = model(json)
                list_id_obj = self.list_id(list_objects)
                if obj.getId() not in list_id_obj and obj.getId() not in list_id_commun:
                    # pour directeur il faut vérifier en plus le département et le job.
                    if isinstance(obj, Directeur):
                        if obj.departement == 'Directing' and obj.job == 'Director':
                            list_objects.append(obj)
                            list_id_commun.append(obj.getId())
                    else:
                        list_objects.append(obj)
                        list_id_commun.append(obj.getId())

    def list_id(self, list_data):
        ids = list()
        for data in list_data:
            data_id = data.getId()
            ids.append(data_id)
        return ids


    def __str__(self):
        return f'{self.titre}'

    def save(self, session):
        self.deliveryDataToTable(Serie, Categorie, self.categories, session)
        self.deliveryDataToTable(Serie, Production, self.productions, session)
        self.deliveryDataToTable(Serie, Plateforme, self.plateformes, session)
        self.deliveryDataToTable(Serie, Acteur, self.acteurs, session)
        self.deliveryDataToTable(Serie, Directeur, self.directeurs, session)
        session.add(self)
        session.commit()

    def deliveryDataToTable(self, table_root, table_destination, list_data, session):
        for k, data in enumerate(list_data):
            if session.query(table_root).filter(table_destination.Pk() == data.getId()).count() > 0:
                list_data[k] = session.query(table_destination).get(data.getId())



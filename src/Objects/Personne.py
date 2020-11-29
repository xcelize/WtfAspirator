'''class Personne(BaseORM):

    __tablename__ = "personnes"
    id_personne = Column(Integer, primary_key=True, autoincrement=False)
    nom = Column(String)
    role = Column(String)
    type = Column(String)
    image_profil = Column(String)

    __mapper_args__ = {
        'polymorphic_identity': 'personnes',
        'polymorphic_on': type
    }

    def __init__(self):
        self.id_personne


class Personnel(Personne):
    __tablename__ = "personnels"
    id_personnel = Column(Integer, ForeignKey('personnes.id_personne'), primary_key=True)
    departement = Column(String)

    __mapper_args__ = {
        'polymorphic_identity': 'personnels',
    }


class Acteur(Personne):
    __tablename__ = "acteurs"
    id_acteur = Column(Integer, ForeignKey('personnes.id_personne'), primary_key=True)
    personnage = Column(String)

    __mapper_args__ = {
        'polymorphic_identity': 'personnels',
    }'''

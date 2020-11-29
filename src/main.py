from WtfAspirator.src.Objects.Categories import Categorie
from WtfAspirator.src.Objects.Film import Film
from WtfAspirator.src.Objects.Plateforme import Plateforme
from WtfAspirator.src.Objects.Serie import Serie
from WtfAspirator.src.Services.VideoService import (
    FilmService,
)
from WtfAspirator.src.Services.SerieService import (
    SerieService,
)
from WtfAspirator.src.Objects.baseORM import Session, engine, BaseORM

def lets_movies():
    list_video: [Film] = []

    service = FilmService()
    film1 = service.get_by_id(2)
    film2 = service.get_by_id(11)

    print(f'Film 1 - {len(film1.productions)}')
    print(f'Film 1 - {len(film1.categories)}')

    print(f'Film 2 - {len(film2.productions)}')
    print(f'Film 2 - {len(film2.categories)}')


def lets_tv():
    service = SerieService()
    serie1 = service.get_by_id(1)
    serie2 = service.get_by_id(2)

    print(f'{serie1}')
    print(f'Serie 1 - {len(serie1.productions)}')
    print(f'Serie 1 - {len(serie1.categories)}')

    print(f'Serie 2 - {len(serie2.productions)}')
    print(f'Serie 2 - {len(serie2.categories)}')

def testORM():
    import logging
    logging.basicConfig()
    logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
    BaseORM.metadata.create_all(engine)
    session = Session()
    serieService = SerieService()
    for i in range(1000):
        try:
            serie = serieService.get_by_id(i)
            serie.save(session)
        except Exception as e:
            print(e)

if __name__ == '__main__':
    testORM()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/



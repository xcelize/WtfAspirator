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
    BaseORM.metadata.create_all(engine)
    session = Session()
    service = SerieService()
    serie = service.get_by_id(2)
    session.add(serie)
    session.commit()


if __name__ == '__main__':
    testORM()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/


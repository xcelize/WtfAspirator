from WtfAspirator.src.Controllers.FilmController import FilmController
from WtfAspirator.src.Objects.baseORM import Session, engine, BaseORM
from PyInquirer import style_from_dict, Token, prompt, Separator

from WtfAspirator.src.Services.VideoService import FilmService

if __name__ == '__main__':
    import logging
    logging.basicConfig()
    logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
    service = FilmService()
    session = Session()
    BaseORM.metadata.create_all(engine)
    for i in range(100):
        try:
            film = service.get_by_id(i)
            film.save(session)
        except Exception as e:
            print(e)



import asyncio
import time
from tqdm import tqdm
from WtfAspirator.src.AsyncService.ServiceFilmAsync import ServiceFilmAsync
from WtfAspirator.src.Controllers.FilmController import FilmController
from WtfAspirator.src.Objects.Film import Film
from WtfAspirator.src.Objects.baseORM import Session, engine, BaseORM
from PyInquirer import style_from_dict, Token, prompt, Separator
from WtfAspirator.src.Services.VideoService import FilmService



def routineSync():
    service = FilmService()
    for i in range(100):
        try:
            serie = service.get_by_id(i)
            print(serie)
        except Exception as e:
            print(e)


def controller():
    BaseORM.metadata.create_all(engine)
    session = Session()
    s = ServiceFilmAsync(session)
    number = 1000
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(s.run_fetching())
    loop.run_until_complete(future)

if __name__ == '__main__':
    controller()
    """start_time = time.time()
    s = ServiceFilmAsync()
    BaseORM.metadata.create_all(engine)
    session = Session()
    loop = asyncio.get_event_loop()
    urls = ["https://api.themoviedb.org/3/movie/" + str(p_id) + "?api_key=6a3276ee2f7c509f53b55cd3d576030c&language=FR" for p_id in range(1000)]
    result = await asyncio.wait(urls, return_when=asyncio.FIRST_COMPLETED)
    print(result)
    results = loop.run_until_complete(s.get(urls))
    for result in tqdm(results):
        if result is not None:
            Film(result).save(session)
    print("--- %s seconds ---" % (time.time() - start_time))"

    start_time = time.time()
    tasks = asyncio.run(routine())
    for tasks in tasks:
        if not isinstance(tasks, Exception):
            print(tasks.id_video)
    print(tasks)
    print("--- %s seconds ---" % (time.time() - start_time))"""



import asyncio
import sys

from WtfAspirator.src.AsyncService.ServiceFilmAsync import ServiceFilmAsync
from WtfAspirator.src.Controllers.FilmController import FilmController
from WtfAspirator.src.Controllers.ControlerFilmAsync import FilmControllerAsync
from WtfAspirator.src.Objects.baseORM import Session, engine, BaseORM
from PyInquirer import style_from_dict, Token, prompt, Separator
from pprint import pprint


class Console:

    style = style_from_dict({
        Token.Separator: '#cc5454',
        Token.QuestionMark: '#673ab7 bold',
        Token.Selected: '#cc5454',  # default
        Token.Pointer: '#673ab7 bold',
        Token.Instruction: '',  # default
        Token.Answer: '#f44336 bold',
        Token.Question: '',
    })

    def __init__(self, p_session: Session):
        self.film_service = ServiceFilmAsync(p_session)
        self.active = True
        self.questions = [
        {
            'type': 'list',
            'message': 'Selectionner une action',
            'name': "route",
            'choices': [
                Separator('On aspire quoi ?'),
                {
                    'name': "film"
                },
                {
                    'name': "serie"
                }
            ]
        },
        {
            'type': 'list',
            'message': 'Voulez vous recommencer?',
            'name': "again",
            'choices': [
                {
                    'name': "oui"
                },
                {
                    'name': "non"
                }
            ]
        },
        {
            'type': 'list',
            'message': 'Nombre de film à aspirer?',
            'name': "nb_films",
            'choices': [
                {
                    'name': "10"
                },
                {
                    'name': "100"
                },
                {
                    'name': "1000"
                },
                {
                    'name': "10000"
                },
                {
                    'name': str(self.film_service.delta)
                }
            ]
        },

    ]

    def run(self):
        while self.active:
            route = self._choisir_route()
            if route['route'] == "film":
                nb_films = self._choisir_nb_films()
                self._launch_async_process(self.film_service.run_fetching(int(nb_films)))
            elif route['route'] == "serie":
                pass
            self.finish_session()

    def finish_session(self):
        answer = prompt(self.questions[1], style=self.style)
        if answer["again"] == "oui":
            self.active = True
        else:
            self.active = False

    def _choisir_route(self):
        answers = prompt(self.questions[0], style=self.style)
        return answers

    def _choisir_nb_films(self):
        answer = prompt(self.questions[2], style=self.style)
        return int(answer.get('nb_films'))

    def _launch_async_process(self, fn):
        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(fn)
        loop.run_until_complete(future)



class Scripted:
    pass


if __name__ == '__main__':
    BaseORM.metadata.create_all(engine)
    session = Session()
    sys.argv.append("console")
    if sys.argv[1] == "console":
        console = Console(session)
        console.run()
    elif sys.argv[1] == "scripted":
        scripted = Scripted()
        print("scripted")

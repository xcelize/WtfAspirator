import sys
from sqlalchemy.orm import Session
from WtfAspirator.src.Controllers.FilmController import FilmController
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
    questions = [
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

    ]

    def __init__(self, p_session: Session):
        self.film_controller = FilmController(p_session)
        self.active = True

    def run(self):
        while self.active:
            route = self._choisir_route()
            if route['route'] == "film":
                self.film_controller.post()
            elif route['route'] == "serie":
                pass
            self.finish_session()

    def finish_session(self):
        answer = prompt(self.questions[1], style=self.style)
        if answer["again"] == "oui":
            self.active = True
        self.active = False

    def _choisir_route(self):
        answers = prompt(self.questions[0], style=self.style)
        return answers


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

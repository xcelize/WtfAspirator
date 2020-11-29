from abc import ABCMeta, abstractmethod

from sqlalchemy.orm import Session


class AbstractContoller(metaclass=ABCMeta):

    model = NotImplementedError

    def __init__(self, session, *args, **kwargs):
        self.session = session

    @abstractmethod
    def post(self, *args, **kwargs):
        pass

    @abstractmethod
    def get_queryset(self):
        pass


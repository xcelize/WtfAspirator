import requests


class ServiceTMDB:

    def __init__(self):
        self.base_url: str = "https://api.themoviedb.org/3/"
        self.client: requests = requests
        self.api_key: str = "6a3276ee2f7c509f53b55cd3d576030c"
        self.language: str = "FR"
        self.model: object = None

    def get(self, urls):
        pass

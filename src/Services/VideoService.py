from requests.models import Response
from WtfAspirator.src.Services.Service import ServiceTMDB
from ..Objects.Film import Film


class FilmService(ServiceTMDB):

    def __init__(self):
        super().__init__()

    def get_by_id(self, p_id: int):
        response: Response = self.client.get(self.base_url + "movie/" + str(p_id) + "?api_key=" + self.api_key + "&language=" + self.language + "&append_to_response=casts")
        if response.status_code == 200:
            video = Film(response.json())
            return video
        else:
            raise Exception("Impossible de trouver un film avec cet ID")

    def get_last_inserted(self):
        response: Response = self.client.get(self.base_url + "movie/latest?api_key=" + self.api_key + "&language=" + self.language)
        if response.status_code == 200:
            video = Film(response.json())
            return video

    def _get_personne_by_serie(self, p_id_film):
        pass


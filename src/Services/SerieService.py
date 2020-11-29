from requests.models import Response
from .Service import ServiceTMDB
from ..Objects.Serie import Serie


class SerieService(ServiceTMDB):

    def __init__(self):
        super().__init__()

    def get_by_id(self, p_id: int):
        response: Response = self.client.get(self.base_url + "tv/" + str(p_id) + "?api_key=" + self.api_key + "&language=" + self.language + "&append_to_response=casts")
        if response.status_code == 200:
            serie = Serie(response.json())
            return serie
        else:
            raise Exception("Impossible de trouver une série avec cet ID")

    def _get_personne_by_serie(self, p_id_serie: int):
        response: Response = self.client.get(self.base_url + "/tv/" + str(p_id_serie) + "/credit" + "?api_key=" + self.api_key + "&language" + self.language)
        if response.status_code == 200:
            json_response = response.json()
            if json_response.get('cast'):
                for personne in json_response.get('cast'):
                    print(personne)



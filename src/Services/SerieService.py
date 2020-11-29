from .Service import ServiceTMDB
from requests.models import Response
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


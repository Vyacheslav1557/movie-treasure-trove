from kinopoisk_unofficial.request.films.filters_request import FiltersRequest, FiltersResponse
from api_client.api_client import api_client

filters_response: FiltersResponse | None = None


def init_filters_response_client():
    global filters_response
    if filters_response is None:
        filters_response = api_client.films.send_filters_request(FiltersRequest())


init_filters_response_client()

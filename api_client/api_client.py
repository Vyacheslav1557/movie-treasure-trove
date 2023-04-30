from kinopoisk_unofficial.kinopoisk_api_client import KinopoiskApiClient
from constants import KINOPOISK_API_KEY

api_client: KinopoiskApiClient | None = None


def init_api_client() -> None:
    """
    KinopoiskApiClient initialization.
    :return: None
    """
    global api_client
    if api_client is None:
        api_client = KinopoiskApiClient(KINOPOISK_API_KEY)


init_api_client()

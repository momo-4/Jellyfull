import requests


class NeoDBRetriever:

    def __init__(self):
        self._api = {
            'from_url': r'https://neodb.social/api/catalog/fetch',
            'tv': r'https://neodb.social/api/tv/',
            'movie': r'https://neodb.social/api/movie/'
        }
        self._support_mode = ['movie', 'tv']
        self._headers = {
            'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                           '(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'),
        }

    def retrieve_from_url(self, url: str) -> dict:
        """Retrieve data with URL

        Args:
            url: str, URL of the media

        Returns:
            dict, data of NeoDB's retrieval
        """
        params = {
            'url': url
        }
        data = requests.get(self._api['from_url'], params=params, headers=self._headers)
        if data.ok:
            return data.json()
        else:
            raise ValueError(f"Failed to retrieve data from {url}")

    def retrieve_from_uuid(self, uuid: str, mode: str) -> dict:
        """Retrieve data with NeoDB UUID

        Args:
            uuid: str, NeoDB UUID
            mode: str, 'movie' or 'tv'

        Returns:
            dict, data from NeoDB
        """
        if mode not in self._support_mode:
            raise ValueError(f"Mode {mode} is not supported.")
        url = self._api[mode] + uuid
        data = requests.get(url, headers=self._headers)
        if data.ok:
            return data.json()

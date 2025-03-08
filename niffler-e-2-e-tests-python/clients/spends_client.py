from urllib.parse import urljoin

import requests


class SpendsHttpClient:

    session: requests.Session
    base_url: str

    def __init__(self, base_url: str, token: str):
        self.base_url = base_url
        self.session = requests.session()
        self.session.headers.update({
            'Authorization': f'Bearer {token}'
        })

    def get_categories(self):
        response = self.session.get(urljoin(self.base_url, '/api/categories/all'))
        response.raise_for_status()
        return response.json()

    def add_category(self, name: str):
        response = self.session.post(urljoin(self.base_url, '/api/categories/add'), json={
            'name': name
        })
        response.raise_for_status()
        return response.json()

    def add_spends(self, body):
        response = self.session.post(urljoin(self.base_url, '/api/spends/add'), json=body)
        response.raise_for_status()
        return response.json()

    def remove_spends(self, ids: list[str]):
        response = self.session.delete(
            urljoin(self.base_url, '/api/spends/remove'), params={'ids': ids}
        )
        response.raise_for_status()

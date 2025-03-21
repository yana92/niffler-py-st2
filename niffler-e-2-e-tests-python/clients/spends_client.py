from urllib.parse import urljoin

import requests

from models.spend import Category, AddSpend, SpendResponse


class SpendsHttpClient:

    session: requests.Session
    base_url: str

    def __init__(self, base_url: str, token: str):
        self.base_url = base_url
        self.session = requests.session()
        self.session.headers.update({
            'Authorization': f'Bearer {token}'
        })

    def get_categories(self) -> list[Category]:
        response = self.session.get(urljoin(self.base_url, '/api/categories/all'))
        response.raise_for_status()
        return [Category.model_validate(item) for item in response.json()]

    def add_category(self, name: str) -> Category:
        response = self.session.post(urljoin(self.base_url, '/api/categories/add'), json={
            'name': name
        })
        response.raise_for_status()
        return Category.model_validate(response.json())

    def add_spends(self, spend: AddSpend) -> SpendResponse:
        response = self.session.post(urljoin(self.base_url, '/api/spends/add'),
                                     json=spend.model_dump())
        response.raise_for_status()
        return SpendResponse.model_validate(response.json())

    def remove_spends(self, ids: list[str]):
        response = self.session.delete(
            urljoin(self.base_url, '/api/spends/remove'), params={'ids': ids}
        )
        response.raise_for_status()

    def all_spends(self, filter_params=None) -> list[SpendResponse]:
        response = self.session.get(
            urljoin(self.base_url, '/api/v2/spends/all'),
            params=filter_params
        )
        response.raise_for_status()
        return [SpendResponse.model_validate(item) for item in response.json()['content']]

    def total_spends(self, filter_params=None):

        response = self.session.get(
            urljoin(self.base_url, '/api/v2/stat/total'),
            params=filter_params
        )
        response.raise_for_status()
        return response.json()

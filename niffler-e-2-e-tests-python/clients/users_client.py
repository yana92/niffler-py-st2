from urllib.parse import urljoin

import requests


class UsersHttpClient:

    session: requests.Session
    base_url: str

    def __init__(self, base_url: str, token: str):
        self.base_url = base_url
        self.session = requests.session()
        self.session.headers.update({
            'Authorization': f'Bearer {token}'
        })

    def logout(self):
        response = self.session.get(urljoin(self.base_url, '/logout'))
        response.raise_for_status()


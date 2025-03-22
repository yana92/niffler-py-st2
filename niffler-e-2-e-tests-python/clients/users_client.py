
import requests


class UsersHttpClient:

    session: requests.Session
    base_url: str

    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.session()
        # self.session.headers.update({
        #     'Authorization': f'Bearer {token}'
        # })

    # def logout(self):
    #     response = self.session.get(urljoin(self.base_url, '/logout'))
    #     response.raise_for_status()

    # def register(self, username: str, password: str):
    #     user = User(username=username, password=password)
    #     body = {
    #         # '_csrf': '10d31c8a-bf7d-48b1-8c6c-5870239c15b2',
    #         'username': user.username,
    #         'password': user.password,
    #         'passwordSubmit': user.password
    #     }
    #     response = self.session.post(urljoin(self.base_url, '/register'),
    #                                  json=body)
    #     response.raise_for_status()
    #     return user

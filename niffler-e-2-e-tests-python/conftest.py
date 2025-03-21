import os
from urllib.parse import urljoin

import pytest
from dotenv import load_dotenv
from selene import browser, have
from clients.spends_client import SpendsHttpClient


pytest_plugins = [
    'fixtures.fixtures_spending',
]


@pytest.fixture(scope="session")
def envs():
    load_dotenv()


@pytest.fixture(scope="session")
def frontend_url(envs) -> str:
    return os.getenv("FRONTEND_URL")


@pytest.fixture(scope="session")
def gateway_url(envs) -> str:
    return os.getenv("GATEWAY_URL")


@pytest.fixture(scope="session")
def auth_url(envs) -> str:
    return os.getenv("AUTH_URL")


@pytest.fixture(scope="session")
def app_user(envs):
    return os.getenv("TEST_USERNAME"), os.getenv("TEST_PASSWORD")


@pytest.fixture(scope="module")
def auth(frontend_url, app_user) -> str:
    username, password = app_user
    browser.open(frontend_url)
    if browser.driver.execute_script('return window.localStorage.getItem("id_token")') is None:
        browser.element('input[name=username]').set_value(username)
        browser.element('input[name=password]').set_value(password)
        browser.element('button[type=submit]').click()
    return browser.driver.execute_script('return window.localStorage.getItem("id_token")')


@pytest.fixture(scope="module")
def spends_client(gateway_url, auth) -> SpendsHttpClient:
    return SpendsHttpClient(gateway_url, auth)


@pytest.fixture()
def main_page(auth, frontend_url):
    browser.open(frontend_url)


@pytest.fixture()
def login_page(auth_url):
    browser.open(urljoin(auth_url, '/login'))


@pytest.fixture()
def register_page(auth_url):
    browser.open(urljoin(auth_url, '/register'))


@pytest.fixture()
def logout(main_page, auth_url):
# =======
# from pytest import fixture
# from selene import browser, have
#
# from utils import random_string
#

# @fixture(scope="session")
# def user():
#     username = random_string()
#     password = random_string(7)
#     browser.open('http://auth.niffler.dc:9000/register')
#     browser.element('#username').set_value(username)
#     browser.element('#password').set_value(password)
#     browser.element('#passwordSubmit').set_value(password)
#     browser.element('button[type="submit"]').click()
#     return {
#         'username': username,
#         'password': password
#     }


# @fixture(scope='module')
# def login(user):
#     browser.open('http://frontend.niffler.dc')
#     token = browser.driver.execute_script(
#             'return window.localStorage.getItem("id_token")'
#     )
#     if token is None:
#         browser.open('http://frontend.niffler.dc')
#         browser.element('input[name=username]').set_value(user['username'])
#         browser.element('input[name=password]').set_value(user['password'])
#         browser.element('button[type=submit]').click()
#     token = browser.driver.execute_script('return window.localStorage.getItem("id_token")')
#     return token


# @fixture()
# def logout():
    browser.open('http://frontend.niffler.dc')
    if browser.driver.execute_script(
            'return window.localStorage.getItem("id_token")'
    ) is not None:
        browser.element('button[aria-label="Menu"]').click()
        browser.element('//*[@id="account-menu"]/div[3]/ul/li[4]').click()
        # browser.element('/html/body/div[2]/div[3]/div/div[2]/button[2]').click()
        browser.element('div[role="presentation"]').should(have.text('Log out')).click()

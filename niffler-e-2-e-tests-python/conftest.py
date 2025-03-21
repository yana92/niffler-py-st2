import os
from urllib.parse import urljoin

import pytest
from dotenv import load_dotenv
from selene import browser, have
from clients.spends_client import SpendsHttpClient
from databases.spend_db import SpendDb
from models.config import Envs

pytest_plugins = [
    'fixtures.fixtures_spending',
]


@pytest.fixture(scope="session")
def envs() -> Envs:
    load_dotenv()
    return Envs(
        frontend_url=os.getenv('FRONTEND_URL'),
        gateway_url=os.getenv('GATEWAY_URL'),
        auth_url=os.getenv('AUTH_URL'),
        spend_db_url=os.getenv('SPEND_DB_URL'),
        test_username=os.getenv('TEST_USERNAME'),
        test_password=os.getenv('TEST_PASSWORD')
    )


@pytest.fixture(scope="session")
def spend_db(envs) -> SpendDb:
    return SpendDb(envs.spend_db_url)


@pytest.fixture(scope="module")
def auth(envs) -> str:
    browser.open(envs.frontend_url)
    if browser.driver.execute_script('return window.localStorage.getItem("id_token")') is None:
        browser.element('input[name=username]').set_value(envs.test_username)
        browser.element('input[name=password]').set_value(envs.test_password)
        browser.element('button[type=submit]').click()
        browser.driver.refresh()

    return browser.driver.execute_script('return window.localStorage.getItem("id_token")')


@pytest.fixture(scope="module")
def spends_client(envs, auth) -> SpendsHttpClient:
    return SpendsHttpClient(envs.gateway_url, auth)


@pytest.fixture()
def main_page(auth, envs):
    browser.open(envs.frontend_url)


@pytest.fixture()
def login_page(logout, envs):
    browser.open(urljoin(envs.auth_url, '/login'))


@pytest.fixture()
def register_page(logout, envs):
    browser.open(urljoin(envs.auth_url, '/register'))


@pytest.fixture()
def profile_page(auth, envs):
    browser.open(urljoin(envs.frontend_url, '/profile'))


@pytest.fixture()
def friends_page(auth, envs):
    browser.open(urljoin(envs.frontend_url, '/people/friends'))


@pytest.fixture()
def logout(envs):
    browser.open(envs.frontend_url)
    if browser.driver.execute_script(
            'return window.localStorage.getItem("id_token")'
    ) is not None:
        browser.element('button[aria-label="Menu"]').click()
        browser.element('//*[@id="account-menu"]/div[3]/ul/li[4]').click()
        # browser.element('/html/body/div[2]/div[3]/div/div[2]/button[2]').click()
        browser.element('div[role="presentation"]').should(have.text('Log out')).click()

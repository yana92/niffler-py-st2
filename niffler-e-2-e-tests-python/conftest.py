import os
import pytest
from dotenv import load_dotenv
from selene import browser
from clients.spends_client import SpendsHttpClient


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
def app_user(envs):
    return os.getenv("TEST_USERNAME"), os.getenv("TEST_PASSWORD")


@pytest.fixture(scope="session")
def auth(frontend_url, app_user) -> str:
    username, password = app_user
    browser.open(frontend_url)
    browser.element('input[name=username]').set_value(username)
    browser.element('input[name=password]').set_value(password)
    browser.element('button[type=submit]').click()
    return browser.driver.execute_script('return window.localStorage.getItem("id_token")')


@pytest.fixture(scope="session")
def spends_client(gateway_url, auth) -> SpendsHttpClient:
    return SpendsHttpClient(gateway_url, auth)


@pytest.fixture(scope="function", params=[])
def category(request, spends_client) -> str:
    category_name = request.param
    current_catigories = spends_client.get_categories()
    category_names = [category['name'] for category in current_catigories]
    if category_name not in category_names:
        spends_client.add_category(category_name)

    return category_name


@pytest.fixture(params=[])
def spends(request, spends_client):
    spend = spends_client.add_spends(request.param)
    yield spend
    try:
        # TODO проверить наличие траты перед удалением
        spends_client.remove_spends(ids=[spend['id']])
    except Exception:
        pass


@pytest.fixture()
def main_page(auth, frontend_url):
    browser.open(frontend_url)

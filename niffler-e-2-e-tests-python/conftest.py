from pytest import fixture
from selene import browser, have

from utils import random_string


@fixture(scope="session")
def user():
    username = random_string()
    password = random_string(7)
    browser.open('http://auth.niffler.dc:9000/register')
    browser.element('#username').set_value(username)
    browser.element('#password').set_value(password)
    browser.element('#passwordSubmit').set_value(password)
    browser.element('button[type="submit"]').click()
    return {
        'username': username,
        'password': password
    }


@fixture(scope='module')
def login(user):
    browser.open('http://frontend.niffler.dc')
    token = browser.driver.execute_script(
            'return window.localStorage.getItem("id_token")'
    )
    if token is None:
        browser.open('http://frontend.niffler.dc')
        browser.element('input[name=username]').set_value(user['username'])
        browser.element('input[name=password]').set_value(user['password'])
        browser.element('button[type=submit]').click()
    token = browser.driver.execute_script('return window.localStorage.getItem("id_token")')
    return token


@fixture()
def logout():
    browser.open('http://frontend.niffler.dc')
    if browser.driver.execute_script(
            'return window.localStorage.getItem("id_token")'
    ) is not None:
        browser.element('button[aria-label="Menu"]').click()
        browser.element('//*[@id="account-menu"]/div[3]/ul/li[4]').click()
        browser.element('div[role="presentation"]').should(have.text('Log out')).click()


from urllib.parse import urljoin

from pytest import mark
from selene import browser, have
from marks import Pages
from utils import random_string


@Pages.login_page
def test_redirect_to_register_page(auth_url: str):
    browser.element('.form__register').click()
    assert browser.driver.current_url == f'{auth_url}/register'
    browser.element('#register-form').should(have.text('Sign up'))


@Pages.register_page
def test_sign_up():
    password = f'pass_{random_string()}'
    browser.element('#username').set_value(f'username_{random_string()}')
    browser.element('#password').set_value(password)
    browser.element('#passwordSubmit').set_value(password)
    browser.element('button[type="submit"]').click()
    browser.element('.form p').should(have.text("Congratulations! You've registered!"))
    browser.element('.form_sign-in').should(have.text("Sign in"))


@Pages.register_page
@mark.parametrize('length', [2, 14])
def test_sign_up_invalid_password(length: int):
    password = random_string(length)
    browser.element('#username').set_value(f'username_{random_string()}')
    browser.element('#password').set_value(password)
    browser.element('#passwordSubmit').set_value(password)
    browser.element('button[type="submit"]').click()
    browser.all('#register-form span').should(have.size(2))
    browser.all('#register-form span')[0].should(
        have.text('Allowed password length should be from 3 to 12 characters')
    )
    browser.all('#register-form span')[1].should(
        have.text('Allowed password length should be from 3 to 12 characters')
    )


@Pages.main_page
def test_logout(auth_url: str):
    browser.element('button[aria-label="Menu"]').click()
    browser.all('ul[role="menu"] li[role="menuitem"]').should(have.size(4))
    browser.element('//*[@id="account-menu"]/div[3]/ul/li[4]').click()
    browser.element('/html/body/div[2]/div[3]/div/div[2]/button[2]').click()
    assert browser.driver.current_url == urljoin(auth_url, '/login')
    assert browser.element('form[action="/login"]')
    assert browser.driver.execute_script(
        'return window.localStorage.getItem("id_token")'
    ) == None, 'Не пустой токен пользователя в localStorage'


@mark.usefixtures('logout')
@Pages.login_page
def test_login(app_user, frontend_url: str):
    username, password = app_user
    browser.element('input[name="username"]').set_value(username)
    browser.element('input[name=password]').set_value(password)
    browser.element('button[type=submit]').click()
    browser.driver.current_url == urljoin(frontend_url, '/main')


@Pages.login_page
def test_auth_invalid_password(app_user):
    username, password = app_user
    browser.element('input[name=username]').set_value(username)
    browser.element('input[name=password]').set_value(f"{password}_")
    browser.element('button[type=submit]').click()
    browser.element('form[action="/login"]').should(have.text('Неверные учетные данные пользователя'))


@Pages.login_page
def test_auth_invalid_username(app_user):
    username, password = app_user
    browser.element('input[name=username]').set_value(f"{username}1")
    browser.element('input[name=password]').set_value(password)
    browser.element('button[type=submit]').click()
    browser.element('form[action="/login"]').should(have.text('Неверные учетные данные пользователя'))


@mark.usefixtures('logout')
@Pages.register_page
def test_redirect_to_login_from_register():
    browser.element('.form__link').should(have.text('Log in!')).click()
    browser.driver.current_url == 'http://auth.niffler.dc:9000/login'

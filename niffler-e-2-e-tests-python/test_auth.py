from pytest import mark
from selene import browser, have


@mark.usefixtures('logout')
def test_auth_invalid_password():
    browser.open('http://frontend.niffler.dc')
    browser.element('input[name=username]').set_value("stas")
    browser.element('input[name=password]').set_value("11111")
    browser.element('button[type=submit]').click()
    browser.element('form[action="/login"]').should(have.text('Неверные учетные данные пользователя'))


@mark.usefixtures('logout')
def test_auth_invalid_username():
    browser.open('http://frontend.niffler.dc')
    browser.element('input[name=username]').set_value("stass")
    browser.element('input[name=password]').set_value("12345")
    browser.element('button[type=submit]').click()
    browser.element('form[action="/login"]').should(have.text('Неверные учетные данные пользователя'))


@mark.usefixtures('logout')
def test_redirect_to_login_from_register():
    browser.open('http://auth.niffler.dc:9000/register')
    browser.element('.form__link').should(have.text('Log in!')).click()
    browser.driver.current_url == 'http://auth.niffler.dc:9000/login'

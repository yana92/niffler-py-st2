from pytest import mark
from selene import browser, have


@mark.usefixtures('login')
class TestRedirect:
    def test_redirect_to_friends_from_menu(self):
        # Шаги
        browser.open('http://frontend.niffler.dc/main')
        browser.element('button[aria-label="Menu"]').click()
        browser.all('ul[role="menu"] li[role="menuitem"]').should(have.size(4))
        browser.element('//*[@id="account-menu"]/div[3]/ul/li[2]').click()
        # Ожидаемый результат
        assert browser.driver.current_url == 'http://frontend.niffler.dc/people/friends'

    def test_redirect_to_all_from_friends(self):
        # Предусловия (переход на /friends)
        browser.open('http://frontend.niffler.dc/people/friends')
        # Шаги
        browser.element('a[href="/people/all"]').click()
        # Ожидаемый результат
        assert browser.driver.current_url == 'http://frontend.niffler.dc/people/all'

    def test_redirect_to_all_from_menu(self):
        # Шаги
        browser.element('button[aria-label="Menu"]').click()
        browser.all('ul[role="menu"] li[role="menuitem"]').should(have.size(4))
        browser.element('//*[@id="account-menu"]/div[3]/ul/li[3]').click()
        # Ожидаемый результат
        assert browser.driver.current_url == 'http://frontend.niffler.dc/people/all'

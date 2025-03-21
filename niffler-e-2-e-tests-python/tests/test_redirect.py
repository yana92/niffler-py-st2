from pytest import mark
from selene import browser, have

from marks import Pages


@mark.usefixtures('auth')
class TestRedirect:
    @Pages.main_page
    def test_redirect_to_friends_from_menu(self):
        browser.element('button[aria-label="Menu"]').click()
        browser.all('ul[role="menu"] li[role="menuitem"]').should(have.size(4))
        browser.element('//*[@id="account-menu"]/div[3]/ul/li[2]').click()
        # Ожидаемый результат
        assert browser.driver.current_url == 'http://frontend.niffler.dc/people/friends'

    @Pages.friends_page
    def test_redirect_to_all_from_friends(self):
        browser.element('a[href="/people/all"]').click()
        assert browser.driver.current_url == 'http://frontend.niffler.dc/people/all'

    def test_redirect_to_all_from_menu(self):
        browser.element('button[aria-label="Menu"]').click()
        browser.all('ul[role="menu"] li[role="menuitem"]').should(have.size(4))
        browser.element('//*[@id="account-menu"]/div[3]/ul/li[3]').click()
        assert browser.driver.current_url == 'http://frontend.niffler.dc/people/all'

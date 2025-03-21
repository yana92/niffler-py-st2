from pytest import mark
from selene import browser, have

from marks import Pages


@mark.usefixtures('auth')
class TestProfile:
    @Pages.profile_page
    def test_edit_name_by_button(self):
        name = 'Стас by button'

        browser.element('#name')
        browser.element('#name').set_value(name)
        browser.element('button[type="submit"]').should(have.text('Save changes')).click()
        browser.element('div[role="alert"]').should(have.text('Profile successfully updated'))
        browser.driver.refresh()
        browser.element('#name').should(have.value(name))

    @Pages.profile_page
    def test_edit_name_by_press_enter(self):
        name = 'Стас by enter'

        browser.element('#name')
        browser.element('#name').set_value(name).press_enter()
        browser.element('div[role="alert"]').should(have.text('Profile successfully updated'))
        browser.driver.refresh()
        browser.element('#name').should(have.value(name))

from urllib.parse import urljoin

from pytest import mark

from marks import Pages, TestData
from selene import browser, have, by

from models.spend import Spend, AddSpend, AddCategory, Category
from utils import random_string

TEST_CATEGORY = 'school'
TEST_CATEGORY_MODEL = AddCategory(name=TEST_CATEGORY)
TEST_SPENDINGS = [
    AddSpend(
        amount=97.5,
        description=f"Test description {random_string()}",
        currency="RUB",
        spendDate="2025-03-05T20:32:27.999Z",
        category=TEST_CATEGORY_MODEL
    ),
    AddSpend(
        amount=197.5,
        description=f"Test description {random_string()}",
        currency="RUB",
        spendDate="2025-03-05T20:32:27.999Z",
        category=TEST_CATEGORY_MODEL
    )
]


@Pages.main_page
def test_spending_title_exists():
    assert browser.element('#spendings').should(have.text('History of Spendings')), \
        'На странице нет ожидаемого title с текстом History of Spendings'


@Pages.main_page
@Pages.profile_page
def test_add_category(spends_client, spend_db):
    browser.open('http://frontend.niffler.dc/profile')
    category_name = 'Test added category'
    browser.element('main h2').should(have.text('Profile'))
    browser.element('#category').set_value(category_name).press_enter()
    browser.element('div[role="alert"]').should(have.text(f"You've added new category: {category_name}"))
    browser.element('//*[@id="root"]/main/div/div').should(have.text(category_name))
    categories = spends_client.get_categories()
    category_id = (category.id for category in categories if category.name == category_name)
    spend_db.delete_category(category_id)


@Pages.main_page
@TestData.category('category for archive')
def test_archived_category(category):
    browser.open('http://frontend.niffler.dc/profile')
    browser.element(
        'div[class="MuiGrid-root MuiGrid-container MuiGrid-spacing-xs-2 css-3w20vr"]'
    ).should(have.text(category.name)).element('button[aria-label="Archive category"]').click()
    browser.element('/html/body/div[2]/div[3]/div/div[2]/button[2]').click()
    browser.element('div[role="alert"]').should(have.text(f"Category {category.name} is archived"))


@mark.usefixtures('auth')
@TestData.category('category for archive 3')
def test_show_archive_category(category_archived):
    browser.open('http://frontend.niffler.dc/profile')
    browser.element('input[type="checkbox"]').click()
    browser.element('//*[@id="root"]/main/div/div').should(have.text(category_archived.name))


@Pages.main_page
@TestData.category(TEST_CATEGORY)
@TestData.spends(TEST_SPENDINGS[0])
def test_delete_one_spending(
        category: Category, spends: Spend
):
    browser.element('#spendings').should(have.text(spends.description))
    browser.element('#spendings tbody input[type=checkbox]').click()
    browser.element('#spendings button[id=delete]').click()
    browser.element('div[role="presentation"]>div[tabindex="0"]')
    browser.element('/html/body/div[2]/div[3]/div/div[2]/button[2]').click()
    assert browser.element('div[role="presentation"]>div[tabindex="-1"]'), \
        'Не удалось удалить трату, диалоговое окно не закрылось'
    browser.all('#spendings tbody tr').should(have.size(0))
    assert browser.element('#spendings').should(have.text('There are no spendings')), \
        'На странице в разделе с тратами отсутсвует текст There are no spendings'


@TestData.category(TEST_CATEGORY)
@Pages.main_page
def test_add_spending(category: Category, envs):
    description = f'Test description {random_string()}'
    browser.element('//*[@id="root"]/header/div/div[2]/a').click()
    browser.element('input[name="amount"]').set_value(15000)
    browser.element(f'input[name="category"]').set_value(category.name)
    browser.element('input[name="description"]').set_value(description)
    browser.element('button[type="submit"]').click()
    assert browser.element(by.text(description)), \
        'На странице отсутсвует добавленная трата'


@Pages.main_page
@TestData.category(TEST_CATEGORY)
@mark.parametrize('multiple_spendings', [TEST_SPENDINGS], indirect=True)
def test_delete_all_spendings(multiple_spendings: list[dict], category: Category):
    browser.element('#spendings input[type=checkbox]').click()
    browser.element('#spendings button[id=delete]').click()
    browser.element('div[role="presentation"]>div[tabindex="0"]')
    browser.all('div[role=dialog] button[type=button]')[-1].should(have.text('Delete')).click()
    assert browser.element('div[role="presentation"]>div[tabindex="-1"]'), \
        'Не удалось удалить трату, диалоговое окно не закрылось'
    browser.all('#spendings tbody tr').should(have.size(0))
    assert browser.element('#spendings').should(have.text('There are no spendings')), \
        'На странице в разделе с тратами отсутсвует текст There are no spendings'


@Pages.main_page
@TestData.category(TEST_CATEGORY)
@mark.parametrize('multiple_spendings', [TEST_SPENDINGS], indirect=True)
def test_spendings_total_amount_one_category(
        category: Category, multiple_spendings: list[dict], total_spendings: dict
):
    total = total_spendings["total"]
    if total % 1 == 0:
        total = int(total)
    browser.driver.refresh()
    assert browser.element('#legend-container li').should(have.text(
        f'{category.name} {total} ₽'
    )), 'Отображется некорректное значение total и категория'


@Pages.main_page
def test_redirect_to_spending_page(envs):
    browser.element('//*[@id="root"]/header/div/div[2]/a').click()
    assert browser.driver.current_url == urljoin(envs.frontend_url, '/spending'), \
        'Текущий url не соответствует ожидаемому'

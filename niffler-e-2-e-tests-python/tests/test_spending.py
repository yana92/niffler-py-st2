from urllib.parse import urljoin

from pytest import mark

from marks import Pages, TestData
from selene import browser, have, by

from utils import random_string

TEST_CATEGORY = 'school'


@Pages.main_page
def test_spending_title_exists():
    browser.element('#spendings').should(have.text('History of Spendings'))


@Pages.main_page
@TestData.category(TEST_CATEGORY)
@TestData.spends({
        "amount": "97",
        "description": f"Test description {random_string()}",
        "currency": "RUB",
        "spendDate": "2025-03-05T20:32:27.999Z",
        "category": {
            "name": TEST_CATEGORY
        }
    })
def test_delete_one_spending(
        frontend_url: str, category: str, spends: dict, spends_client
):
    browser.element('#spendings').should(have.text(spends['description']))
    browser.element('#spendings tbody input[type=checkbox]').click()
    browser.element('#spendings button[id=delete]').click()
    browser.element('div[role="presentation"]>div[tabindex="0"]')
    browser.element('/html/body/div[2]/div[3]/div/div[2]/button[2]').click()
    browser.all('#spendings tbody tr').should(have.size(0))
    browser.element('#spendings').should(have.text('There are no spendings'))


@TestData.category(TEST_CATEGORY)
@Pages.main_page
def test_add_spending(category: str, frontend_url: str, spends_client):
    description = f'Test description {random_string()}'
    browser.element('//*[@id="root"]/header/div/div[2]/a').click()
    browser.element('input[name="amount"]').set_value(15000)
    browser.element(f'input[name="category"]').set_value(category)
    browser.element('input[name="description"]').set_value(description)
    browser.element('button[type="submit"]').click()
    assert browser.driver.current_url == urljoin(frontend_url, '/main')
    browser.element(by.text(description))


@Pages.main_page
@TestData.category(TEST_CATEGORY)
@mark.parametrize('multiple_spendings', [[
    {
        "amount": "25000",
        "description": f"QA.GURU Python Advanced 2",
        "currency": "RUB",
        "spendDate": "2025-03-05T20:32:27.999Z",
        "category": {
            "name": TEST_CATEGORY
        }
    },
    {
        "amount": "20000",
        "description": f"QA.GURU Python Advanced 2",
        "currency": "RUB",
        "spendDate": "2025-03-05T20:32:27.999Z",
        "category": {
            "name": TEST_CATEGORY
        }
    }
]], indirect=True)
def test_delete_all_spendings(multiple_spendings: list[dict], category: str):
    browser.element('#spendings input[type=checkbox]').click()
    browser.element('#spendings button[id=delete]').click()
    browser.element('div[role="presentation"]>div[tabindex="0"]')
    browser.all('div[role=dialog] button[type=button]')[-1].should(have.text('Delete')).click()
    browser.all('#spendings tbody tr').should(have.size(0))
    browser.element('#spendings').should(have.text('There are no spendings'))


@Pages.main_page
@TestData.category(TEST_CATEGORY)
@mark.parametrize('multiple_spendings', [[
    {
        "amount": "25000",
        "description": f"QA.GURU Python Advanced 2",
        "currency": "RUB",
        "spendDate": "2025-03-05T20:32:27.999Z",
        "category": {
            "name": TEST_CATEGORY
        }
    },
    {
        "amount": "20000",
        "description": f"QA.GURU Python Advanced 2",
        "currency": "RUB",
        "spendDate": "2025-03-05T20:32:27.999Z",
        "category": {
            "name": TEST_CATEGORY
        }
    }
]], indirect=True)
def test_spendings_total_amount_one_category(
        category: str, multiple_spendings: list[dict], total_spendings: dict
):
    browser.element('#legend-container li').should(have.text(
        f'{category} {int(total_spendings["total"])} ₽'
    ))


@Pages.main_page
def test_redirect_to_spending_page(frontend_url: str):
    browser.element('//*[@id="root"]/header/div/div[2]/a').click()
    assert browser.driver.current_url == urljoin(frontend_url, '/spending')


@TestData.category(TEST_CATEGORY)
@Pages.main_page
def test_add_spending(category: str, frontend_url: str, spends_client):
    description = f'Test description {random_string()}'
    browser.element('//*[@id="root"]/header/div/div[2]/a').click()
    browser.element('input[name="amount"]').set_value(15000)
    browser.element(f'input[name="category"]').set_value(category)
    browser.element('input[name="description"]').set_value(description)
    browser.element('button[type="submit"]').click()
    assert browser.driver.current_url == urljoin(frontend_url, '/main')
    browser.element(by.text(description))

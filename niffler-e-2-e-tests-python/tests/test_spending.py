from marks import Pages, TestData
from selene import browser, have

TEST_CATEGORY = 'school'


@Pages.main_page
def test_spending_title_exists():
    browser.element('#spendings').should(have.text('History of Spendings'))


@Pages.main_page
@TestData.category(TEST_CATEGORY)
@TestData.spends({
        "amount": "97",
        "description": f"QA.GURU Python Advanced 2",
        "currency": "RUB",
        "spendDate": "2025-03-05T20:32:27.999Z",
        "category": {
            "name": TEST_CATEGORY
        }
    })
def test_spending_should_be_deleted_after_table_action(frontend_url, category, spends):

    browser.open(frontend_url)
    browser.element('#spendings').should(have.text('QA.GURU Python Advanced 2'))
    browser.element('#spendings tbody input[type=checkbox]').click()
    browser.element('#spendings button[id=delete]').click()
    browser.all('div[role=dialog] button[type=button]')[-1].should(have.text('Delete')).click()
    browser.all('#spendings tbody tr').should(have.size(0))
    browser.element('#spendings').should(have.text('There are no spendings'))

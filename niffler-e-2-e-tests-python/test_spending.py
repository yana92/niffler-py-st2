import requests
from selene import browser, have


def test_spending_title_exists():
    browser.open('http://frontend.niffler.dc')
    browser.element('input[name=username]').set_value("stas")
    browser.element('input[name=password]').set_value("12345")
    browser.element('button[type=submit]').click()
    browser.element('#spendings').should(have.text('History of Spendings'))


def test_spending_should_be_deleted_after_table_action():
    url = 'http://gateway.niffler.dc:8090/api/spends/add'
    headers = {
        'Authorization': 'Bearer eyJraWQiOiIwNjFmNmIwMS1mNjc5LTQ4MmYtYjEzMy1hNjE2NGFiZmI3OGMiLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJzdGFzIiwiYXVkIjoiY2xpZW50IiwiYXpwIjoiY2xpZW50IiwiYXV0aF90aW1lIjoxNzQxMjA2NzQ3LCJpc3MiOiJodHRwOi8vYXV0aC5uaWZmbGVyLmRjOjkwMDAiLCJleHAiOjE3NDEyMDg1NDgsImlhdCI6MTc0MTIwNjc0OCwianRpIjoiNjRhMWNlZDUtYmU3NC00MjFhLThkZjctMDA1YTMwOTk2NjM3Iiwic2lkIjoidTlaZnJJaGF4NEJwWnlwVFB0ZlNDQVFrWjdqSUhJS0NmcUl3WVVyS1o1WSJ9.S8rleLnDGZ1cJ4slKUimtJIYwJDtovINjMF4o_e_fGAD_0tt_yuRM1-SDvYBN-gxL4ytTzGZ1yVDVrqipN3Q9frAOVHutXSSyLOVErvX1CKWXXdhwYomyPhsa9dQwTjtTyHeWInR8-A8trbUMlh3g9UtxMpm9-3jLhJA7iXfK96iB6eBut0lsWlA6GjVTtQk9zi_GyE4oBNdwasPeoQAGybMNgU8lYD6CxrwlORGRyFlvsDO4i42y5Js01ze6PCAMko9STAv1yS8TTNn5UXsRmRr_knmrCid47vqYzLd0qjLJAjZEri6glg06wVJ5wjJZV0cYEY6c_7VvRYnVEt4AA',
        # 'Content-Type': 'application/json'
    }
    data = {
        "amount": "97",
        "description": "",
        "currency": "RUB",
        "spendDate": "2025-03-05T20:32:27.999Z",
        "category": {
            "name": "QA.GURU Python Advanced 2"
        }
    }

    # Отправка POST-запроса
    response = requests.post(url, headers=headers, json=data)

    print(response.json())

    browser.open('http://frontend.niffler.dc')
    browser.element('input[name=username]').set_value("stas")
    browser.element('input[name=password]').set_value("12345")
    browser.element('button[type=submit]').click()
    browser.element('#spendings').should(have.text('QA.GURU Python Advanced 2'))
    browser.element('#spendings tbody input[type=checkbox]').click()
    browser.element('#spendings button[id=delete]').click()
    browser.all('div[role=dialog] button[type=button]')[-1].should(have.text('Delete')).click()
    browser.all('#spendings tbody tr').should(have.size(0))
    browser.element('#spendings').should(have.text('There are no spendings'))

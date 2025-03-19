import requests
from pytest import mark
from selene import browser, have


@mark.usefixtures('login')
def test_spending_title_exists():
    browser.element('#spendings').should(have.text('History of Spendings'))


def test_spending_should_be_deleted_after_table_action(login):
    token = login
    # Предусловие (создание категории)
    category = 'school'
    url = 'http://gateway.niffler.dc:8090/api/categories/add'
    headers = {
        'Authorization': f'Bearer {token}',
    }
    data = {
        'name': category,
    }
    requests.post(url, headers=headers, json=data)

    # Предусловие (создание траты)
    token = login
    url = 'http://gateway.niffler.dc:8090/api/spends/add'
    headers = {
        'Authorization': f'Bearer {token}',
    }
    data = {
        "amount": "97",
        "description": "QA.GURU Python Advanced 2",
        "currency": "RUB",
        "spendDate": "2025-03-05T20:32:27.999Z",
        "category": {
            "name": category
        }
    }

    response = requests.post(url, headers=headers, json=data)

    print(response.json())

    # Шаги
    browser.open('http://frontend.niffler.dc')
    browser.element('#spendings').should(have.text('QA.GURU Python Advanced 2'))
    browser.element('#spendings tbody input[type=checkbox]').click()
    browser.element('#spendings button[id=delete]').click()
    browser.all('div[role=dialog] button[type=button]')[-1].should(have.text('Delete')).click()
    # Ожидаемый результат
    browser.all('#spendings tbody tr').should(have.size(0))
    browser.element('#spendings').should(have.text('There are no spendings'))


@mark.usefixtures('login')
def test_add_category():
    browser.open('http://frontend.niffler.dc/profile')
    # Шаги теста
    category = 'Test added category'
    browser.element('main h2').should(have.text('Profile'))
    browser.element('#category').set_value(category).press_enter()
    # Ожидаемый результат
    browser.element('div[role="alert"]').should(have.text(f"You've added new category: {category}"))
    browser.element('//*[@id="root"]/main/div/div').should(have.text(category))


def test_archived_category(login):
    token = login

    # Предусловие (создание категории)
    category = 'category for archive'
    url = 'http://gateway.niffler.dc:8090/api/categories/add'
    headers = {
        'Authorization': f'Bearer {token}',
    }
    data = {
        'name': category,
    }

    requests.post(url, headers=headers, json=data)
    # Предусловие (переход в профиль)
    browser.open('http://frontend.niffler.dc/profile')
    # Шаги
    browser.element('div[class="MuiGrid-root MuiGrid-container MuiGrid-spacing-xs-2 css-3w20vr"]').should(have.text(category)).element('button[aria-label="Archive category"]').click()
    browser.element('/html/body/div[2]/div[3]/div/div[2]/button[2]').click()
    # Ожидаемый результат
    browser.element('div[role="alert"]').should(have.text(f"Category {category} is archived"))


def test_show_archive_category(login):
    token = login
    # Предусловие (создание категории)
    category = 'category for archive 3'
    url = 'http://gateway.niffler.dc:8090/api/categories/add'
    headers = {
        'Authorization': f'Bearer {token}',
    }
    data = {
        'name': category,
    }

    response = requests.post(url, headers=headers, json=data)
    # Предусловия (архивирование категории)
    url = 'http://gateway.niffler.dc:8090/api/categories/update'
    data = response.json().copy()
    data['archived'] = True
    requests.post(url, headers=headers, json=data)
    # Предусловие (переход в профиль)
    browser.open('http://frontend.niffler.dc/profile')
    # Шаги
    browser.element('input[type="checkbox"]').click()
    # Ожидаемый результат
    browser.element('//*[@id="root"]/main/div/div').should(have.text(category))

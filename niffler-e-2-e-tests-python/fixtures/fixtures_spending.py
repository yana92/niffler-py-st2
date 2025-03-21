import pytest


@pytest.fixture(scope="function", params=[])
def category(request, spends_client) -> str:
    category_name = request.param
    current_catigories = spends_client.get_categories()
    category_names = [category['name'] for category in current_catigories]
    if category_name not in category_names:
        spends_client.add_category(category_name)

    return category_name


@pytest.fixture(params=[])
def category_archived(request, spends_client):
    category_name = request.param
    category = spends_client.add_category(category_name)
    data = category.copy()
    data['archived'] = True
    category_archived = spends_client.archive_category(body=data)
    return category_archived


@pytest.fixture(params=[])
def spends(request, spends_client):
    spend = spends_client.add_spends(request.param)
    yield spend
    try:
        all_spends = spends_client.all_spends()['content']
        spend_ids = [s['id'] for s in all_spends]
        if spend['id'] in spend_ids:
            spends_client.remove_spends(ids=[spend['id']])
    except Exception:
        pass


@pytest.fixture(params=[])
def multiple_spendings(spends_client, request):
    spendings_data = request.param
    spendings = [spends_client.add_spends(spend) for spend in spendings_data]
    yield spendings
    try:
        all_spends = spends_client.all_spends()['content']
        spend_ids = [s['id'] for s in all_spends]
        for spending in spendings:
            if spending['id'] in spend_ids:
                spends_client.remove_spends(ids=[spending['id']])
    except Exception:
        pass


@pytest.fixture(params=[None])
def total_spendings(spends_client, request):
    total_spendings = spends_client.total_spends(request.param or None)
    return total_spendings

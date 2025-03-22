import pytest

from models.spend import Spend, SpendResponse, Category


@pytest.fixture(params=[])
def category(request, spends_client, spend_db) -> Category:
    category_name = request.param
    current_categories = spends_client.get_categories()
    category_added = next((
        category for category in current_categories if category.name == category_name
    ), None)
    if category_added is None:
        category_added = spends_client.add_category(category_name)
    yield category_added
    spendings = spend_db.get_category_spends(category_added.id)
    spendings_ids = [spend.id for spend in spendings]
    if len(spendings_ids) > 0:
        spends_client.remove_spends(spendings_ids)
    spend_db.delete_category(category_added.id)


# @pytest.fixture(params=[])
# <<<<<<< HEAD
# def spends(request, spends_client) -> Spend:
# =======
# def category_archived(request, spends_client):
#     category_name = request.param
#     category: Category = spends_client.add_category(category_name)
#     # data = category.copy()
#     # data['archived'] = True
#     category.archived = True
#     category_archived = spends_client.archive_category(category)
#     return category_archived

@pytest.fixture()
def category_archived(category: Category, spends_client) -> Category:
    # category_name = request.param
    # category: Category = spends_client.add_category(category_name)
    # data = category.copy()
    # data['archived'] = True
    category.archived = True
    category_archived = spends_client.archive_category(category)
    return category_archived


@pytest.fixture(params=[])
# def spends(request, spends_client):
def spends(request, spends_client) -> Spend:
# >>>>>>> 5fa15e2162eb3c35e8d1f4abb180d9e67b760c53
    spend = spends_client.add_spends(request.param)
    yield spend
    all_spends = spends_client.all_spends()
    if spend.id in [spend.id for spend in all_spends]:
        spends_client.remove_spends([spend.id])


@pytest.fixture(params=[])
def multiple_spendings(spends_client, request) -> list[SpendResponse]:
    spendings_data = request.param
    spendings = [spends_client.add_spends(spend) for spend in spendings_data]
    yield spendings
# <<<<<<< HEAD
    all_spends = spends_client.all_spends()
    for test_spend in all_spends:
        if test_spend.id in [spend.id for spend in all_spends]:
            spends_client.remove_spends([test_spend.id])
# =======
#     try:
#         all_spends = spends_client.all_spends()['content']
#         spend_ids = [s['id'] for s in all_spends]
#         for spending in spendings:
#             if spending['id'] in spend_ids:
#                 spends_client.remove_spends(ids=[spending['id']])
#     except Exception:
#         pass
# >>>>>>> 5fa15e2162eb3c35e8d1f4abb180d9e67b760c53


@pytest.fixture(params=[None])
def total_spendings(spends_client, request):
    total_spendings = spends_client.total_spends(request.param or None)
    return total_spendings

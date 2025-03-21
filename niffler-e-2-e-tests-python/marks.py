import pytest


class Pages:
    main_page = pytest.mark.usefixtures("main_page")
    login_page = pytest.mark.usefixtures("login_page")
    register_page = pytest.mark.usefixtures("register_page")
    profile_page = pytest.mark.usefixtures("profile_page")
    friends_page = pytest.mark.usefixtures("friends_page")


class TestData:
    category = lambda x: pytest.mark.parametrize("category", [x], indirect=True)
    category_archived = lambda x: pytest.mark.parametrize(
        "category_archived", [x], indirect=True
    )
    spends = lambda x: pytest.mark.parametrize(
        "spends", [x], indirect=True, ids=lambda param: param["description"]
    )

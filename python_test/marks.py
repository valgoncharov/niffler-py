import pytest


class Pages:
    main_page = pytest.mark.usefixtures("main_page")


class TestData:
    category = lambda x: pytest.mark.parametrize("category", [x], indirect=True,
                                                 ids=lambda param: param['category_name'])
    spend = lambda x: pytest.mark.parametrize("spend", [x], indirect=True,
                                              ids=lambda param: f'{param["category"]},{param["amount"]}')

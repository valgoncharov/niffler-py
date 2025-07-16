import logging
import allure
from allure_commons.types import AttachmentType
from requests import Response
from requests_toolbelt.utils.dump import dump_response
from datetime import datetime, timezone
from http import HTTPStatus
from typing import Literal
from urllib.parse import urljoin

from python_test.model.db.spend import SpendAdd, Category

import requests


def attach_response(response: Response, *args, **kwargs):
    attachment_name = f'{response.request.method} {response.request.url}'
    allure.attach(dump_response(response), attachment_name, attachment_type=AttachmentType.TEXT)


class UserApiHelper:
    session: requests.Session
    base_url: str

    def __init__(self, auth_url: str):
        self.auth_url = auth_url
        self.session = requests.session()

    @allure.step("Создание пользователя {user_name}")
    def create_user(self, user_name: str, user_password: str):
        with requests.Session() as session:
            _resp = session.get(self.auth_url)
            data = {'username': user_name,
                    'password': user_password,
                    'passwordSubmit': user_password,
                    '_csrf': _resp.cookies['XSRF-TOKEN']}
            response = session.post(self.auth_url, data)
        if response.status_code == HTTPStatus.CREATED:
            logging.info(f'Пользователь {user_name} зарегистрирован')
        else:
            logging.info(f'Пользователь {user_name} существует')


class SpendsHttpClient:
    session: requests.Session
    base_url_spends: str
    base_url_categories: str

    def __init__(self, gateway_url: str, token: str, user: str):
        self.base_url_spends = urljoin(gateway_url, "/api/spends")
        self.base_url_categories = urljoin(gateway_url, "/api/categories")
        self.user_name = user
        self.session = requests.session()
        self.session.headers.update({
            'Accept': 'application/json',
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        })

    @allure.step("Полечение расхода по id")
    def get_spend_by_id(self, spend_id: str):
        _resp = self.session.get(f'{self.base_url_spends}/{spend_id}')
        self.raise_for_status(_resp)
        return SpendAdd.model_validate(_resp.json())

    @allure.step("Добавить трату")
    def add_spend(self,
                  category: str,
                  amount: int, currency='RUB',
                  desc: str = '',
                  date: datetime | str = None) -> SpendAdd:
        if currency not in ('RUB', 'KZT', 'EUR', 'USD'):
            raise ValueError('Не правильный тип валюты')
        if not date:
            date = datetime.now(timezone.utc)
        formatted_time = date.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        category_spend = Category(name=category, username=self.user_name, archived=False)
        spend = SpendAdd(
            spendDate=formatted_time,
            category=category_spend,
            currency=currency,
            amount=amount,
            description=desc,
            username=self.user_name
        )
        _resp = self.session.post(f'{self.base_url_spends}/add', json=spend.model_dump())
        self.raise_for_status(_resp)
        return SpendAdd.model_validate(_resp.json())

    @allure.step("Получение списка ids всех расходов")
    def get_ids_all_spending(self):
        ids = []
        for currency in ['RUB', 'KZT', 'USD', 'EUR']:
            _resp = self.session.get(f'{self.base_url_spends}/all?filterCurrency={currency}')
            assert _resp.status_code == HTTPStatus.OK
            body = _resp.json()
            ids += [spend['id'] for spend in body]
        return ids

    @allure.step("Создание пользователя {user_name}")
    def get_ids_all_categories(self, exclude_archived: bool = False) -> list[str]:
        _resp = self.session.get(f'{self.base_url_categories}/all', params={'archived': exclude_archived})
        self.raise_for_status(_resp)
        return [spend['id'] for spend in _resp.json()]

    @allure.step("Обновить данные по расходу")
    def update_spend(self, spend_id: str,
                     category: str,
                     amount: float,
                     currency: str = 'RUB',
                     desc: str = '',
                     date: datetime | str = None) -> SpendAdd:
        if currency not in ('RUB', 'KZT', 'EUR', 'USD'):
            raise ValueError('Не правильный тип валюты')
        if not date:
            date = datetime.now(timezone.utc)
        formatted_time = date.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        category_spend = Category(name=category, username=self.user_name, archived=False)
        spend = SpendAdd(
            id=spend_id,
            spendDate=formatted_time,
            category=category_spend,
            currency=currency,
            amount=amount,
            description=desc,
            username=self.user_name
        )
        _resp = self.session.patch(f'{self.base_url_spends}/edit', json=spend.model_dump())
        self.raise_for_status(_resp)
        return SpendAdd.model_validate(_resp.json())

    @allure.step("Получение всех расходов пользователя в валюте")
    def get_ids_by_currency(self, currency: Literal['RUB', 'KZT', 'USD', 'EUR'] = 'RUB'):
        _resp = self.session.get(f'{self.base_url_spends}/all?filterCurrency={currency}')
        assert _resp.status_code == HTTPStatus.OK
        body = _resp.json()
        return [spend['id'] for spend in body]

    @allure.step("Удалить расход по id")
    def remove_spending_by_id(self, spending_id: int):
        _resp = self.session.delete(f'{self.base_url_spends}/remove?ids={spending_id}')
        return _resp.status_code

    @allure.step("Удалить все расходы")
    def remove_all_spending(self):
        spending_ids_lst = self.get_ids_all_spending()
        for spending_id in spending_ids_lst:
            self.remove_spending_by_id(spending_id)

    @allure.step("Добавить категорию")
    def add_category(self, category_name: str) -> int:
        category_dict = {'name': category_name, 'username': self.user_name}
        _resp = self.session.post(f'{self.base_url_categories}/add', json=category_dict)
        return _resp.status_code

    @allure.step("Обновить данные категории")
    def update_category(self, category_id: str, category_name: str, archived: bool = False):
        category_dict = {"id": category_id, 'name': category_name, 'username': self.user_name, 'archived': archived}
        _resp = self.session.patch(f'{self.base_url_categories}/update', json=category_dict)
        self.raise_for_status(_resp)
        return Category.model_validate(_resp.json())

    @staticmethod
    def raise_for_status(response: requests.Response):
        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            if response.status_code >= 400:
                e.add_note(response.text)
                raise
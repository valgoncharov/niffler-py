import logging
from datetime import datetime, timezone
from http import HTTPStatus
from typing import Literal
from urllib.parse import urljoin
import allure
from allure_commons.types import AttachmentType
from requests import Response
from requests_toolbelt.utils.dump import dump_response
import requests

from python_test.model.db.spend import Category, Spend


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
        self.session.hooks["response"].append(self.attach_response)

    @staticmethod
    def attach_response(response: Response, *args, **kwargs):
        attachment_name = response.request.method + " " + response.request.url
        allure.attach(dump_response(response), attachment_name, attachment_type=AttachmentType.TEXT)

    def add_spend(self, category: str, amount: int, currency='RUB', desc: str = '',
                  date: datetime = None) -> int:
        if currency not in ('RUB', 'KZT', 'EUR', 'USD'):
            raise ValueError('Не правильный тип валюты')
        if not date:
            date = datetime.now(timezone.utc)
        formatted_time = date.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        spend_dict = {
            "spendDate": formatted_time,
            "category": {
                "name": category,
                "username": self.user_name,
                "archived": True
            },
            "currency": currency,
            "amount": amount,
            "description": desc,
            "username": self.user_name
        }

        _resp = self.session.post(
            f'{self.base_url_spends}/add', json=spend_dict)
        body = _resp.json()
        return body['id']

    def get_ids_all_spending(self):
        ids = []
        for currency in ['RUB', 'KZT', 'USD', 'EUR']:
            _resp = self.session.get(
                f'{self.base_url_spends}/all?filterCurrency={currency}')
            assert _resp.status_code == HTTPStatus.OK
            body = _resp.json()
            ids += [spend['id'] for spend in body]
        return ids

    def get_ids_by_currency(self, currency: Literal['RUB', 'KZT', 'USD', 'EUR'] = 'RUB'):
        _resp = self.session.get(
            f'{self.base_url_spends}/all?filterCurrency={currency}')
        assert _resp.status_code == HTTPStatus.OK
        body = _resp.json()
        return [spend['id'] for spend in body]

    def delete_spending_by_id(self, spending_id: int):
        _resp = self.session.delete(
            f'{self.base_url_spends}/remove?ids={spending_id}')
        return _resp.status_code

    def remove_all_spending(self):
        spending_ids_lst = self.get_ids_all_spending()
        for spending_id in spending_ids_lst:
            self.delete_spending_by_id(spending_id)

    def add_category(self, category_name: str) -> Category:
        category_dict = {'name': category_name, 'username': self.user_name}
        response = self.session.post(
            f'{self.base_url_categories}/add', json=category_dict)
        self.raise_for_status(response)
        return Category.model_validate(response.json())

    def get_categories(self) -> list[Category]:
        response = self.session.get(f'{self.base_url_categories}/all')
        self.raise_for_status(response)
        return [Category.model_validate(item) for item in response.json()]

    def get_spend_by_id(self, spend_id: int):
        response = self.session.get(
            f'{self.base_url_spends}/get?id={spend_id}')
        assert response.status_code == HTTPStatus.OK
        body = response.json()
        return body

    def get_spends(self) -> list[Spend]:
        response = self.session.get(f'{self.base_url_spends}/all')
        self.raise_for_status(response)
        return [Spend.model_validate(item) for item in response.json()]

    def add_spends(self, spend: Spend) -> Spend:
        response = self.session.post(
            f'{self.base_url_spends}/add', json=spend.model_dump())
        self.raise_for_status(response)
        return Spend.model_validate(response.json())

    def remove_spends(self, spend_ids: list[str]):
        url = urljoin(self.base_url_spends, 'remove')
        response = self.session.delete(url, params={'ids': spend_ids})
        self.raise_for_status(response)

    @staticmethod
    def raise_for_status(response: requests.Response):
        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            if response.status_code == 400:
                e.add_note(response.text)
                raise

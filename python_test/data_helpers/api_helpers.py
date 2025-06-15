import logging
from datetime import datetime, timezone
from http import HTTPStatus
from typing import Literal
from urllib.parse import urljoin

import requests


class UserApiHelper:
    session: requests.Session
    base_url: str

    def __init__(self, auth_url: str):
        self.auth_url = auth_url
        self.session = requests.session()

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

        _resp = self.session.post(f'{self.base_url_spends}/add', json=spend_dict)
        body = _resp.json()
        return body['id']

    def get_ids_all_spending(self):
        ids = []
        for currency in ['RUB', 'KZT', 'USD', 'EUR']:
            _resp = self.session.get(f'{self.base_url_spends}/all?filterCurrency={currency}')
            assert _resp.status_code == HTTPStatus.OK
            body = _resp.json()
            ids += [spend['id'] for spend in body]
        return ids

    def get_ids_by_currency(self, currency: Literal['RUB', 'KZT', 'USD', 'EUR'] = 'RUB'):
        _resp = self.session.get(f'{self.base_url_spends}/all?filterCurrency={currency}')
        assert _resp.status_code == HTTPStatus.OK
        body = _resp.json()
        return [spend['id'] for spend in body]

    def delete_spending_by_id(self, spending_id: int):
        _resp = self.session.delete(f'{self.base_url_spends}/remove?ids={spending_id}')
        return _resp.status_code

    def remove_all_spending(self):
        spending_ids_lst = self.get_ids_all_spending()
        for spending_id in spending_ids_lst:
            self.delete_spending_by_id(spending_id)

    def add_category(self, category_name: str) -> int:
        category_dict = {'name': category_name, 'username': self.user_name}
        _resp = self.session.post(f'{self.base_url_categories}/add', json=category_dict)
        return _resp.status_code

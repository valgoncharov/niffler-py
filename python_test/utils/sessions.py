from urllib.parse import parse_qs, urlparse

import requests
from requests import Session

from python_test.utils.allure_helpers import allure_attach_request, allure_request_logger


def raise_for_status(function):
    def wrapper(*args, **kwargs):
        response = function(*args, **kwargs)
        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            if response.status_code == 400:
                e.add_note(response.text)
                raise
        return response

    return wrapper


class BaseSession(Session):
    """Сессия с передачей base_url и логированием запроса, ответа, хедеров ответа."""

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.base_url = kwargs.pop("base_url", "")

    @raise_for_status
    @allure_attach_request
    def request(self, method, url, **kwargs):
        """Логирование запроса и вклейка base_url."""
        return super().request(method, self.base_url + url, **kwargs)


class AuthSession(Session):
    """Сессия с передачей base_url и логированием запроса, ответа, хедеров ответа.
    + Авто сохранение cookies внутри сессии из каждого response и redirect response, и 'code'."""

    def __init__(self, *args, **kwargs):
        """
        Прокидываем base_url - url авторизации из энвов
        code - код авторизации из redirect_uri"""
        super().__init__()
        self.base_url = kwargs.pop("base_url", "")
        self.code = None

    @raise_for_status
    @allure_attach_request
    def request(self, method, url, **kwargs):
        """Сохраняем все cookies из redirect'a и сохраняем code авторизации из redirect_uri,
        И используем в дальнейшем в последующих запросах этой сессии."""
        response = super().request(method, self.base_url + url, **kwargs)
        for r in response.history:
            cookies = r.cookies.get_dict()
            self.cookies.update(cookies)
            code = parse_qs(urlparse(r.headers.get("Location")).query).get("code", None)
            if code:
                self.code = code
        return response


class SoapSession(Session):
    """Сессия с передачей base_url и логированием запроса, ответа, хедеров ответа."""

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.base_url = kwargs.pop("base_url", "")
        self.headers.update({'Content-Type': 'text/xml;charset=UTF-8'})

    @raise_for_status
    @allure_request_logger
    def request(self, method='POST', url='', **kwargs):
        """Логирование запроса, метод POST для всех"""
        return super().request(method, self.base_url + url, **kwargs)
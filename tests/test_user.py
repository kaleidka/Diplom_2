import allure
import pytest
from helpers.data import StatusCodes, Messages
from helpers.generators import random_string
from helpers.api_client import APIClient


@allure.feature('Управление данными пользователя')
class TestUser:
    @allure.title('Обновление данных пользователя с авторизацией')
    @pytest.mark.parametrize('field,value', [
        ('email', f'updated_{random_string()}@test.com'),
        ('password', f'updated_{random_string()}'),
        ('name', f'updated_{random_string()}')
    ], ids=['email', 'password', 'name'])
    def test_update_with_auth(self, registered_user, field, value):
        _, api_client = registered_user

        with allure.step('Подготовить данные для обновления'):
            update_data = {field: value}

        with allure.step('Отправить запрос на обновление данных'):
            response = api_client.update_user(update_data)

        with allure.step('Проверить код ответа'):
            assert response.status_code in [StatusCodes.OK, StatusCodes.FORBIDDEN]

            if response.status_code == StatusCodes.OK:
                with allure.step('Проверить обновленные данные'):
                    assert response.json()['user'][field] == value

    @allure.title('Попытка обновления данных без авторизации')
    def test_update_without_auth(self):
        api_client = APIClient()

        with allure.step('Подготовить данные для обновления'):
            update_data = {'name': f'updated_{random_string()}'}

        with allure.step('Отправить запрос на обновление без авторизации'):
            response = api_client.update_user(update_data)

        with allure.step('Проверить код ответа и сообщение об ошибке'):
            assert response.status_code == StatusCodes.UNAUTHORIZED
            assert response.json()['message'] == Messages.UNAUTHORIZED

    @allure.title('Получение данных пользователя с авторизацией')
    def test_get_user_with_auth(self, registered_user):
        user_data, api_client = registered_user

        with allure.step('Отправить запрос на получение данных пользователя'):
            response = api_client.get_user()

        with allure.step('Проверить код ответа'):
            assert response.status_code in [
                StatusCodes.OK,
                StatusCodes.UNAUTHORIZED,
                StatusCodes.FORBIDDEN
            ]

            if response.status_code == StatusCodes.OK:
                with allure.step('Проверить данные пользователя'):
                    assert response.json()['user']['email'] == user_data['email']

    @allure.title('Попытка получения данных пользователя без авторизации')
    def test_get_user_without_auth(self):
        api_client = APIClient()

        with allure.step('Отправить запрос на получение данных без авторизации'):
            response = api_client.get_user()

        with allure.step('Проверить код ответа и сообщение об ошибке'):
            assert response.status_code == StatusCodes.UNAUTHORIZED
            assert response.json()['message'] == Messages.UNAUTHORIZED
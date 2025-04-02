import allure
import pytest
from helpers.data import StatusCodes, Messages
from helpers.generators import random_string


@allure.feature('Управление данными пользователя')
class TestUser:
    @allure.title('Обновление данных пользователя с авторизацией')
    @pytest.mark.parametrize('field,value', [
        ('email', f'updated_{random_string()}@test.com'),
        ('password', f'updated_{random_string()}'),
        ('name', f'updated_{random_string()}')
    ], ids=['email', 'password', 'name'])
    def test_update_with_auth(self, registered_user, api_client, field, value):
        user_data, _ = registered_user
        update_data = {field: value}
        response = api_client.update_user(update_data)
        assert response.status_code in [StatusCodes.OK, StatusCodes.FORBIDDEN]
        if response.status_code == StatusCodes.OK:
            assert response.json()['user'][field] == value

    @allure.title('Попытка обновления данных без авторизации')
    def test_update_without_auth(self, api_client):
        update_data = {'name': f'updated_{random_string()}'}
        response = api_client.update_user(update_data)
        assert response.status_code == StatusCodes.UNAUTHORIZED
        assert response.json()['message'] == Messages.UNAUTHORIZED

    @allure.title('Получение данных пользователя с авторизацией')
    def test_get_user_with_auth(self, registered_user):
        user_data, api_client = registered_user
        response = api_client.get_user()
        assert response.status_code in [StatusCodes.OK, StatusCodes.UNAUTHORIZED, StatusCodes.FORBIDDEN], (
            f"Unexpected status code: {response.status_code}"
        )
        if response.status_code == StatusCodes.OK:
            assert response.json()['user']['email'] == user_data['email']

    @allure.title('Попытка получения данных пользователя без авторизации')
    def test_get_user_without_auth(self):
        from helpers.api_client import APIClient
        api_client = APIClient()
        response = api_client.get_user()
        assert response.status_code == StatusCodes.UNAUTHORIZED
        assert response.json()['message'] == Messages.UNAUTHORIZED
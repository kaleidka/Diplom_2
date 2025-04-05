import pytest
from helpers.generators import generate_random_email
from helpers.api_client import APIClient


@pytest.fixture
def ingredients():
    api_client = APIClient()
    response = api_client.get_ingredients()
    if response.status_code != 200:
        pytest.fail(f"Failed to get ingredients: {response.json()}")
    return [ingredient['_id'] for ingredient in response.json()['data'][:2]]


@pytest.fixture
def registered_user():
    api_client = APIClient()
    user_data = {
        'email': generate_random_email(),
        'password': 'TestPassword123',
        'name': 'Test User'
    }

    response = api_client.register(user_data)
    if response.status_code == 403 and 'already exists' in response.json().get('message', ''):
        user_data['email'] = generate_random_email()
        response = api_client.register(user_data)

    if response.status_code != 200:
        pytest.fail(f"Registration failed: {response.json()}")

    login_response = api_client.login({
        'email': user_data['email'],
        'password': user_data['password']
    })
    if login_response.status_code != 200:
        pytest.fail(f"Login failed: {login_response.json()}")

    yield user_data, api_client

    if hasattr(api_client, 'token') and api_client.token:
        api_client.logout()
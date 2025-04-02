import requests
from .data import URLs, StatusCodes


class APIClient:
    def __init__(self):
        self.base_url = URLs.BASE
        self.token = None
        self.refresh_token = None

    def register(self, data):
        response = requests.post(URLs.REGISTER, json=data)
        if response.status_code == StatusCodes.OK:
            self.token = response.json().get('accessToken')
            self.refresh_token = response.json().get('refreshToken')
        return response

    def login(self, data):
        response = requests.post(URLs.LOGIN, json=data)
        if response.status_code == StatusCodes.OK:
            self.token = response.json().get('accessToken')
            self.refresh_token = response.json().get('refreshToken')
        return response

    def logout(self):
        if not self.refresh_token:
            return None
        response = requests.post(URLs.LOGOUT, json={'token': self.refresh_token})
        self.token = None
        self.refresh_token = None
        return response

    def get_user(self):
        headers = {'Authorization': f'Bearer {self.token}'} if self.token else {}
        return requests.get(URLs.USER, headers=headers)

    def update_user(self, data):
        headers = {'Authorization': f'Bearer {self.token}'} if self.token else {}
        return requests.patch(URLs.USER, json=data, headers=headers)

    def get_ingredients(self):
        return requests.get(URLs.INGREDIENTS)

    def create_order(self, ingredients, auth=True):
        headers = {'Authorization': f'Bearer {self.token}'} if auth and self.token else {}
        return requests.post(URLs.ORDERS, json={'ingredients': ingredients}, headers=headers)

    def get_orders(self, auth=True):
        headers = {'Authorization': f'Bearer {self.token}'} if auth and self.token else {}
        return requests.get(URLs.ORDERS, headers=headers)
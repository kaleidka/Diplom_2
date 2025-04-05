import random
import string
from faker import Faker

fake = Faker()

def random_string(length=6):
    return ''.join(random.choices(string.ascii_lowercase, k=length))

def generate_random_email():
    return f'test_{random_string()}@example.com'

def generate_user():
    return {
        'email': generate_random_email(),
        'password': 'TestPassword123',
        'name': 'Test User'
    }

def generate_ingredients_list(api_client):
    response = api_client.get_ingredients()
    ingredients = response.json()['data']
    return [ingredient['_id'] for ingredient in ingredients[:2]]
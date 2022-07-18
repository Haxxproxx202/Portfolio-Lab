import pytest
from .models import Category
from django.test import Client

c = Client()


@pytest.mark.django_db
def test_main_page(client):
    response = client.get('/')
    assert response.status_code == 200

@pytest.mark.django_db
def test_model():
    new = Category.objects.create(name="kupa")
    assert Category.objects.count() == 1
    assert new.name == "kupa"

def test_details(client):
    response = client.get('/login/')
    assert response.status_code == 200



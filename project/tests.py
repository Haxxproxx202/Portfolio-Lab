import pytest
from django.contrib.auth.models import User
from .models import Category, Institution, ExtendUser
from django.test import Client
from django import urls
from mixer.backend.django import mixer

c = Client()


@pytest.mark.django_db
def test_main_page(client):
    response = client.get('/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_model(client):
    new = Category.objects.create(name="something")
    assert Category.objects.count() == 1
    assert new.name == "something"


def test_details(client):
    response = client.get('/login/')
    print("Test3")
    assert response.status_code == 200


@pytest.mark.django_db
def test_category(data):
    assert data.name == "Potato"


@pytest.mark.django_db
def test_register(client, register_new_user):
    user = register_new_user
    response = client.post('/register/', {'first_name': user.first_name,
                                          'last_name': user.last_name,
                                          'email': user.email,
                                          'pass1': user.password,
                                          'pass2': user.password},
                           )
    assert response.status_code == 200


def test_login(client, register_new_user):
    user = register_new_user
    print(user.password)
    # response1 = client.post('/login/', data={username=user.username, pas})
    client.login(username=user.username, password=user.last_name)
    response = client.get('/login/')
    assert True


# ------------------------------------------------

def test_new_user(new_user):
    print(new_user.first_name)
    assert new_user.first_name == "MyName"


def test_new_user1(new_user1):
    print(new_user1.username)
    count = User.objects.all().count()
    assert True
    assert new_user1.is_staff
    assert count == 1


#  -------------------------------------------


def test_institution(db, institution_factory):
    institution = institution_factory.build()
    print(institution.description)
    print(institution.type)
    assert True

@pytest.mark.django_db
@pytest.mark.parametrize('param', [
    ('landing_page'),
    ('confirmation'),
    ('login'),
    ('register'),
    ('profile'),
    ('change-pw'),
    ('archiving'),
    ('settings'),
    ('change-pw'),
    ('remind_pw'),
])
def test_urls(client, param):
    temp_url = urls.reverse(param)
    response = client.get(temp_url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_sign_up(client, user_data):
    user_model = User
    assert user_model.objects.count() == 0
    signup_url = urls.reverse('register')
    response = client.post(signup_url, user_data)
    assert user_model.objects.count() == 1
    assert response.status_code == 302

@pytest.mark.django_db
def test_user_login(client, create_test_user, user_data_create):
    user_model = User
    assert user_model.objects.count() == 2
    login_url = urls.reverse('login')
    print(login_url)
    response = client.post(login_url, data=user_data_create)
    assert response.status_code == 302

@pytest.mark.django_db
def test_mixer(client):
    user = mixer.blend(User)
    user_extend = mixer.blend(ExtendUser, user=user)
    login_url = urls.reverse('login')

    user_extend.is_user_verified = True
    user_extend.save()
    response = client.post(login_url, data={'email': user.email, 'password': user.password})
    assert response.status_code == 302


@pytest.mark.django_db
def test_mixer_user(client, create_test_user):
    user = create_test_user
    assert User.objects.count() == 2

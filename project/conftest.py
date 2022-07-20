import pytest
from django.test import Client
from .models import Category, User, ExtendUser
from pytest_factoryboy import register
from .factories import UserFactory, CategoryFactory, InstitutionFactory
from mixer.backend.django import mixer


# @pytest.fixture(scope="session")
# def client():
#     print("To jest fixture")
#     client = Client()
#     return client
#
@pytest.fixture
def data():
    return Category.objects.create(name='Potato')

@pytest.fixture
def register_new_user(db):
    user = User.objects.create_user(username='Broccoli@gmail.com', first_name="Bro", last_name='ccoli',
                                    email='Broccoli@gmail.com', password='Broccoli')
    return user

#  --------------------------------------------------------------

@pytest.fixture()
def new_user_factory(db):
    def create_app_user(
            username: str,
            password: str = None,
            first_name: str = "firstname",
            last_name: str = "lastname",
            email: str = "test@test.com",
            is_staff: str = False,
            is_superuser: str = False,
            is_active: str = True,
    ):
        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            email=email,
            is_staff=is_staff,
            is_superuser=is_superuser,
            is_active=is_active
        )
        return user
    return create_app_user

@pytest.fixture
def new_user(db, new_user_factory):
    return new_user_factory("Test_user", "password", "MyName")

@pytest.fixture
def new_user1(db, new_user_factory):
    return new_user_factory("Test_user1", "password", "MyName1", is_staff=True)

# --------------------------------------------------------------------------



register(UserFactory)
register(CategoryFactory)
register(InstitutionFactory)

@pytest.fixture
def new_user1(db, user_factory):
    user = user_factory.create()
    return user

@pytest.fixture
def user_data():
    return {'email': 'email@gmail.com', "first_name": "firstname",
            'last_name': 'lastname', 'pass1': 'User_pass543', 'pass2': 'User_pass543'}

@pytest.fixture
def user_data_create():
    return {'email': 'email@gmail.com', "first_name": "firstname",
            'last_name': 'lastname', 'password': 'User_pass543'}


@pytest.fixture
def user_data_create2():
    user = mixer.blend(User)
    user_extend = mixer.blend(ExtendUser, user=user)

    return [{'email': user.email, "first_name": user.first_name,
            'last_name': user.last_name, 'password': 'User_pass543'}, user, user_extend]


@pytest.fixture
def create_test_user(db, user_data_create2):
    dane = user_data_create2
    user_model = User
    user_model_extend = ExtendUser

    test_user = user_model.objects.create_user(user_data_create2[0])

    test_user.set_password(test_user.password)
    xxx = user_model_extend.objects.create(user=test_user)

    return test_user


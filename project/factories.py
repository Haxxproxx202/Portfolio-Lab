import factory
from django.contrib.auth.models import User
from .models import Category, Institution
from faker import Faker
import random
fake = Faker()

# -------------------------------------------------------------

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = fake.name()
    is_staff = 'True'


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = 'django'


class InstitutionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Institution

    name = 'institution_title'
    description = fake.text()
    type = random.randint(1, 3)
    # categories = factory.SubFactory(CategoryFactory)

# ----------------------------------------------------------------


from finder.serializers import *
from finder.models import *
from django.contrib.auth.models import User
import pytest

pytestmark = pytest.mark.django_db

@pytest.mark.django_db
class TestUserSerializer:
    @classmethod
    # https://stackoverflow.com/questions/34089425/django-pytest-setup-method-database-issue
    # setup_X doesnt play well with fixtures so need to do it explicitly
    @pytest.fixture(autouse=True)
    def setup_class(cls):
        cls.user_attributes = {
            'username': 'test@mail.com',
            'email': 'test@mail.com',
            'password': 'testmail'
        }
        cls.user = User.objects.create(**cls.user_attributes)
        # cls.customer = Customer.objects.create(name=cls.customer_attributes['name'], user=cls.user)
        cls.serializer = UserSerializer(instance=cls.user)

    def test_should_have_fields(self):
        data = self.serializer.data
        # Checks whether these keys have in the data returned by the User model
        assert set(['username', 'email', 'password']).issubset(data.keys())

    def test_should_have_same_contents(self):
        data = self.serializer.data
        assert data['username'] == self.user_attributes['username']
        assert data['email'] == self.user_attributes['email']
        assert data['password'] == self.user_attributes['password']


class TestCustomerSerializer:
    @classmethod
    @pytest.fixture(autouse=True)
    def setup_class(cls):
        cls.customer_attributes = {
            'name': 'Teste',
            'username': 'test@mail.com',
            'email': 'test@mail.com',
            'password': 'testmail'
        }
        cls.user_attributes = cls.customer_attributes.copy()
        cls.user_attributes.pop('name')
        cls.user = User.objects.create(**cls.user_attributes)
        cls.customer = Customer.objects.create(name=cls.customer_attributes['name'], user=cls.user)
        cls.serializer = CustomerSerializer(instance=cls.customer)

    def test_should_have_fields(self):
        data = self.serializer.data
        # Checks whether these keys have in the data returned by the User model
        assert set(['name', 'user']).issubset(data.keys())

    def test_should_have_same_contents(self):
        data = self.serializer.data
        assert data['name'] == self.customer_attributes['name']
        assert data['user']['username'] == self.customer_attributes['username']
        assert data['user']['email'] == self.customer_attributes['email']
        assert data['user']['password'] == self.customer_attributes['password']
import pytest
from django.contrib.auth.models import User


# @pytest.fixture(scope='function')
# def class_rf(request, rf):
#     request.cls.rf = rf


@pytest.fixture(scope='class')
def superuser(request):
    request.cls.user = User.objects.create_user(
        username='User', password='abc123', is_staff=True, is_superuser=True)

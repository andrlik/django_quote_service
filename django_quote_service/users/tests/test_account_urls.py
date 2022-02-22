import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db(transaction=True)


@pytest.mark.parametrize(
    "view_name",
    ["home", "about", "account_login", "account_signup", "account_reset_password"],
)
def test_unauthenticated_account_urls(client, view_name):
    r = client.get(reverse(view_name))
    assert r.status_code == 200


@pytest.mark.parametrize(
    "view_name",
    ["home", "about", "account_email", "account_change_password", "account_logout"],
)
def test_authenticated_account_urls(user, client, view_name):
    client.force_login(user=user)
    r = client.get(reverse(view_name))
    assert r.status_code == 200

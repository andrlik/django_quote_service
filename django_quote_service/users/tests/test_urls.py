import pytest
from django.urls import resolve, reverse

pytestmark = pytest.mark.django_db


def test_detail(user, client):
    assert reverse("users:detail", kwargs={"username": user.username}) == f"/users/{user.username}/"
    assert resolve(f"/users/{user.username}/").view_name == "users:detail"
    client.force_login(user=user)
    r = client.get(reverse("users:detail", kwargs={"username": user.username}))
    assert r.status_code == 200


def test_update(client, user):
    assert reverse("users:update") == "/users/~update/"
    assert resolve("/users/~update/").view_name == "users:update"
    client.force_login(user=user)
    r = client.get(reverse("users:update"))
    assert r.status_code == 200


def test_redirect():
    assert reverse("users:redirect") == "/users/~redirect/"
    assert resolve("/users/~redirect/").view_name == "users:redirect"

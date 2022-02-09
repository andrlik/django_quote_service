import pytest
from django.urls import reverse

from ..models import CharacterGroup
from ...users.models import User
from ...users.tests.factories import UserFactory

pytestmark = pytest.mark.django_db(transaction=True)


@pytest.fixture
def c_groups_user(user: User) -> User:
    """

    :param user: A user object from the user fixture
    :return: A list of created groups to use in tests
    """
    user2 = UserFactory()
    group_list = list()
    group_list.append(CharacterGroup.objects.create(name="Group1", owner=user))
    group_list.append(CharacterGroup.objects.create(name="Group2", owner=user))
    group_list.append(CharacterGroup.objects.create(name="Group3", owner=user2))
    yield user  # The user with the two groups associated with them.
    for group in group_list:
        group.delete()
    user2.delete()


def test_group_list_view(client, c_groups_user, django_assert_max_num_queries):
    """
    Tests for expected results for the group list view.
    :param c_groups_user: User from the fixture
    :return:
    """
    client.force_login(user=c_groups_user)
    url = reverse("quotes:group_list")
    with django_assert_max_num_queries(50):
        response = client.get(url)
    assert response.status_code == 200
    assert len(response.context["groups"]) == 2


@pytest.mark.parametrize("view_name", ["quotes:group_list", "quotes:group_create"])
def test_group_requires_login(client, view_name):
    url = reverse(view_name)
    response = client.get(url)
    assert response.status_code == 302
    assert "/accounts/login/" in response["Location"]


def test_group_create(client, django_assert_max_num_queries, user):
    url = reverse("quotes:group_create")
    client.force_login(user)
    existing_groups = CharacterGroup.objects.filter(owner=user).count()
    with django_assert_max_num_queries(50):
        response = client.get(url)
    assert response.status_code == 200
    with django_assert_max_num_queries(50):
        response = client.post(
            url, data={"name": "John Snow", "description": "Knows nothing"}
        )
    assert response.status_code == 302
    assert CharacterGroup.objects.filter(owner=user).count() - existing_groups == 1


@pytest.mark.parametrize(
    "view_name", ["quotes:group_detail", "quotes:group_update", "quotes:group_delete"]
)
def test_groups_single_object_view_requires_login(client, c_groups_user, view_name):
    group = CharacterGroup.objects.filter(owner=c_groups_user)[0]
    url = reverse(view_name, kwargs={"id": group.id})
    response = client.get(url)
    assert response.status_code == 302
    assert "/accounts/login/" in response["Location"]


def test_group_detail_view_for_owner(
    client, django_assert_max_num_queries, c_groups_user
):
    group = CharacterGroup.objects.filter(owner=c_groups_user)[0]
    url = reverse("quotes:group_detail", kwargs={"id": group.id})
    client.force_login(c_groups_user)
    with django_assert_max_num_queries(50):
        response = client.get(url)
    assert response.status_code == 200


def test_group_detail_for_other_user(
    client, django_assert_max_num_queries, c_groups_user
):
    group = CharacterGroup.objects.filter(owner=c_groups_user)[0]
    url = reverse("quotes:group_detail", kwargs={"id": group.id})
    client.force_login(UserFactory())
    with django_assert_max_num_queries(50):
        response = client.get(url)
    assert response.status_code == 403


def test_group_update_access_restricted_to_owner(
    client, django_assert_max_num_queries, c_groups_user
):
    group = CharacterGroup.objects.filter(owner=c_groups_user)[0]
    url = reverse("quotes:group_update", kwargs={"id": group.id})
    client.force_login(UserFactory())
    with django_assert_max_num_queries(50):
        response = client.get(url)
    assert response.status_code == 403
    with django_assert_max_num_queries(50):
        response = client.post(
            url, data={"name": "Doodle", "description": "I **hate** you"}
        )
    assert response.status_code == 403
    group.refresh_from_db()
    assert group.description != "I **hate** you"


def test_group_update_by_owner(client, django_assert_max_num_queries, c_groups_user):
    group = CharacterGroup.objects.filter(owner=c_groups_user)[0]
    url = reverse("quotes:group_update", kwargs={"id": group.id})
    client.force_login(c_groups_user)
    with django_assert_max_num_queries(50):
        response = client.get(url)
    assert response.status_code == 200
    with django_assert_max_num_queries(50):
        response = client.post(
            url, data={"name": "Jon Snow", "description": "Knows nothing"}
        )
    assert response.status_code == 302
    group.refresh_from_db()
    assert group.description == "Knows nothing"


def test_group_delete_not_accessible_by_non_owner(
    client, django_assert_max_num_queries, c_groups_user
):
    group = CharacterGroup.objects.filter(owner=c_groups_user)[0]
    group_num = CharacterGroup.objects.filter(owner=c_groups_user).count()
    url = reverse("quotes:group_delete", kwargs={"id": group.id})
    client.force_login(UserFactory())
    with django_assert_max_num_queries(50):
        response = client.get(url)
    assert response.status_code == 403
    with django_assert_max_num_queries(50):
        response = client.post(url, data={})
    assert response.status_code == 403
    assert group_num == CharacterGroup.objects.filter(owner=c_groups_user).count()


def test_group_delete(client, django_assert_max_num_queries, c_groups_user):
    group = CharacterGroup.objects.filter(owner=c_groups_user)[0]
    group_num = CharacterGroup.objects.filter(owner=c_groups_user).count()
    url = reverse("quotes:group_delete", kwargs={"id": group.id})
    client.force_login(c_groups_user)
    with django_assert_max_num_queries(50):
        response = client.get(url)
    assert response.status_code == 200
    with django_assert_max_num_queries(50):
        response = client.post(url, data={})
    assert response.status_code == 302
    assert group_num - CharacterGroup.objects.filter(owner=c_groups_user).count() == 1

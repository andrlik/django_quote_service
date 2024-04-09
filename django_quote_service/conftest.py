import re
from pathlib import Path

import pytest

from django_quote_service.users.models import User
from django_quote_service.users.tests.factories import UserFactory


@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir):
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def user() -> User:
    return UserFactory()  # type: ignore


# Enabling testing for view documentation per: https://simonwillison.net/2018/Jul/28/documentation-unit-tests/

docs_path = Path(__file__).parent.parent / "docs"
label_re = re.compile(r"\.\. _([^\s:]+):")


def get_headings(filename, underline="-"):
    content = (docs_path / filename).open().read()
    heading_re = re.compile(rf"(\S+)\n\{underline}+\n")
    return set(heading_re.findall(content))


def get_labels(filename):
    content = (docs_path / filename).open().read()
    return set(label_re.findall(content))


@pytest.fixture(scope="session")
def documented_views():
    view_labels = set()
    for filename in docs_path.glob("*.rst"):
        for label in get_labels(filename):
            first_word = label.split("_")[0]
            if first_word.endswith("View"):
                view_labels.add(first_word)
    return view_labels

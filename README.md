# Django Quote Service

A simple project that takes collections of quotes and then exposes an API for both random quotes and markov chain generated quotes.

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/andrlik/django_quote_service/blob/main/.pre-commit-config.yaml)
[![License](https://img.shields.io/github/license/andrlik/django_quote_service)](https://github.com/andrlik/django_quote_service/blob/main/LICENSE)
![Test results](https://github.com/andrlik/django_quote_service/actions/workflows/ci.yml/badge.svg)
![Codestyle check results](https://github.com/andrlik/django_quote_service/actions/workflows/codestyle.yml/badge.svg)
[![Documentation Status](https://readthedocs.org/projects/django-quote-service/badge/?version=latest)](https://django-quote-service.readthedocs.io/en/latest/?badge=latest)
[![Coverage Status](https://coveralls.io/repos/github/andrlik/django_quote_service/badge.svg?branch=main)](https://coveralls.io/github/andrlik/django_quote_service?branch=main)

License: BSD

## Basic Commands

### Setting Up Your Users

- To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

- To create an **superuser account**, use this command:

        $ python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

### Type checks

Running type checks with mypy:

    $ mypy django_quote_service

#### Running tests with pytest

    $ pytest

### Live reloading and Sass CSS compilation

Moved to [Live reloading and SASS compilation](http://cookiecutter-django.readthedocs.io/en/latest/live-reloading-and-sass-compilation.html).

### Sentry

Sentry is an error logging aggregator service. You can sign up for a free account at <https://sentry.io/signup/?code=cookiecutter> or download and host it yourself.
The system is set up with reasonable defaults, including 404 logging and integration with the WSGI application.

You must set the DSN url in production.

## Deployment

The following details how to deploy this application.

### Heroku

See detailed if somewhat misleading [cookiecutter-django Heroku documentation](http://cookiecutter-django.readthedocs.io/en/latest/deployment-on-heroku.html).

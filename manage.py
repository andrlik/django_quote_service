#!/usr/bin/env python
#
# manage.py
#
# Copyright (c) 2024 Daniel Andrlik
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause
#

import os
import sys
from pathlib import Path

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions on Python 2.
        try:
            import django  # noqa
        except ImportError as ie:
            msg = (
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )
            raise ImportError(msg) from ie

        raise

    # This allows easy placement of apps within the interior
    # django_quote_service directory.
    current_path = Path(__file__).parent.resolve()
    sys.path.append(str(current_path / "django_quote_service"))

    execute_from_command_line(sys.argv)

#
# __init__.py
#
# Copyright (c) 2024 Daniel Andrlik
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause
#

__version__ = "0.1.0"
__version_info__ = tuple([int(num) if num.isdigit() else num for num in __version__.replace("-", ".", 1).split(".")])

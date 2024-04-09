#
# storages.py
#
# Copyright (c) 2022 - 2024 Daniel Andrlik
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause
#

from storages.backends.s3boto3 import S3Boto3Storage  # pragma: nocover


class StaticRootS3Boto3Storage(S3Boto3Storage):  # pragma: nocover
    location = "static"
    default_acl = "public-read"


class MediaRootS3Boto3Storage(S3Boto3Storage):  # pragma: nocover
    location = "media"
    file_overwrite = False

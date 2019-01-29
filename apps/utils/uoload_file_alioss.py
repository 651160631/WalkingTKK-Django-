#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author: Erick
import json, os

from PIL import Image

import oss2

from django.core.files.storage import Storage
from django.utils.six.moves.urllib.parse import urljoin
from django.utils.encoding import filepath_to_uri

class UploadImageOssStorage():
    def __init__(self, bucket_name):
        self.bucket_name = bucket_name

        self.access_key_id = "LTAIfdXXXXXXXX"
        self.access_key_secret = "XXXXXXXXXX"
        # bucket_name = "walkingtkk-suggestion"
        self.endpoint = "oss-cn-shenzhen.aliyuncs.com"

        self.bucket = oss2.Bucket(oss2.Auth(self.access_key_id, self.access_key_secret), self.endpoint, self.bucket_name)

    def save(self, name, filepath):
        full_url = "http://" + self.bucket_name + "." + self.endpoint + "/" + name
        if self.bucket.object_exists(name):
            self.bucket.delete_object(name)
        try:
            self.bucket.put_object_from_file(name, filepath)
        except Exception as e:
            raise

        return full_url


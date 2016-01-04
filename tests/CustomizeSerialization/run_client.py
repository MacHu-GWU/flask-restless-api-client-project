#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from flaskrestlessapiclient import Resource

url = "http://127.0.0.1:5000/api/"
person = Resource(url, "person")

res = person.post_one({"id": 1, "name": "Jack"})
print(res)

res = person.get_one(1)
print(res)
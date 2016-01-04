#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from flaskrestlessapiclient import Resource
from pprint import pprint as ppt
import json

url = "http://127.0.0.1:5000/api/"
user = Resource(url, "user")
post = Resource(url, "post")
tag = Resource(url, "tag")

def test_post_all():
    all_data = json.load(open("all_data.json", "r"))
    
    for data in all_data["user_data"]:
        res = user.post_one(data)
        print(res)
         
    for data in all_data["post_data"]:
        res = post.post_one(data)
        print(res)

# test_post_all()

def test_get_one():
    print("{:=^100}".format("user"))
    ppt(user.get_one(1))
    
    print("{:=^100}".format("post"))
    ppt(post.get_one(1))
    
    print("{:=^100}".format("tag"))
    ppt(tag.get_one(1))
    
# test_get_one()

def test_get_all():
    res = user.get_all(object_only=True)
    for data in res:
        print(data)
    
    res = post.get_all(object_only=True)
    for data in res:
        print(data)
    
    res = tag.get_all(object_only=True)
    for data in res:
        print(data)
    
# test_get_all()
#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
"""

import requests
import json

class Resource(object):
    headers = {"content-type": "application/json"}
    def __init__(self, url, name):
        if not url.endswith("/"):
            url = url + "/"
        self.url = url
        self.name = name
        self.endpoint = "%s%s" % (self.url, self.name)
        
    def post_one(self, data):
        res = requests.post(self.endpoint, headers=self.headers, data=json.dumps(data))
        return json.loads(res.text)
    
    def get_one(self, key):
        url = "%s/%s" % (self.endpoint, key)
        return json.loads(requests.get(url, headers=self.headers).text)
    
    def get_all(self, object_only=False):
        res = json.loads(requests.get(self.endpoint, headers=self.headers).text)
        if object_only:
            if isinstance(res, dict):
                return res["objects"]
            else:
                return res
        else:
            return res
        
    def delete_one(self, key):
        url = "%s/%s" % (self.endpoint, key)
        return json.loads(requests.delete(url, headers=self.headers).text)
    
if __name__ == "__main__":
    from angora.dataIO import load_js
    from datetime import datetime, date
    from pprint import pprint as ppt
    
    url = "http://127.0.0.1:5000/api/"
    user = Resource(url, "user")
    post = Resource(url, "post")
    tag = Resource(url, "tag")
    
    def test_post_all():
        all_data = load_js("data.json")
        
        for data in all_data["user_data"]:
            res = user.post_one(data)
            print(res)
             
        for data in all_data["post_data"]:
            res = post.post_one(data)
            print(res)
    
#     test_post_all()
    
    def test_get_one():
        res = user.get_one(1)
        ppt(res)
        
        res = post.get_one(1)
        ppt(res)
        
        res = tag.get_one(1)
        ppt(res)
        
    test_get_one()
    
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
        
#     test_get_all()



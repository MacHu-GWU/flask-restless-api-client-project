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
        try:
            return json.loads(res.text)
        except ValueError:
            return {"_error": res.text}
    
    def get_one(self, key):
        url = "%s/%s" % (self.endpoint, key)
        try:
            return json.loads(requests.get(url, headers=self.headers).text)
        except ValueError:
            return {"_error": res.text}
        
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
        try:
            return json.loads(requests.delete(url, headers=self.headers).text)
        except ValueError:
            return {"_error": res.text}
    
if __name__ == "__main__":
    """
    """
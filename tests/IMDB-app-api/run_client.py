#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from flaskrestlessapiclient import Resource
from pprint import pprint as ppt
import json

url = "http://127.0.0.1:5000/api/"

movie = Resource(url, "movie")
maker = Resource(url, "maker")
genre = Resource(url, "genre")
person = Resource(url, "person")
role = Resource(url, "role")

def test_post_all():
    all_data = json.load(open("all_data.json", "r"))

    for data in all_data["maker_data"]:
        res = maker.post_one(data)
        ppt(res)
        
    for data in all_data["genre_data"]:
        res = genre.post_one(data)
        ppt(res)
    
    for data in all_data["person_data"]:
        res = person.post_one(data)
        ppt(res)

    for data in all_data["movie_data"]:
        res = movie.post_one(data)
        ppt(res)
        
test_post_all()

def test_get_one():
    print("{:=^100}".format("movie"))
    ppt(movie.get_one(1))
    
    print("{:=^100}".format("maker"))
    ppt(maker.get_one(1))
    
    print("{:=^100}".format("genre"))
    ppt(genre.get_one(1))
    
    print("{:=^100}".format("person"))
    ppt(person.get_one(1))
    
    print("{:=^100}".format("role"))
    ppt(role.get_one(1))
    
test_get_one()        
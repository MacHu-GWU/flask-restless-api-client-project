#!/usr/bin/env python
# -*- coding: utf-8 -*-

from faker import Factory
from datetime import datetime, date
import random, string, json

def simple_serialize(data):
    data = dict(data)
    for k, v in data.items():
        if isinstance(v, (datetime, date)):
            data[k] = str(v)
    return data

fake = Factory.create()

# user数据
n_user = 5
user_data = list()
for i in range(n_user):
    data = {
        "id": i + 1,
        "account": fake.company_email(),
        "password": fake.password(),
        "birth_date": fake.date(),
        "create_datetime": fake.date_time(),
    }
    user_data.append(simple_serialize(data))

# tag数据
n_tag = 3
tag_data = list()
for i in range(n_tag):
    data = {"id": i + 1, "name": fake.word()}
    tag_data.append(data)
    
# post数据
n_post = 20
post_data = list()
for i in range(n_post):
    data = {
        "id": i + 1,
        "title": fake.sentence(),
        "body": fake.paragraph(),
        "create_datetime": fake.date_time(),
        "author_id": random.randint(1, 1 + n_user),
        "tags": random.sample(tag_data, random.randint(1, n_tag))
    }
    post_data.append(simple_serialize(data))

if __name__ == "__main__":
    all_data = {
        "user_data": user_data,
        "tag_data": tag_data,
        "post_data": post_data, 
    }
    json.dump(all_data, open("all_data.json", "w"), sort_keys=True,
        indent=4, separators=("," , ": "))
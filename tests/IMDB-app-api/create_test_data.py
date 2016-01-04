#!/usr/bin/env python
# -*- coding: utf-8 -*-

from faker import Factory
from datetime import datetime, date
import random, json

def simple_serialize(data):
    data = dict(data)
    if "_sa_instance_state" in data:
        del data["_sa_instance_state"]

    for k, v in data.items():
        if isinstance(v, (datetime, date)):
            data[k] = str(v)
    return data

def make_fake_data():
    """
    """
    # create fake data
    fake = Factory.create()
    
    # Role data
    role_list = ["Director", "Writer", "Star"]
    role_data = list()
    for i, name in enumerate(role_list):
        role_data.append(simple_serialize({
            "id": i + 1,
            "name": name,
        }))
     
    # Person data
    n_person = 10
    person_data = list()
    person_raw_data = list()
    for i in range(n_person):
        person_data.append(
            simple_serialize({
                "id": i + 1,
                "name": fake.name(),
                "roles": random.sample(role_data, random.randint(1, 2)),
            })
        )
        person_raw_data.append(
            simple_serialize({
                "id": i + 1,
                "name": fake.name(),
            })
        )

    # Split Director, Writer and Star
    director_data, writer_data, star_data = list(), list(), list()
    for person1, person2 in zip(person_data, person_raw_data):
        for role in person1["roles"]:
            if role["id"] == 1:
                director_data.append(person1)
            elif role["id"] == 2:
                writer_data.append(person1)
            elif role["id"] == 3:
                star_data.append(person1)

    # Maker data
    maker_list = ["Disney", "Dreamworks", "MGM", "Columbia"]
    maker_data = list()
    for i, name in enumerate(maker_list):
        maker_data.append(simple_serialize({
            "id": i + 1,
            "name": name,
        }))
     
    # Genre data
    genre_list = ["Action", "Crime", "Drama", "Music", "Sci-Fi", "Thriller"]
    genre_data = list()
    for i, name in enumerate(genre_list):
        genre_data.append(simple_serialize({
            "id": i + 1,
            "name": name,
        }))

    # Movie data
    n_movie = 30
    movie_data = list()
    for i in range(n_movie):
        movie_data.append(simple_serialize({
            "id": i + 1,
            "title": fake.sentence(),
            "maker": random.choice(maker_data),
            "genres": random.sample(genre_data, random.randint(1, 3)),
            "directors": random.sample(director_data, random.randint(1, 2)),
            "writers": random.sample(writer_data, random.randint(1, 3)),
            "stars": random.sample(star_data, random.randint(1, 4)),
        }))
    
    # dump to json
    all_data = {
        "movie_data": movie_data,
        "maker_data": maker_data,
        "genre_data": genre_data,
        "person_data": person_data,
        "director_data": director_data,
        "writer_data": writer_data,
        "star_data": star_data,
        "role_data": role_data,
    }
    json.dump(all_data, open("all_data.json", "w"), sort_keys=True,
        indent=4, separators=("," , ": "))
    
if __name__ == "__main__":
    make_fake_data()
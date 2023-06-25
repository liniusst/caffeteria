# pylint: disable= missing-docstring
from pymongo import MongoClient


def db_session():
    client = MongoClient("localhost", 27017)
    db = client["caffee"]
    return db

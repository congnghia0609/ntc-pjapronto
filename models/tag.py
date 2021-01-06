"""
@author nghiatc
@since 06/01/2021
"""
import bson
from pymongo import DESCENDING

from mdb import mdb


tag_table = mdb.db.tag


class Tag:
    def __init__(self, id, name, create_at, update_at):
        self.id = id
        self.name = name
        self.create_at = create_at
        self.update_at = update_at


def add_tag(tag):
    tag_table.insert_one(tag)
    # tag_id = rs.inserted_id
    # tag['id'] = tag_id
    return tag


def get_tag(oid):
    return tag_table.find_one({"_id": oid})


def update_tag(tag):
    # tag_table.find_one_and_update(tag)
    rs = tag_table.find_one_and_replace({"_id": tag["_id"]}, tag)
    # tag_id = rs.inserted_id
    # tag['id'] = tag_id
    return rs


def total_tags():
    return tag_table.count_documents({})


def get_slide_tags(skip, limit):
    rs = tag_table.find().skip(skip).limit(limit).sort("_id", DESCENDING)
    return rs

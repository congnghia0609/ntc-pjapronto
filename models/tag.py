"""
@author nghiatc
@since 06/01/2021
"""
from mdb import mdb


tag_table = mdb.db.tag


class Tag:
    def __init__(self, id, name, create_at, update_at):
        self.id = id
        self.name = name
        self.create_at = create_at
        self.update_at = update_at


def add_tag(tag):
    rs = tag_table.insert_one(tag)
    # tag_id = rs.inserted_id
    # tag['id'] = tag_id
    return tag



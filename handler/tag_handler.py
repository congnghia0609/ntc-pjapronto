"""
@author nghiatc
@since 06/01/2021
"""
import copy
import datetime
import json
import bson
import models


def add_tag(req):
    params = json.loads(req.body.decode('utf8'))
    name = params["name"]
    if len(name) == 0:
        return req.Response(json={'err': -1, 'msg': 'Parameters invalid'})
    tag = {
        "name": name,
        "created_at": datetime.datetime.utcnow(),
        "updated_at": datetime.datetime.utcnow(),
    }
    # data_resp = copy.deepcopy(tag)
    tag_db = models.add_tag(tag)
    print(tag_db)
    data_resp = {
        "id": str(tag_db['_id']),
        "name": tag_db['name'],
        "updated_at": tag_db['updated_at'].isoformat(),
    }
    print(data_resp)
    return req.Response(json={'err': 0, 'msg': 'Add tag successfully', 'data': data_resp})



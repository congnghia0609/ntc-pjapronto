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


def update_tag(req):
    params = json.loads(req.body.decode('utf8'))
    id = params["id"]
    name = params["name"]
    print(id)
    print(name)
    if len(name) == 0 or len(id) == 0:
        return req.Response(json={'err': -1, 'msg': 'Parameters invalid'})
    try:
        oid = bson.ObjectId(id)
    except:
        return req.Response(json={'err': -1, 'msg': 'TagId invalid'})
    tag_db = models.get_tag(oid)
    print(tag_db)
    if tag_db == None:
        return req.Response(json={'err': -1, 'msg': 'Tag is not exist'})
    tag_db["name"] = name
    tag_db["updated_at"] = datetime.datetime.utcnow()
    rs = models.update_tag(tag_db)
    print(rs)
    data_resp = {
        "id": str(tag_db['_id']),
        "name": tag_db['name'],
        "updated_at": tag_db['updated_at'].isoformat(),
    }
    print(data_resp)
    return req.Response(json={'err': 0, 'msg': 'Update tag successfully', 'data': data_resp})


def get_tag(req):
    id = req.match_dict['id']
    print(id)
    if len(id) == 0:
        return req.Response(json={'err': -1, 'msg': 'Parameters invalid'})
    try:
        oid = bson.ObjectId(id)
    except:
        return req.Response(json={'err': -1, 'msg': 'TagId invalid'})
    tag_db = models.get_tag(oid)
    print(tag_db)
    if tag_db == None:
        return req.Response(json={'err': -1, 'msg': 'Tag is not exist'})
    data_resp = {
        "id": str(tag_db['_id']),
        "name": tag_db['name'],
        "updated_at": tag_db['updated_at'].isoformat(),
    }
    print(data_resp)
    return req.Response(json={'err': 0, 'msg': 'Get tag successfully', 'data': data_resp})


def get_tags(req):
    paging = 2
    page = 1
    is_more = False
    tags = []
    print(req.query)
    # sp = req.query["page"]
    # print("sp:", sp)
    if "page" in req.query:
        page = int(req.query["page"])
    print("page:", page)
    total = models.total_tags()
    if total <= 0:
        data_resp = {
            "page": page,
            "isMore": is_more,
            "tags": tags,
        }
        return req.Response(json={'err': 0, 'msg': 'Get list tags successfully', 'data': data_resp})
    max_page = (total-1)/paging + 1
    if page > max_page:
        data_resp = {
            "page": page,
            "isMore": is_more,
            "tags": tags,
        }
        return req.Response(json={'err': 0, 'msg': 'Get list tags successfully', 'data': data_resp})
    if page < max_page:
        is_more = True
    skip = (page - 1) * paging
    tags_db = models.get_slide_tags(skip, paging)
    for t in tags_db:
        jt = {
            "id": str(t['_id']),
            "name": t['name'],
            "updated_at": t['updated_at'].isoformat(),
        }
        tags.append(jt)
    data_resp = {
        "page": page,
        "isMore": is_more,
        "tags": tags,
    }
    print(data_resp)
    return req.Response(json={'err': 0, 'msg': 'Get list tags successfully', 'data': data_resp})

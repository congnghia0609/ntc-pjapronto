"""
@author nghiatc
@since 06/01/2021
"""
import json


def add_tag(req):
    body = json.loads(req.body.decode('utf8'))
    print("body: ", body)
    print("body['name']: ", body["name"])
    return req.Response(json={'hello': 'world'})



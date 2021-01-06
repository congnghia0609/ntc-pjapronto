"""
@author nghiatc
@since 06/01/2021
"""

import asyncio
from json import JSONDecodeError
from japronto import Application


def hello(request):
    return request.Response(text='Hello world!')


async def asynchronous(req):
    for i in range(1, 4):
        await asyncio.sleep(1)
        print(i, 'seconds elapsed')
    return req.Response(text='3 seconds elapsed')


def params(request):
    return request.Response(text='Request with p1={0} p2={1}!'.format(request.match_dict['p1'], request.match_dict['p2']))


def basic(request):
    text = """Basic request properties:
      Method: {0.method}
      Path: {0.path}
      HTTP version: {0.version}
      Query string: {0.query_string}
      Query: {0.query}""".format(request)

    if request.headers:
        text += "\nHeaders:\n"
        for name, value in request.headers.items():
            text += "      {0}: {1}\n".format(name, value)

    return request.Response(text=text)


def body(request):
    text = """Body related properties:
      Mime type: {0.mime_type}
      Encoding: {0.encoding}
      Body: {0.body}
      Text: {0.text}
      Form parameters: {0.form}
      Files: {0.files}
    """.format(request)

    try:
        json = request.json
    except JSONDecodeError:
        pass
    else:
        text += "\nJSON:\n"
        text += str(json)

    return request.Response(text=text)


def misc(request):
    text = """Miscellaneous:
      Matched route: {0.route}
      Hostname: {0.hostname}
      Port: {0.port}
      Remote address: {0.remote_addr},
      HTTP Keep alive: {0.keep_alive}
      Match parameters: {0.match_dict}
    """.strip().format(request)

    if request.cookies:
        text += "\nCookies:\n"
        for name, value in request.cookies.items():
            text += "      {0}: {1}\n".format(name, value)

    return request.Response(text=text)


if __name__ == '__main__':
    app = Application()

    r = app.router
    # http://localhost:8080/
    r.add_route('/', hello, 'GET')
    # http://localhost:8080/async
    r.add_route("/async", asynchronous, methods=['GET'])
    # http://localhost:8080/params/a/b
    r.add_route('/params/{p1}/{p2}', params, method='GET')
    # http://localhost:8080/basic
    r.add_route('/basic', basic)
    # http://localhost:8080/body
    r.add_route('/body', body)
    # http://localhost:8080/misc
    r.add_route('/misc', misc)

    app.run(port=8080, debug=True)

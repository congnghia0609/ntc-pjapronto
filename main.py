"""
@author nghiatc
@since 06/01/2021
"""

import asyncio
from http.cookies import SimpleCookie
from json import JSONDecodeError
from japronto import Application, RouteNotFoundException
from jinja2 import Template
from handler import tag_handler


def hello(request):
    return request.Response(text='Hello world!')


async def asynchronous(req):
    for i in range(1, 4):
        await asyncio.sleep(1)
        print(i, 'seconds elapsed')
    return req.Response(text='3 seconds elapsed')


# Requests with the path starting with `/params/` segment and followed
# by two additional segments will be directed here.
# Values of the additional segments will be stored in side `request.match_dict`
# dictionary with keys taken from {} placeholders. A request to `/params/1/2`
# would leave `match_dict` set to `{'p1': 1, 'p2': '2'}`.
def params(request):
    return request.Response(text='Request with p1={0} p2={1}!'.format(request.match_dict['p1'], request.match_dict['p2']))


# Request line and headers.
# This represents the part of a request that comes before message body.
# Given a HTTP 1.1 `GET` request to `/basic?a=1` this would yield
# `method` set to `GET`, `path` set to `/basic`, `version` set to `1.1`
# `query_string` set to `a=1` and `query` set to `{'a': '1'}`.
# Additionally if headers are sent they will be present in `request.headers`
# dictionary. The keys are normalized to standard `Camel-Cased` convention.
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


# Message body
# If there is a message body attached to a request (as in a case of `POST`)
# method the following attributes can be used to examine it.
# Given a `POST` request with body set to `b'J\xc3\xa1'`, `Content-Length` header set
# to `3` and `Content-Type` header set to `text/plain; charset=utf-8` this
# would yield `mime_type` set to `'text/plain'`, `encoding` set to `'utf-8'`,
# `body` set to `b'J\xc3\xa1'` and `text` set to `'Já'`.
# `form` and `files` attributes are dictionaries respectively used for HTML forms and
# HTML file uploads. The `json` helper property will try to decode `body` as a
# JSON document and give you resulting Python data type.
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


# Miscellaneous
# `route` will point to an instance of `Route` object representing
# route chosen by router to handle this request. `hostname` and `port`
# represent parsed `Host` header if any. `remote_addr` is the address of
# a client or reverse proxy. If `keep_alive` is true the client requested to
# keep connection open after the response is delivered. `match_dict` contains
# route placeholder values as documented in `2_router.md`. `cookies` contains
# a dictionary of HTTP cookies if any.
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


# json Response: https://github.com/squeaky-pl/japronto/blob/master/tutorial/5_response.md
def json(request):
    return request.Response(json={'hello': 'world'})


def cookies(request):
    cookies = SimpleCookie()
    cookies['hello'] = 'world'
    cookies['hello']['domain'] = 'localhost'
    cookies['hello']['path'] = '/'
    cookies['hello']['max-age'] = 3600
    cookies['city'] = 'São Paulo'
    return request.Response(text='cookies', cookies=cookies)


# This handler raises ZeroDivisionError which doesnt have an error
# handler registered so it will result in 500 Internal Server Error
def unhandled(request):
    1 / 0


# You can also override default 404 handler if you want
def handle_not_found(request, exception):
    return request.Response(code=404, text="Sorry can't find that!")


# A view can read HTML from a file
def home(request):
    with open('views/layout.html') as layout_html:
        return request.Response(text=layout_html.read(), mime_type='text/html')


# A view could also return a rendered jinja2 template
def jinja(request):
    template = Template('<h1>Hello {{ name }}!</h1>')
    return request.Response(text=template.render(name='World'),
                            mime_type='text/html')


# https://github.com/squeaky-pl/japronto
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
    # http://localhost:8080/json
    r.add_route('/json', json)
    # http://localhost:8080/cookies
    r.add_route('/cookies', cookies)
    # http://localhost:8080/unhandled
    r.add_route('/unhandled', unhandled)
    # http://localhost:8080/home
    r.add_route('/home', home)
    # http://localhost:8080/template
    r.add_route('/template', jinja)

    # Tag API
    # http://localhost:8080/tags
    r.add_route('/tag', tag_handler.add_tag, method='POST')
    r.add_route('/tag', tag_handler.update_tag, method='PUT')
    r.add_route('/tag/{id}', tag_handler.get_tag, method='GET')
    r.add_route('/tags', tag_handler.get_tags, method='GET')
    r.add_route('/tag/{id}', tag_handler.delete_tag, method='DELETE')

    # register all the error handlers so they are actually effective
    app.add_error_handler(RouteNotFoundException, handle_not_found)

    app.run(port=8080, debug=True)

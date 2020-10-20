import re
import traceback

"""
For your homework this week, you'll be creating a wsgi application of
your own.

You'll create an online calculator that can perform several operations.

You'll need to support:

  * Addition
  * Subtractions
  * Multiplication
  * Division

Your users should be able to send appropriate requests and get back
proper responses. For example, if I open a browser to your wsgi
application at `http://localhost:8080/multiple/3/5' then the response
body in my browser should be `15`.

Consider the following URL/Response body pairs as tests:

```
  http://localhost:8080/multiply/3/5   => 15
  http://localhost:8080/add/23/42      => 65
  http://localhost:8080/subtract/23/42 => -19
  http://localhost:8080/divide/22/11   => 2
  http://localhost:8080/               => <html>Here's how to use this page...</html>
```

To submit your homework:

  * Fork this repository (Session03).
  * Edit this file to meet the homework requirements.
  * Your script should be runnable using `$ python calculator.py`
  * When the script is running, I should be able to view your
    application in my browser.
  * I should also be able to see a home page (http://localhost:8080/)
    that explains how to perform calculations.
  * Commit and push your changes to your fork.
  * Submit a link to your Session03 fork repository!


"""


def add(*args):
    """ Returns a STRING with the sum of the arguments """

    # TODO: Fill sum with the correct value, based on the
    # args provided.
    sum = 0
    if len(args) > 2:
        args = args[0:2]
    try:
        for num in args:
            sum += int(num)
    except (TypeError, ValueError):
        return "Please use integers"
    return f'The sum of {args[0]} and {args[1]} is {str(sum)}'

# TODO: Add functions for handling more arithmetic operations.

def home():
    welcome = '''
    <h1>How to use this page</h1>
    <body>
    Welcome to the WSGI Calculator!
    <br>
    <p>To use this page, enter '/add', '/subtract', '/multiply', or '/divide' at
     the end of this page's URL, followed by two numbers with slashes between them.
     </p>
    <p>The format 'operand/a/b' will return:</p>
    <ul>
    <li>a + b</li>
    <li>a - b</li>
    <li>a * b</li>
    <li>a / b</li>
    </ul>
    <p>Some examples:</p>
    <ul>
    <li><a href="/add/10/12">localhost:8080/add/10/12</a></li>
    <li><a href="subtract/23/42">localhost:8080/subtract/23/42</a></li>
    <li><a href="multiply/3/5">localhost:8080/multiply/3/5</a></li>
    <li><a href="divide/22/11">localhost:8080/divide/22/11</a></li>
    </ul>
    </body>
    '''
    return welcome


def subtract(*args):
    if len(args) > 2:
        args = args[0:2]
    try:
        difference = int(args[0]) - int(args[1])
    except (TypeError, ValueError):
        return "Please use integers"
    return f'The difference of {args[0]} and {args[1]} is {str(difference)}'

def multiply(*args):
    if len(args) > 2:
        args = args[0:2]
    try:
        product = int(args[0]) * int(args[1])
    except (TypeError, ValueError):
        return "Please use integers"
    return f'The product of {args[0]} and {args[1]} is {str(product)}'

def divide(*args):
    if len(args) > 2:
        args = args[0:2]
    try:
        quotient = int(args[0])/int(args[1])
    except (TypeError, ValueError):
        return "Please use integers"
    except ZeroDivisionError:
        raise ZeroDivisionError
    return f'The quotient of {args[0]} and {args[1]} is {str(quotient)}'

def resolve_path(path):
    """
    Should return two values: a callable and an iterable of
    arguments.
    """
    funcs = {
             '': home,
             'add': add,
             'subtract': subtract,
             'multiply': multiply,
             'divide': divide
             }


    path = path.strip('/').split('/')
    func_name = path[0]
    args = path[1:]

    try:
        func = funcs[func_name]
    except KeyError:
        raise NameError

    return func, args

def application(environ, start_response):
    headers = [('Content-type', 'text/html')]
    try:
        path = environ.get('PATH_INFO', None)
        if path is None:
            raise NameError
        func, args = resolve_path(path)
        body = func(*args)
        status = "200 OK"
    except NameError:
        status = '404 Not Found'
        body = '<h1> Not Found</h1>'
    except ZeroDivisionError:
        status = '400 Bad Request'
        body = '<h1>Zero Division Error: Black hole created</h1>'
    except Exception:
        status = '500 Internal Server Error'
        body = '<h1>Internal Server Error</h1>'
        print(traceback.format_exc())
    finally:
        headers.append(('Content-length', str(len(body))))
    start_response(status, headers)
    return [body.encode('utf8')]

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()

#!/usr/bin/env python3

# Russell Felts
# Exercise 04 Book Server

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

def info(*args):
    """
    Produces a string that describes the site and how to use it
    :param args: unused as nothing is being calculated
    :return: String containing html describing the site
    """
    page = """
        <h1>Calculator</h1>
        <p>This site is a simple calculator that will add, substract, multiply, and divide two numbers.</p>
        <p>Simply enter a url similar to http://localhost:8080/add/23/42 and the answer will be returned.</p>
        <p> The possible paths are /add/#/#, /substract/#/#, /multiply/#/#, /divide/#/#</p>
    """
    return page


def add(*args):
    """
    Adds to ints in a list
    :param args: to numbers to add
    :return: a STRING with the sum of the arguments
    """

    # Convert the args to ints
    temp_list = contert_to_int(*args)
    total = sum(temp_list)

    return str(total)


def subtract(*args):
    """
    Subtract two ints
    :param args: to numbers to subtract
    :return: a STRING with the sum of the arguments
    """

    # Convert the args to ints
    temp_list = contert_to_int(*args)
    total = temp_list[0] - temp_list[1]

    return str(total)

def multiply(*args):
    """
    Multiply two ints
    :param args: to numbers to multiply
    :return: a STRING with the sum of the arguments
    """

    # Convert the args to ints
    temp_list = contert_to_int(*args)
    total = temp_list[0] * temp_list[1]

    return str(total)


def divide(*args):
    """
    Divides two ints
    :param args: to numbers to divide
    :return: a STRING with the sum of the arguments
    """
    temp_list = contert_to_int(*args)

    try:
        total = temp_list[0] / temp_list[1]
    except ZeroDivisionError:
        raise ZeroDivisionError

    return str(total)


def contert_to_int(*args):
    """
    Converts the string args to a list of ints
    :param args: Two strings
    :return: A list of ints
    """
    return [int(arg) for arg in args]


def resolve_path(path):
    """
    Take the request and determine the function to call
    :param path: string representing the requested page
    :return: func - the name of the requested function,
            args - iterable of arguments required for the requested function
    """
    funcs = {
        '': info,
        'add': add,
        'subtract': subtract,
        'multiply': multiply,
        'divide': divide
    }

    # Split the path to determine what the function and arguments
    path = path.strip('/').split('/')

    func_name = path[0]
    args = path[1:]

    # Get the requested function from the dictionary or raise an error
    try:
        func = funcs[func_name]
    except KeyError:
        raise NameError

    return func, args


def application(environ, start_response):
    """
    Handle incoming requests and route them to the appropriate function
    :param environ: dictionary that contains all of the variables from the WSGI server's environment
    :param start_response: the start response method
    :return: the response body
    """
    headers = [('Content-type', 'text/html')]
    try:
        path = environ.get('PATH_INFO', None)

        if path is None:
            raise NameError

        func, args = resolve_path(path)
        body = func(*args)
        status = "200 OK"

    except NameError:
        status = "404 Not Found"
        body = "<h1>Not Found</h1>"
    except ZeroDivisionError:
        status = "400 Bad Request"
        body = "<h1>Bad Request</h1>"
    except Exception:
        status = "500 Internal Server Error"
        body = "<h1>Internal Server Error</h1>"
        print(traceback.format_exc())
    finally:
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)

    return [body.encode('utf8')]


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()

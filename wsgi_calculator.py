#!/usr/bin/env python

'''
http://localhost:8080/multiply/3/5  => 15
http://localhost:8080/add/23/42     => 65
http://localhost:8080/divide/6/0    => HTTP "400 Bad Request"
'''
page = """<html>
<head>
<title>WSGI Calulator!</title>
</head>
<body>
<h1>Welcome to the WSGI Calculator!</h1>
<p>Please type in a url like localhost:8080/functionname/operand/operand</p>
It supports addition, subtraction, multiplication, and division
<p>See the examples below:</p>
<hr>
<a href="http://localhost:8080/add/13/7">/add/13/7</a>
<p><a href="http://localhost:8080/add/23/-42">/add/23/-42</a></p>
<p><a href="http://localhost:8080/subtract/126/21">/subtract/126/21</a></p>
<p><a href="http://localhost:8080/subtract/43/-780">/subtract/43/-780</a></p>
<p><a href="http://localhost:8080/multiply/23/0">/multiply/23/0</a></p>
<p><a href="http://localhost:8080/multiply/54/65">/multiply/54/65</a></p>
<p><a href="http://localhost:8080/divide/60/15">/divide/60/15</a></p>
<p><a href="http://localhost:8080/divide/16/0">/divide/16/0</a></p>
<br>
<h1>Current Answer: {result}</h1>
</body>
</html>"""

def add(*args):
    return str(int(args[0]) + int(args[1]))

def subtract(*args):
    return str(int(args[0]) - int(args[1]))

def multiply(*args):
    return str(int(args[0]) * int(args[1]))

def divide(*args):
    return str(int(args[0]) / int(args[1]))

def resolve_path(path):
    args = path.strip("/").split("/")

    func_name = args.pop(0)

    func = {
	   "add" : add,
       "subtract" : subtract,
       "multiply" : multiply,
       "divide" : divide
       }.get(func_name)

    return func, args

def application(environ, start_response):
    headers = [('Content-type', 'text/html')]
    try:
        path = environ.get('PATH_INFO', None)
        if path is None:
            raise NameError
        func, args = resolve_path(path)
        result = func(*args)
        status = "200 OK"
    except NameError:
        status = "404 Not Found"
        result = "Not Found"
    except ZeroDivisionError:
        status = "400 Bad Request"
        result = "Only Chuck Norris can divide by zero"
    except Exception:
        status = "500 Internal Server Error"
        result = "There is a problem with your url or some other error"
    finally:
        body = page.format(result=result)
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)
        return [body.encode('utf8')]

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()

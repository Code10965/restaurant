#!/usr/bin/env python3

# A small website which reads from a database and renders html based on user input
# Uses sqlite3 and wsgi to get the job done. 

# Use the out of the box reference implementation of WSGI from python
from wsgiref.simple_server import make_server

# import function which connects to the database and returns a list of restaurants
from database_connect import get_restaurants

#useful for parsing the post request from wsgi 
from urllib import parse

## first view: ask for the neighborhood. 
# this is static HTML, which containts a form. 
def index():
    html = """
    <html>
    <head>
    <title>A super simple python WSGI server</title>
    </head>
    <body>

    <p>
    This is a simple Python WSGI server. This html generated from a function. 
    </p>
    <form action="" method="post">
    <p>
    <label for="neighborhood">Your Neighborhood: </label>
    <input type="text" id="neighborhood" name="neighborhood">
    <input type="submit" value="Send">
    </p>
    </form>
    </body>
    </html>
    """

    return [html.encode("utf-8")]

## second view: display restaurants in the neighborhood
# this is dynamic HMTL which is rendered server-side.
def restaurants_list(restaurants):

    elements_html = ""

    # generate HTML list elements from the 
    for restaurant in restaurants:
        elements_html += "<li>" + restaurant[1] + "</li>"

    html = """
    <html>
    <head>
    <title>A database response</title>
    </head>
    <body>
    <p>
    My favorite restaurants in your neighborhood:
    </p>
    <ul>
    {elements_placeholder}
    </ul>
    </form>
    </body>
    </html>
    """.format(elements_placeholder=elements_html)
    return [html.encode("utf-8")]

## Render an error for any other paths requested.
# display the path requested to the user. 
def path_error(requsted_path):

    html = """
    <html>
    <head>
    <title>my very first error page </title>
    </head>
    <body>
    <h2>
    You asked for page {path_placeholder}, but we haven't built that yet. 
    </h2>
    </form>
    </body>
    </html>
    """.format(path_placeholder=requsted_path)
    return [html.encode("utf-8")]

## The main application.
#  this will be called on every get request. 
def neighborhood_restaurants(environ, start_response):

    # set status and HTTP header for response, both needed.
    # these will be send with the resposne body, below.
    status = '200 OK'
    headers = [('Content-type', 'text/html; charset=utf-8')]

    # send the response, once there is a body. 
    start_response(status, headers)

    ## get information from the client request, in order to decide how to respond

    # get the method, e.g. GET, POST.
    request_method = environ.get('REQUEST_METHOD')
    
    # get the path, e.g. index.html or /hello 
    request_path = environ.get('PATH_INFO')

    # render index() for a GET request at the root 
    if request_method == 'GET' and request_path == "/":
        return index()

    # render restaurants_list for a POST request at the root 
    elif request_method == 'POST' and request_path == "/":
        
        ## Parse user input from form, pass it to restaurants_list()

        # get the size of the post request sent, to know how much to read. 
        request_body_size = int(environ.get('CONTENT_LENGTH'))
        
        # read the post request from the environment 
        request_body_raw = environ['wsgi.input'].read(request_body_size)

        # use the built-in parse function to get an (encoded) dictionary
        request_body_dict = parse.parse_qs(request_body_raw)

        # using the key defined in the form, get the value which has been sent by the user. 
        value = request_body_dict['neighborhood'.encode()]

        # finally, define a variable which has the neighborhood name in plaintext. 
        neighborhood = value[0].decode()

        ## pass user input to function which queries the database
        # and returns a list of tuples of restuarants.
        restaurants = get_restaurants(neighborhood)

        ## pass list of restaurants to function which generates the HMTL 
        # and return it, i.e. send it back to the client.        
        return restaurants_list(restaurants)

    # render an error another page is requested. 
    else: 
        return path_error(request_path)

## make the file directly execeutable. 


if __name__ == '__main__':
    
    print("Staring restaurants website server.")

    PORT = 8000
    ADDRESS = 'localhost'

    # define server daemon, which takes the main application function define above as an argument.
    httpd = make_server(ADDRESS, PORT, neighborhood_restaurants)
    print("WSGI Server running on port http://{address_placeholder}:{port_placeholder}".format(address_placeholder=ADDRESS, port_placeholder=PORT))

    # server
    httpd.serve_forever()

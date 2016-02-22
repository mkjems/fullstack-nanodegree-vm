from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
import re

from restaurant_views import restaurants_list_view, restaurant_create_view
from restaurant_views import restaurant_update_view, restaurant_delete_view

from restaurant_models import restaurants_list_model, restaurant_create_model, restaurant_model
from restaurant_models import restaurant_update_model, restaurant_delete


class webserverHandler (BaseHTTPRequestHandler):

    def do_GET(self):
        print 'PATH GET: %s' % self.path
        try:
            if self.path.endswith("/restaurants"):

                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                model = restaurants_list_model()
                output = restaurants_list_view(model)

                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/restaurant/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = restaurant_create_view()

                self.wfile.write(output)
                print output
                return

            regex = re.compile('^/restaurant/edit/(\d+)')
            match = regex.match(self.path)
            if match is not None:
                restaurant_id = match.group(1)
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                model = restaurant_model(restaurant_id)
                output = restaurant_update_view(model)

                self.wfile.write(output)
                print output
                return

            regex2 = re.compile('^/restaurant/delete/(\d+)')
            match2 = regex2.match(self.path)
            if match2 is not None:
                print 'Match'
                restaurant_id = match2.group(1)
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                model = restaurant_model(restaurant_id)
                output = restaurant_delete_view(model)

                self.wfile.write(output)
                print output
                return

            raise ValueError('No handler for {0}'.format(self.path))

        except IOError:
            self.send_error(404, "File Not Found %s" % self.path)

    def do_POST(self):
        print 'PATH POST: %s' % self.path
        try:
            if self.path.endswith("/restaurant/new"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    name = fields.get('restaurant_name')[0]

                restaurant_create_model(name)
                print "Name: %s " % name
                self.send_response(301)
                self.send_header("Location", "http://localhost:8000/restaurants")
                return

            if self.path.endswith("/restaurant/update"):
                print 'we have a match'
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    name = fields.get('restaurant_name')[0]
                    restaurant_id = fields.get('restaurant_id')[0]

                restaurant_update_model(restaurant_id, name)
                print "Name: %s " % name
                print "Id: %s " % restaurant_id
                self.send_response(301)
                self.send_header("Location", "http://localhost:8000/restaurants")
                return

            if self.path.endswith('/restaurant/delete'):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    restaurant_id = fields.get('restaurant_id')[0]

                restaurant_delete(restaurant_id)
                print "Deleted Restaurant with id: %s" % restaurant_id
                self.send_response(301)
                self.send_header("Location", "http://localhost:8000/restaurants")
                return

            raise ValueError('No handler for {0}'.format(self.path))

        except:
            pass


def main():
    try:
        port = 8000
        server = HTTPServer(('', port), webserverHandler)
        print "Server is running on port {0}".format(port)
        server.serve_forever()

    except KeyboardInterrupt:
        print "^C Detected... Stoping web server"
        server.socket.close()

if __name__ == '__main__':
    main()

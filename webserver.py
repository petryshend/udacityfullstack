from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from database_setup import *
import cgi



class webServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Hello!</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/hola"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>&#161 Hola !</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/restaurants"):
                restaurants = session.query(Restaurant).all()
                output = "<ol>"
                for res in restaurants:
                    output += "<li>" + res.name + "</li>"
                    output += "<a href=\"" + str(res.id) + "/edit/\">Edit</a>"
                    output += " | <a href=\"" + str(res.id) + "/delete/\">Delete</a>"
                output += "</ol>"
                self.renderPage(output)
                return

            if self.path.endswith("/create"):
                output = "<h1>Create new restaurant</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/create'><h2>Name?</h2><input name="name" type="text" ><input type="submit" value="Submit"> </form>'''
                self.renderPage(output)
                return

            if self.path.endswith("/edit"):
                print 'hhh'
                rest_id = self.path.split("/")[1]
                print rest_id
                rest = session.query(Restaurant).filter_by(id=rest_id).first()
                output = "<h1>Edit restaurant name</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/edit'><input name="name" type="text" value="%s"><input type="submit" value="Submit"> </form>''' % rest.name
                self.renderPage(output)
                return



        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        try:
            if self.path.endswith("/create"):
                ctype, pdict = cgi.parse_header(self.headers.getheader("content-type"))
            if ctype == "multipart/form-data":
                fields = cgi.parse_multipart(self.rfile, pdict)
            messagecontent = fields.get("name")
            newRestaurant = Restaurant(messagecontent[0])
            session.add(newRestaurant)
            session.commit()

            self.redirect('/restaurants')


        except:
            pass

    def renderPage(self, body):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        output = "<html><body>%s</body></html>" % body
        self.wfile.write(output)

    def redirect(self, path):
        self.send_response(301)
        self.send_header("Content-type", "text/html")
        self.send_header("Location", path)
        self.end_headers()



def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webServerHandler)
        print "Web Server running on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print " ^C entered, stopping web server...."
        server.socket.close()

if __name__ == '__main__':
    main()
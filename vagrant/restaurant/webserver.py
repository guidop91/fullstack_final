from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

## Database imports
from database import Base, Restaurant, MenuItem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

## Create session and connect to database
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

class webserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/restaurant"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                restaurants = session.query(Restaurant).all()

                output = ""
                output += "<html><body>"
                output += "<h3><a href='/restaurant/new'>Make a new Restaurant</a></h3>"
                for r in restaurants:
                    output += '<p>%s</p>' % r.name
                    output += '<p><a href="/restaurant/%s/edit">Edit</a></p>' % r._id
                    output += '<p><a href="/restaurant/%s/delete">Delete</a></p><br>' % r._id
                output += "</body></html>"
                
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/restaurant/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += '''<form method='POST' enctype='multipart/form-data' 
                action='/restaurant/new' ><h2>New Restaurant</h2><input name="res-name" 
                type="text" ><input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/edit"):
                #Get the ID and make the query
                rest_id = self.path.split('/')[2]
                rest_query = session.query(Restaurant).filter_by(_id=rest_id).one()

                if rest_query:
                    self.send_response(200)
                    self.send_header('Content-type','text/html')
                    self.end_headers()

                    #HTML for this page
                    output = '<html><body>'
                    output += '<h1>' + rest_query.name + '</h1>'
                    output += '''
                        <form method='POST' enctype='multipart/form-data' action='/restaurant/%s/edit'>
                            <input name='newName' type='text'>
                            <input type='submit' value='Change'>
                        </form></body></html>
                    ''' % rest_query._id

                    self.wfile.write(output)

            if self.path.endswith("/delete"):
                #Get the ID and make the query
                rest_id = self.path.split('/')[2]
                rest_query = session.query(Restaurant).filter_by(_id=rest_id).one()

                if rest_query:
                    self.send_response(200)
                    self.send_header('Content-type','text/html')
                    self.end_headers()

                    #HTML for this page
                    output = '<html><body>'
                    output += '<h1>Are you sure you want to delete ' + rest_query.name + '?</h1><br>'
                    output += '''
                        <form method='POST' enctype='multipart/form-data' action='/restaurant/%s/delete'>
                            <input type='submit' value='DELETE'>
                        </form></body></html>
                    ''' % rest_query._id

                    self.wfile.write(output)
                
            

        except IOError:
            self.send_error(404,"File not found %s" % self.path)

    def do_POST(self):
        try:
            if self.path.endswith('/restaurant/new'):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    res_name = fields.get('res-name')

                    #Database work
                    new_rest = Restaurant(name=res_name[0])
                    session.add(new_rest)
                    session.commit()

                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location','/restaurant')
                    self.end_headers()

            if self.path.endswith('/edit'):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    res_name = fields.get('newName')
                    res_id = self.path.split('/')[2]

                    #Database work
                    chosen_rest = session.query(Restaurant).filter_by(_id=res_id).one()
                    if chosen_rest:
                        chosen_rest.name = res_name[0]
                        session.add(chosen_rest)
                        session.commit()

                        self.send_response(301)
                        self.send_header('Content-type', 'text/html')
                        self.send_header('Location','/restaurant')
                        self.end_headers()

            if self.path.endswith('/delete'):
               
                res_id = self.path.split('/')[2]

                #Database work
                chosen_rest = session.query(Restaurant).filter_by(_id=res_id).one()
                if chosen_rest:
                    session.delete(chosen_rest)
                    session.commit()
                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location','/restaurant')
                    self.end_headers()
        except:
            pass

def main():
    try:
        port = 8080
        server = HTTPServer(('',port),webserverHandler)
        print "Web Server running on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print "^C entered, stopping web server..."
        server.socket.close()


if __name__ =='__main__':
    main()
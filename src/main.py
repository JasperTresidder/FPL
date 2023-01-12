from web.web import MyServer
from http.server import BaseHTTPRequestHandler, HTTPServer
hostName = "localhost"
serverPort = 85
webServer = HTTPServer((hostName, serverPort), MyServer)
MyServer.load(6574078)
print("Server started http://%s:%s" % (hostName, serverPort))
webServer.serve_forever()
print("Server stopped.")



import time
import services

def application(environ, start_response):
    time.sleep(10)
    status = '200 OK'
    output = 'Hello World!'
    response_headers = [('Content-type', 'text/plain'), ('Content-Length', str(len(output)))]
    start_response(status, response_headers)
    return [output]



from Weather import Station
import os

def wsgi(environ, response):
    response('200 OK', [('Content-type','text/html')])
    return Station(environ['QUERY_STRING']).html()

def cgi(station=None):
    if not station:
        try: station = os.environ['QUERY_STRING']
        except KeyError: station = 'KMTN'
    print 'Content-type: text/html'
    print
    for out in Station(station).html():
        print out

if __name__ == '__main__':
    cgi()

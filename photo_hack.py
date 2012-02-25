import sys, json
from pprint import pprint
from bottle import route, run, request, response
sys.path.append('/home/david/photo-hack')
import backend_stuff

@route('/', method='POST')
def index():
    data = request.files.data
    if name and data and data.file:
        raw = data.file.read() # This is dangerous for big files
        filename = data.filename
        return "Hello %s! You uploaded %s (%d bytes)." % (name, filename, len(raw))

    response.content_type = 'application/json'
    venues = backend_stuff.main()
    venues_json = json.dumps(venues)
    return venues_json

@route('/hello')
def hello():
    return "Hello World!"


import sys, json
from pprint import pprint
from bottle import route, run, request, response
sys.path.append('/home/david/photo-hack')
import backend_stuff

@route('/', method='POST')
def index():
    data = request.files.data
    if data and data.file:
        raw = data.file.read() # This is dangerous for big files
        filename = data.filename
        
        # decode data using base64 codec, write to a file
        fh = open('imageToSave.jpg', 'wb')
        #fh.write(raw.decode('base64'))
        fh.write(raw)
        fh.close()

        return "Hello You uploaded %s (%d bytes)." % (filename, len(raw))

    response.content_type = 'application/json'
    venues = backend_stuff.main()
    venues_json = json.dumps(venues)
    return venues_json

@route('/hello')
def hello():
    return "Hello World!"


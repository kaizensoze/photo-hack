import sys, json, time
from pprint import pprint
from bottle import route, run, request, response, static_file, error
sys.path.append('/home/david/photo-hack')
import backend_stuff

@route('/', method='POST')
def index():
    image = request.POST.get('image')
    lat = request.POST.get('lat')
    lng = request.POST.get('lng')
    filename = 'u' + str(int(time.time())) + '.jpeg'

    if image:
        fh = open('uploaded_images/' + filename, 'wb')
        fh.write(image.decode('base64'))
        fh.close()

    response.content_type = 'application/json'
    return {'image_url': 'http://dev.ragemyface.com/uploaded_images/' + filename, 'venue_id': '123'}


@route('/hello')
def hello():
    response.content_type = 'application/json'
    return {'image_url': 'http://dev.ragemyface.com/uploaded_images/', 'venue_id': 123}

@route('/uploaded_images/<filename>')
def send_image(filename):
    return static_file(filename, root='/home/david/photo-hack/uploaded_images')

@error(404)
def error404(error):
    return 'Nothing here, sorry'

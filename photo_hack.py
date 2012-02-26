import sys, json, time
from pprint import pprint
from bottle import route, run, request, response, static_file, error
sys.path.append('/home/david/photo-hack')
import backend_stuff


UPLOADED_IMAGES_PATH = '/home/david/photo-hack/uploaded_images'
COMPARE_IMAGES_PATH = '/home/david/photo-hack/compare_images'
BASE_URL = 'http://dev.ragemyface.com/'

@route('/', method='POST')
def index():
    image = request.POST.get('image')
    filename = request.POST.get('filename')
    lat = request.POST.get('lat')
    lng = request.POST.get('lng')
    if not filename:
        filename = 'u' + str(int(time.time())) + '.jpeg'

    if image:
        fh = open('uploaded_images/' + filename, 'wb')
        fh.write(image.decode('base64'))
        fh.close()

    response.content_type = 'application/json'
    return {'image_url': BASE_URL + filename, 'venue_id': '123'}


@route('/uploaded_images/<filename>')
def send_image(filename):
    return static_file(filename, root=UPLOADED_IMAGES_PATH)


@route('/compare_images/<filename>')
def compare_images(filename):
    return static_file(filename, root=COMPARE_IMAGES_PATH)


@error(404)
def error404(error):
    return 'Nothing here, sorry'


import json
import sys
import threading
import time

from pprint import pprint

from bottle import route, run, request, response, static_file, error
import backend

sys.path.append('/home/david/photo-hack')


UPLOADED_IMAGES_PATH = '/home/david/photo-hack/uploaded_images'
COMPARE_IMAGES_PATH = '/home/david/photo-hack/compare_images'
BASE_URL = 'http://dev.ragemyface.com/'


@route('/upload', method='POST')
def upload():
    # upload params
    image = request.POST.get('image')
    #filename = request.POST.get('filename')
    lat = request.POST.get('lat')
    lng = request.POST.get('lng')

    gps_loc = (lat, lng)

    # generate filename to save image to disk
    if not filename:
        filename = 'u' + str(int(time.time())) + '.jpeg'

    # save image to disk
    if image:
        fh = open('uploaded_images/' + filename, 'wb')
        fh.write(image.decode('base64'))
        fh.close()

    match_result = backend.getMatch(filename, gps_loc)
    match_result["filepath"] = filename

    response.content_type = 'application/json'
    return json.dumps(match_result)


@route('/send_postcard')
def send_postcard():
    image_url = request.GET.get('image_url')
    venue_name = request.GET.get('venue_name')

    threading.Timer(0, backend.sendPostCard, [image_url, venue_name]).start()

    return image_url


@route('/piictu')
def add_image_to_feed():
    image_url = request.GET.get('image_url')
    category = request.GET.get('category')


@route('/uploaded_images/<filename>')
def send_image(filename):
    return static_file(filename, root=UPLOADED_IMAGES_PATH)


@route('/compare_images/<filename>')
def compare_images(filename):
    return static_file(filename, root=COMPARE_IMAGES_PATH)


@error(404)
def error404(error):
    return 'Nothing here, sorry'

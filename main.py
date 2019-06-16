from bottle import post, get, run, static_file, default_app
from capturing import Capturing
from autopilot import Autopilot

config = {
    'photos_directory': 'photos',
    'port': 3001
}

capturing = Capturing(config['photos_directory'])
autopilot = Autopilot()


@get('/')
@get('/index.html')
def index_html():
    return static('index.html', 'text/html')


@get('/<file_path:re:js/.*>')
def js(file_path):
    return static(file_path, 'application/javascript')


@get('/<file_path:re:css/.*>')
def css(file_path):
    return static(file_path, 'text/css')


# obsolete
@get('/photos-count')
def photos_count():
    return str(capturing.get_photos_max_index())


@get('/status')
def status():
    return {
        'photosCount': capturing.get_photos_max_index(),
        'isCapturing': capturing.is_capturing,
        'isAutopiloting': autopilot.is_running,
        'latency': autopilot.vision.latency,
        'objects': [visible_object.to_serializable() for visible_object in autopilot.vision.latest_objects]
    }
    #return '{{ photosCount:{0}, isCapturing:{1}, isAutopiloting:{2}, latency:{3} }}'.format(
    #    capturing.get_photos_max_index(),
    #    capturing.is_capturing,
    #    autopilot.is_running,
    #    autopilot.vision.latency,
    #)


@get('/photos/<index>')
def photo(index):
    cache = None
    if index == 'last':
        index = capturing.get_photos_max_index()
        cache = 'no-store'
    response = static(capturing.get_photo_path('%04d' % int(index)), 'image/jpg')
    if cache is not None:
        response.set_header('Cache-Control', cache)
    return response


def static(path, type):
    return static_file(path,
                       root='.',
                       mimetype=type)


@post('/start-capture')
def start_capture():
    capturing.start()


@post('/stop-capture')
def stop_capture():
    capturing.stop()


@post('/start-autopilot')
def start_autopilot():
    autopilot.start()


@post('/stop-autopilot')
def stop_autopilot():
    autopilot.stop()


if __name__ == '__main__':
    run(host='0.0.0.0', port=config['port'])
else:
    app = application = default_app()



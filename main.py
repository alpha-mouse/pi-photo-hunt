import os, glob, re
from picamera import PiCamera
from threading import Thread, Lock
from bottle import post, get, run, static_file, default_app

config = {
    'photos_directory': 'photos',
    'port': 3001
}

thread = None
interrupt_capture = False
lock = Lock()


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


@get('/photos-count')
def photos_count():
    return str(get_photos_max_index())


@get('/photos/<index>')
def photo(index):
    if index == 'last':
        index = get_photos_max_index()
    return static(get_photo_path(index), 'image/jpg')


def static(path, type):
    return static_file(path,
                       root='.',
                       mimetype=type)


@post('/start-capture')
def start_capture():
    global thread
    if thread is None:
        with lock:
            if thread is None:
                thread = Thread(target=capture)
                thread.start()


@post('/stop-capture')
def stop_capture():
    global thread, interrupt_capture
    if thread is not None:
        with lock:
            if thread is not None:
                interrupt_capture = True
                thread.join()
                interrupt_capture = False
                thread = None


def capture():
    photo_index = get_photos_max_index() + 1
    # The fecking camera better be initialized here, in this thread.
    # Because when running this under uwsgi I've pulled my hair out
    # trying to understand why no photos are taken
    camera = PiCamera()
    camera.resolution = (1296, 972)
    while not interrupt_capture:
        camera.capture(get_photo_path(photo_index))
        photo_index += 1
    camera.close()


def get_photos_max_index():
    p = re.compile(get_photo_path('(\d+)'), re.IGNORECASE)
    existing_indices = [int(p.match(_).group(1)) for _ in glob.glob(get_photo_path('*'))]
    if len(existing_indices) == 0:
        return 0
    return max(existing_indices)


def get_photo_path(index):
    return os.path.join(config['photos_directory'], 'duck_' + str(index) + '.jpg')


if __name__ == '__main__':
    if not os.path.exists(config['photos_directory']):
        os.makedirs(config['photos_directory'], exist_ok=True)
    run(host='0.0.0.0', port=config['port'])
else:
    app = application = default_app()



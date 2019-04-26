import os, glob, re
from picamera import PiCamera
from threading import Thread, Lock


class Capturing:
    def __init__(self, photos_directory):
        if not os.path.exists(photos_directory):
            os.makedirs(photos_directory, exist_ok=True)

        self.photos_directory = photos_directory
        self.thread = None
        self.interrupt_capture = False
        self.lock = Lock()

    def start_capture(self):
        if self.thread is None:
            with self.lock:
                if self.thread is None:
                    self.thread = Thread(target=self.capture)
                    self.thread.start()

    def stop_capture(self):
        if self.thread is not None:
            with self.lock:
                if self.thread is not None:
                    self.interrupt_capture = True
                    self.thread.join()
                    self.interrupt_capture = False
                    self.thread = None

    def get_photos_max_index(self):
        p = re.compile(self.get_photo_path('(\d+)'), re.IGNORECASE)
        existing_indices = [int(p.match(_).group(1)) for _ in glob.glob(self.get_photo_path('*'))]
        if len(existing_indices) == 0:
            return 0
        return max(existing_indices)

    def get_photo_path(self, index):
        return os.path.join(self.photos_directory, 'duck_' + str(index) + '.jpg')

    def capture(self):
        photo_index = self.get_photos_max_index() + 1
        # The fecking camera better be initialized here, in this thread.
        # Because when running this under uwsgi I've pulled my hair out
        # trying to understand why no photos are taken
        camera = PiCamera()
        # camera.resolution = (1296, 972)
        camera.iso = 1600
        while not self.interrupt_capture:
            camera.capture(self.get_photo_path('%04d' % photo_index))
            photo_index += 1
        camera.close()

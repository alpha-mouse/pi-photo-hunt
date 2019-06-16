import os
import numpy as np
import tensorflow as tf
from threading import Thread, Lock
from picamera import PiCamera
from time import time

checkpoint = os.path.join(os.getcwd(), 'inference_graph.pb')

class Vision:
    def __init__(self, update_callback):
        self.update_callback = update_callback

        self.thread = None
        self.interrupt_observation = False
        self.lock = Lock()

        self.latest_objects = []
        self.latency = 0

        detection_graph = tf.Graph()
        with detection_graph.as_default():
            od_graph_def = tf.GraphDef()
            with tf.gfile.GFile(checkpoint, 'rb') as fid:
                serialized_graph = fid.read()
                od_graph_def.ParseFromString(serialized_graph)
                tf.import_graph_def(od_graph_def, name='')

            self.session = tf.Session(graph=detection_graph)
            self.image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
            self.detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
            self.detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
            self.detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')

    def start(self):
        if self.thread is None:
            with self.lock:
                if self.thread is None:
                    self.latest_objects = []
                    self.thread = Thread(target=self.observe)
                    self.thread.start()

    def stop(self):
        if self.thread is not None:
            with self.lock:
                if self.thread is not None:
                    self.interrupt_observation = True
                    self.thread.join()
                    self.interrupt_observation = False
                    self.thread = None

    @property
    def is_observing(self):
        return self.thread is not None

    def observe(self):
        camera = PiCamera()
        camera.resolution = (640, 480)
        camera.iso = 1600

        image = np.empty((camera.resolution[1], camera.resolution[0], 3), dtype=np.uint8)
        while not self.interrupt_observation:
            s = time()
            camera.capture(image, 'rgb')
            image_expanded = np.expand_dims(image, axis=0)
            (boxes, scores, classes) = self.session.run(
                [self.detection_boxes, self.detection_scores, self.detection_classes],
                feed_dict={self.image_tensor: image_expanded})

            self.latency = time() - s
            self.latest_objects = [VisibleObject(box, scores[0][i], classes[0][i]) for i, box in enumerate(boxes[0])]
            self.update_callback(self.latest_objects)

        camera.close()


class VisibleObject:
    def __init__(self, box, probability, category):
        self.box = box
        self.probability = probability
        self.category = category

    def to_serializable(self):
        return {
            'box': [float(x) for x in self.box],
            'probability': float(self.probability),
            'category': int(self.category),
        }

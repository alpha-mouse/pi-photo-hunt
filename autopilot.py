from vision import Vision
from motion import Motion


class Autopilot:
    def __init__(self):
        self.vision = Vision(self._on_new_capture)
        self.motion = Motion()

    def start(self):
        self.motion.set_values(0,0)
        self.motion.enable()
        self.vision.start()

    def stop(self):
        self.motion.disable()
        self.vision.stop()

    @property
    def is_running(self):
        return self.vision.is_observing

    def _on_new_capture(self, objects):
        # Speed equals the probability of the most probable object detected.
        # That is, if confident - move fast
        speed = objects[0].probability

        total_weight = 0
        direction_weight = 0
        for i in range(0, len(objects)):
            obj = objects[i]
            # box size times probability
            weight = (obj.box[2] - obj.box[0]) * (obj.box[3] - obj.box[1]) * obj.probability
            # if it's not a duck - discount heavily
            if obj.category != 1:
                weight /= 10
            total_weight += weight
            # box_mid_point = (obj.box[3] + obj.box[1]) / 2
            # translate [0,1] into [-1,1]
            # direction = box_mid_point * 2 - 1
            direction = (obj.box[3] + obj.box[1]) - 1
            direction_weight += direction * weight

        direction = direction_weight / total_weight

        self.motion.set_values(speed, direction)

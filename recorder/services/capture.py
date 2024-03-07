import os
import time
from threading import Thread, Lock
from collections import deque

from cv2 import VideoCapture, CAP_PROP_POS_FRAMES, imwrite


# https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_gui/py_video_display/py_video_display.html
# https://docs.python.org/3/library/threading.html


class MockCapture:
    def __init__(self, source, fps, histsize):
        self.source = source
        self.__wait = 1 / fps
        self.__frames = deque(maxlen=histsize)
        self.__lock = Lock()
        self.__stop = False

    def start(self):
        Thread(target=self.__worker).start()

    def stop(self):
        self.__stop = True

    def save(self, target):
        with self.__lock:
            for i, frame in enumerate(self.__frames):
                imwrite(os.path.join(target, 'frame-{nr}.png'.format(nr=i + 1)), frame)

    def __worker(self):
        stream = VideoCapture(self.source)
        try:
            while stream.isOpened() and not self.__stop:
                start = time.time()
                ok, frame = stream.read()
                if ok:
                    with self.__lock:
                        self.__frames.append(frame)
                    # roughly match video timing
                    dur = time.time() - start
                    wait = self.__wait - dur
                    if wait > 0:
                        time.sleep(wait)
                else:
                    # rewind
                    stream.set(CAP_PROP_POS_FRAMES, 0)
        finally:
            stream.release()

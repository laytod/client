import time
import io
import threading
import picamera
import subprocess


class Camera(object):
    thread = None  # background thread that reads frames from camera
    frame = None  # current frame is stored here by background thread
    last_access = 0  # time of last client access to the camera

    def initialize(self):
        if Camera.thread is None:
            # start background frame thread
            Camera.thread = threading.Thread(target=self._thread)
            Camera.thread.start()

            # wait until frames start to be available
            while self.frame is None:
                time.sleep(0)

    def get_frame(self):
        Camera.last_access = time.time()
        self.initialize()
        return self.frame

    @classmethod
    def _thread(cls):
        with picamera.PiCamera() as camera:
            # camera setup
            camera.resolution = (320, 240)
            camera.hflip = True
            camera.vflip = True

            # let camera warm up
            camera.start_preview()
            print 'warming up...'
            time.sleep(2)

            path = '/run/shm/'

            # command to add timestamp banner onto pictures
            cmd = """convert -pointsize 20 -fill '#0008' -draw "rectangle 0,450 720,480" -fill white -draw "text 430,470 '$(date)'" {path}tmp.jpg {path}image.jpg""".format(path=path)

            # 10 seconds after the last call to get_frame, disable the camera.
            # While the camera is enabled, take 1 picture per second.
            while time.time() - cls.last_access < 10:
                camera.capture('{path}/tmp.jpg'.format(path=path))
                subprocess.call(cmd, shell=True)

                # save timestamped frame to the class
                with open('{path}/image.jpg'.format(path=path), 'rb') as img:
                    cls.frame = io.BytesIO(img.read())

                time.sleep(1)
                pass

        cls.thread = None

    # @classmethod
    # def _thread(cls):
    #     with picamera.PiCamera() as camera:
    #         # camera setup
    #         camera.resolution = (320, 240)
    #         camera.hflip = True
    #         camera.vflip = True

    #         # let camera warm up
    #         camera.start_preview()
    #         print 'warming up...'
    #         time.sleep(2)

    #         print 'starting stream.'
    #         stream = io.BytesIO()
    #         for _ in camera.capture_continuous(stream, 'jpeg', use_video_port=True):
    #             # store frame
    #             stream.seek(0)
    #             print 'saving frame'
    #             cls.frame = stream.read()

    #             # reset stream for next frame
    #             stream.seek(0)
    #             stream.truncate()

    #             time.sleep(4)

    #             # if there hasn't been any clients asking for frames in
    #             # the last 10 seconds stop the thread
    #             if time.time() - cls.last_access > 10:
    #                 break
    #     cls.thread = None

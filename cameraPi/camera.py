import time
import logging
import picamera
import subprocess
from io import BytesIO
from threading import Thread, Lock


logger = logging.getLogger(__name__)


class Camera(object):
    thread = None               # background thread that reads frames from camera
    frame_buffer = BytesIO()   # current frame is stored here by background thread
    frame_ready = False
    last_access = 0             # time of last client access to the camera
    mutex = Lock()

    @classmethod
    def initialize(cls):
        if cls.thread is None:
            logger.info('Initializing camera thread.')

            # start background frame thread
            cls.thread = Thread(target=cls._thread)
            cls.thread.start()

            # wait until frames start to be available
            while not cls.frame_ready:
                time.sleep(0)
        else:
            logger.info('thread already init-ed.  just return the frame')

    @classmethod
    def get_frame(cls):
        logger.info('Getting frame from camera...')
        cls.last_access = time.time()
        cls.initialize()
        cls.mutex.acquire()

        try:
            cls.frame_buffer.seek(0)
            return cls.frame_buffer.read()
        finally:
            cls.mutex.release()

    @classmethod
    def _set_frame(cls, frame_data):
        cls.mutex.acquire()

        try:
            logger.info('Writing to frame')
            cls.frame_buffer.truncate(0)
            cls.frame_buffer.seek(0)
            cls.frame_buffer.write(frame_data)
        finally:
            cls.mutex.release()

    @classmethod
    def _thread(cls):
        res_width = 320
        res_height = 240

        # res_width = 640
        # res_height = 480

        # res_width = 1024
        # res_height = 768

        with picamera.PiCamera() as camera:
            # camera setup
            camera.resolution = (res_width, res_height)
            camera.hflip = True
            camera.vflip = True

            # let camera warm up
            camera.start_preview()
            print 'warming up...'
            time.sleep(2)

            path = '/run/shm/'

            # command to add timestamp banner onto pictures
            cmd = """convert -pointsize 20 -fill '#0008' -draw "rectangle 0,{banner_y} {res_width},{res_height}" -fill white -draw "text {banner_text_x},{banner_text_y} '$(date)'" {path}tmp.jpg {path}image.jpg""".format(
                path=path,
                banner_text_y=res_height - 14,
                banner_text_x=res_width - 290,
                banner_y=res_height - 40,
                res_width=res_width,
                res_height=res_height,
            )

            # 10 seconds after the last call to get_frame, disable the camera.
            # While the camera is enabled, take 1 picture per second.
            while time.time() - cls.last_access < 10:
                camera.capture('{path}tmp.jpg'.format(path=path))
                subprocess.call(cmd, shell=True)

                # save timestamped frame to the class
                with open('{path}image.jpg'.format(path=path), 'rb') as img:
                    image_contents = img.read()

                cls._set_frame(image_contents)
                cls.frame_ready = True

                time.sleep(1)

        cls.thread = None
        cls.frame_ready = False

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

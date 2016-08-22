import time
import logging
import subprocess
from io import BytesIO
from picamera import PiCamera
from threading import Thread, Lock


logger = logging.getLogger(__name__)


class Camera(object):
    thread = None               # background thread that reads frames from camera
    frame_ready = False         # flag to signify if a current frame is in the buffer
    last_access = 0             # time of last client access to the camera

    frame_buffer = BytesIO()    # current frame is stored here by background thread
    mutex = Lock()              # mutex for the frame_buffer

    @classmethod
    def initialize(cls):
        """ Initialize a new camera thread and wait for images to be written to
        the frame buffer.  If a camera thread is already active, return.
        """
        if cls.thread is None:
            logger.info('Initializing camera thread')
            # start background frame thread
            cls.thread = Thread(target=cls._thread)
            cls.thread.start()

            # wait until frames start to be available
            while not cls.frame_ready:
                time.sleep(0)

    @classmethod
    def get_frame(cls):
        """First make sure that the camera is running and has taken a photo.
        Then aquire the mutex to read the buffer and return it's contents.
        """
        cls.last_access = time.time()
        cls.initialize()
        cls.mutex.acquire()

        try:
            logger.info('Retrieving frame from buffer')
            cls.frame_buffer.seek(0)
            return cls.frame_buffer.read()
        finally:
            cls.mutex.release()

    @classmethod
    def _set_frame(cls, frame_data):
        """ Aquire the mutex for the buffer and then write binary data to it.
        """
        cls.mutex.acquire()

        try:
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

        with PiCamera() as camera:
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
            while time.time() - cls.last_access < 10:
                # take a picture and add the timestamp banner
                camera.capture('{path}tmp.jpg'.format(path=path))
                subprocess.call(cmd, shell=True)

                # read the new frame's contents from disk
                with open('{path}image.jpg'.format(path=path), 'rb') as img:
                    image_contents = img.read()

                # write frame to the buffer
                cls._set_frame(image_contents)
                cls.frame_ready = True

                # only take 1 picture per second
                time.sleep(1)

        # shutting down the thread...
        cls.thread = None
        cls.frame_ready = False

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
                camera.capture('{path}/tmp.jpg'.format(path=path))
                subprocess.call(cmd, shell=True)
                time.sleep(1)

                # save timestamped frame to the class
                with open('{path}/image.jpg'.format(path=path), 'rb') as img:
                    cls.frame = io.BytesIO(img.read())

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

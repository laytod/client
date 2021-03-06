import io
import time
import picamera
import subprocess

camera = picamera.PiCamera()

# camera default settings
camera.sharpness = 0
camera.contrast = 0
camera.brightness = 50
camera.saturation = 0
camera.ISO = 0
camera.video_stabilization = False
camera.exposure_compensation = 0
camera.exposure_mode = 'auto'
camera.meter_mode = 'average'
camera.awb_mode = 'auto'
camera.image_effect = 'none'
camera.color_effects = None
camera.rotation = 0
camera.hflip = False
camera.vflip = False
camera.crop = (0.0, 0.0, 1.0, 1.0)


# changes
camera.vflip = True
camera.hflip = True
sleep_duration = 1

if __name__ == '__main__':

    # write to shared memory (RAM) so we don't wear out the SD card
    path = '/run/shm/'
    cmd = """convert -pointsize 20 -fill '#0008' -draw "rectangle 0,450 720,480" -fill white -draw "text 430,470 '$(date)'" {path}tmp.jpg {path}image.jpg""".format(path=path)

    # loop forever taking pictures
    while True:
        camera.capture('{path}/tmp.jpg'.format(path=path))
        subprocess.call(cmd, shell=True)
        time.sleep(sleep_duration)

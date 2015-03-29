import sys
import time
import smtplib
import picamera
from subprocess import check_output, call

from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

import ConfigParser
from os import path
config = ConfigParser.ConfigParser()
config_path = path.dirname(path.dirname(path.realpath(__file__))) + '/camserv.conf'
config.read(config_path)

# email credentials
username = config.get('email', 'user')
password = config.get('email', 'pw')

pin = 27
call(['gpio', 'export', str(pin), 'in'])


def send_email(
        subject='No Subject',
        sender=None,
        recipients=None,
        body=None,
        user=None,
        pw=None,
        image_path=None):
    try:

        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = recipients
        text = MIMEText(body)
        msg.attach(text)

        if image_path:
            f = open(image_path, 'rb')
            mime_image = MIMEImage(f.read())
            f.close()
            msg.attach(mime_image)

        server = smtplib.SMTP()
        server.connect("smtp.gmail.com", 'submission')
        server.starttls()
        server.ehlo()
        server.login(user, pw)
        server.sendmail(sender, recipients, msg.as_string())
    except Exception, e:
        return e


def take_picture():

    # write to shared memory (RAM) so we don't wear out the SD card
    filename = 'alert.jpeg'
    path = '/run/shm/'
    cmd = """convert -pointsize 20 -fill '#0008' -draw "rectangle 0,450 720,480" -fill white -draw "text 430,470 '$(date)'" {path}{filename} {path}{filename}""".format(path=path, filename=filename)

    with picamera.PiCamera() as camera:
        camera.resolution = (800, 600)
        camera.start_preview()
        # Camera warm-up time
        time.sleep(2)
        camera.capture(path+filename)

        # add timestamp
        call(cmd, shell=True)

    return path+filename


def get_pin_status(pin):
    return int(check_output(['gpio', '-g', 'read', str(pin)]))


if __name__ == '__main__':
    send_alert = config.get('pir', 'email')
    read_interval = 0.5
    # seconds_to_sleep = 10
    admins = 'laytod@gmail.com'
    subject = 'Email Subject'
    body = """
    Hello,
        There was motion detected.
    """

    while True:
        status = get_pin_status(pin)

        if status == 1:
            if send_alert:
                send_email(
                    sender=username,
                    recipients=admins,
                    subject=subject,
                    body=body,
                    user=username,
                    pw=password,
                    image_path=take_picture(),
                )
            print 'sent email to {recipients}'.format(recipients=admins)
            sys.exit(0)

            # time.sleep(seconds_to_sleep)
        time.sleep(read_interval)

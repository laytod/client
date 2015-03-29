import sys
import time
import smtplib
from subprocess import check_output, call

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
        pw=None):
    try:
        server = smtplib.SMTP()
        server.connect("smtp.gmail.com", 'submission')
        server.starttls()
        server.ehlo()
        server.login(user, pw)
        server.sendmail(sender, recipients, 'Subject: {subject}\n\n{body}'.format(subject=subject, body=body))
    except Exception, e:
        return e


def get_pin_status(pin):
    return int(check_output(['gpio', '-g', 'read', str(pin)]))


if __name__ == '__main__':
    read_interval = 0.5
    # seconds_to_sleep = 10
    admins = ['laytod@gmail.com']
    subject = 'Email Subject'
    body = """
    Hello,
        There was motion detected.
    """

    while True:
        status = get_pin_status(pin)

        if status == 1:
            print "motion detected"
            send_email(
                sender=username,
                recipients=admins,
                subject=subject,
                body=body,
                user=username,
                pw=password
            )
            print 'sent email to {recipients}'.format(recipients=admins)
            sys.exit(0)

            # time.sleep(seconds_to_sleep)
        time.sleep(read_interval)

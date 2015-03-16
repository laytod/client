import time
from subprocess import check_output, call

pin = 27
seconds_to_sleep = 1
call(['gpio', 'export', str(pin), 'in'])


def get_pin_status(pin):
    return int(check_output(['gpio', '-g', 'read', str(pin)]))


if __name__ == '__main__':

	print "monitoring pin {pin}".format(pin=pin)

	while True:
		status = get_pin_status(pin)

		if status == 1:
			print "motion detected"

		time.sleep(seconds_to_sleep)

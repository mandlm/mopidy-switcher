#!/usr/bin/python

import glob
import os
import subprocess
import ConfigParser

import RPi.GPIO as GPIO

yellowLed = 15
redLed = 17
greenLed = 18

buttonPin = 27
dummyPin = 1

mopidyConf = '/etc/mopidy/mopidy.conf'
userDir = '/etc/mopidy/conf.user/'

def setLeds(yellow, red, green):
    GPIO.output(yellowLed, yellow)
    GPIO.output(redLed, red)
    GPIO.output(greenLed, green)

def getConfiguredLedColor():
	config = ConfigParser.ConfigParser()
	config.read(mopidyConf)

	return config.get('moped-switcher', 'led')

def setConfiguredLedColor():
	ledColor = getConfiguredLedColor()

	if ledColor == 'yellow':
		setLeds(1, 0, 0)
	elif ledColor == 'red':
		setLeds(0, 1, 0)
	elif ledColor == 'green':
		setLeds(0, 0, 1)

def stopMopidy():
    command = ['service', 'mopidy', 'stop']
    subprocess.call(command, shell=False)

def startMopidy():
    command = ['service', 'mopidy', 'start']
    subprocess.call(command, shell=False)

def getConfigs():
    return sorted(glob.glob(os.path.join(userDir, '*.conf')))

def getCurrentConfig():
    if os.path.islink(mopidyConf):
        return os.path.realpath(mopidyConf)
    else:
        return None

def getNextConfig():
    currentConfig = getCurrentConfig()
    availableConfigs = getConfigs()    
    currentIndex = availableConfigs.index(currentConfig)
    nextIndex = (currentIndex + 1) % len(availableConfigs)
    return availableConfigs[nextIndex]

def setConfig(newConfig):
    if os.path.islink(mopidyConf) and os.path.isfile(newConfig):
        os.unlink(mopidyConf)
        os.symlink(newConfig, mopidyConf)

def switchConfig():
    setConfig(getNextConfig())
    
def buttonHandler(channel):
	print 'Switching to ' + getNextConfig()
	try:
		setLeds(0, 0, 0)
		stopMopidy()
		switchConfig()
		startMopidy()
		setConfiguredLedColor()
	except OSError as e:
		print 'Error: ' + e.strerror

if __name__ == '__main__':
	GPIO.setmode(GPIO.BCM)

	GPIO.setup(yellowLed, GPIO.OUT)
	GPIO.setup(redLed, GPIO.OUT)
	GPIO.setup(greenLed, GPIO.OUT)

	GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.setup(dummyPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

	GPIO.add_event_detect(buttonPin, GPIO.FALLING, callback=buttonHandler, bouncetime=1000)

        setConfiguredLedColor()

	try:
		while True:
			GPIO.wait_for_edge(dummyPin, GPIO.RISING)
	finally:
		GPIO.cleanup()

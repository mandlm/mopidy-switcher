#!/usr/bin/python

from time import sleep

import RPi.GPIO as GPIO

yellowLed = 15
redLed = 17
greenLed = 18

buttonPin = 27

sleepTimes = [0.75, 0.5, 0.25, 0.125, 0.0625]
sleepTimeIndex = 0

def buttonHandler(channel):
    global sleepTimeIndex
    print 'button pushed'
    sleepTimeIndex = (sleepTimeIndex + 1) % len(sleepTimes)

def setLeds(yellow, red, green):
    GPIO.output(yellowLed, yellow)
    GPIO.output(redLed, red)
    GPIO.output(greenLed, green)
    
try:
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(yellowLed, GPIO.OUT)
    GPIO.setup(redLed, GPIO.OUT)
    GPIO.setup(greenLed, GPIO.OUT)

    GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
    GPIO.add_event_detect(buttonPin, GPIO.FALLING, callback=buttonHandler, bouncetime=1000)    

    while True:
        setLeds(1, 0, 0)
        sleep(sleepTimes[sleepTimeIndex])
        setLeds(0, 1, 0)
        sleep(sleepTimes[sleepTimeIndex])
        setLeds(0, 0, 1)
        sleep(sleepTimes[sleepTimeIndex])
finally:
    setLeds(0, 0, 0)
    GPIO.cleanup()

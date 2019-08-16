

from evdev import InputDevice, categorize, ecodes, list_devices

import RPi.GPIO as GPIO
import time

#TODO Make this not ass
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

gamepad = InputDevice('/dev/input/event1')

leftForwardPin = 20
leftBackwardPin = 16 
leftPwmPin = 21

rightForwardPin = 26
rightBackwardPin = 19
rightPwmPin = 13

def pwmSetup(pin):
    GPIO.setup(pin, GPIO.OUT)
    temp = GPIO.PWM(pin, 100)
    temp.start(0)
    return temp

GPIO.setup(leftForwardPin, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(leftBackwardPin, GPIO.OUT, initial=GPIO.LOW)
leftPwm = pwmSetup(leftPwmPin)

GPIO.setup(rightForwardPin, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(rightBackwardPin, GPIO.OUT, initial=GPIO.LOW)
rightPwm = pwmSetup(rightPwmPin)

def handleRight(value):
    if value > 10:
        GPIO.output(rightForwardPin, GPIO.HIGH)
        GPIO.output(rightBackwardPin, GPIO.LOW)
        rightPwm.ChangeDutyCycle(value)
    elif value < -10:
        GPIO.output(rightForwardPin, GPIO.LOW)
        GPIO.output(rightBackwardPin, GPIO.HIGH)
        rightPwm.ChangeDutyCycle(abs(value))
    else:
        GPIO.output(rightForwardPin, GPIO.LOW)
        GPIO.output(rightBackwardPin, GPIO.LOW)
        rightPwm.ChangeDutyCycle(0)

def handleLeft(value):
    if value > 10:
        GPIO.output(leftForwardPin, GPIO.HIGH)
        GPIO.output(leftBackwardPin, GPIO.LOW)
        leftPwm.ChangeDutyCycle(value)
    elif value < -10:
        GPIO.output(leftForwardPin, GPIO.LOW)
        GPIO.output(leftBackwardPin, GPIO.HIGH)
        leftPwm.ChangeDutyCycle(abs(value))
    else:
        GPIO.output(leftForwardPin, GPIO.LOW)
        GPIO.output(leftBackwardPin, GPIO.LOW)
        leftPwm.ChangeDutyCycle(0)

gamepad = None

while True:
    if gamepad:
        for event in gamepad.read_loop():
            if event.type == ecodes.EV_KEY:
                print("BUTTON", event)
            elif event.type == ecodes.EV_ABS:
                absevent = categorize(event)
                max = 65536
                #Take the 16 bit value and convert it to be between -100 and 100 for PWM
                value = (absevent.event.value / ( max / 2 ) - 1) * 100
                code = ecodes.bytype[absevent.event.type][absevent.event.code]
                #print(ecodes.bytype[absevent.event.type][absevent.event.code], absevent.event.value)
                if code == "ABS_Y":
                    handleLeft(value)
                elif code == "ABS_RZ":
                    handleRight(value)
                    #print(code, value)
    else:
        time.sleep(.1)
        devices = [InputDevice(path) for path in list_devices()]
        for device in devices:
                if "Xbox Wireless Controller" in device.name:
                    gamepad = device



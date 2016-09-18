#!/usr/bin/python3

import RPi.GPIO as GPIO
import requests
from firebase import firebase
import time

SERVO_PIN = 18
LIGHT_PIN = 17
SPEAKER_PIN = 19
SWITCH_PIN = 23

SERVO_OPEN = 12.5
SERVO_CLOSE = 5

BUTTON_PRESSED = False



class App:
    def dispenseDosage(self):
        nDosage = self.firebaseApp.get('/patients/197214/dosage', None)
        print("nDosage:" + str(nDosage))
        for val in range (0, nDosage):
            GPIO.output(LIGHT_PIN, True)
            self.servoPWM.ChangeDutyCycle(SERVO_OPEN)
            # speakerPWM.ChangeDutyCycle(24)
            time.sleep(2)
            # speakerPWM.ChangeDutyCycle(0)
            self.servoPWM.ChangeDutyCycle(SERVO_CLOSE)
            GPIO.output(LIGHT_PIN, False)
            time.sleep(2)
    def mainLoop(self):
        while True:
            result = self.firebaseApp.get('/patients/197214/alert', None)
            input_state = GPIO.input(SWITCH_PIN)

            # button
            if input_state == BUTTON_PRESSED:
                print("Button: " + str(input_state))
                self.dispenseDosage()

            # if alert was true
            elif bool(result) == True:
                self.dispenseDosage()
                self.firebaseApp.put('/patients/197214', "alert", False)
                    # input_state = GPIO.input(SWITCH_PIN)

                    # Turn Servo

            # if alert was false
            elif bool(result) == False:
                nextDispenseTimeStamp = self.firebaseApp.get('/patients/197214/nextDispense', None)
                dosesPerDay = self.firebaseApp.get('/patients/197214/dosesPerDay', None)
                curTimestamp = time.time()
                print(curTimestamp)
                print(nextDispenseTimeStamp)
                print(dosesPerDay)
                if curTimestamp >= nextDispenseTimeStamp and dosesPerDay !=0 : # has scheduling
                    self.dispenseDosage()
                    nextDispense = 24/dosesPerDay*60*60 + curTimestamp
                    self.firebaseApp.put('/patients/197214','nextDispense', nextDispense  )
                else: # no scheduling
                    print('waiting')

            time.sleep(5)
    def __init__(self):
        # GPIO Setup
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(SERVO_PIN, GPIO.OUT)
        GPIO.setup(SPEAKER_PIN, GPIO.OUT)
        GPIO.setup(LIGHT_PIN, GPIO.OUT)
        GPIO.setup(SWITCH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        self.servoPWM = GPIO.PWM(SERVO_PIN, 70)
        self.servoPWM.start(SERVO_CLOSE)
        self.firebaseApp = firebase.FirebaseApplication('https://lumohacks-med-disp.firebaseio.com', None)

        self.mainLoop()




try:
    App()
except KeyboardInterrupt:
    print('Program Interrupted')
finally:
    GPIO.cleanup()

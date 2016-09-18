#!/usr/bin/python3


import RPi.GPIO as GPIO
import requests
from firebase import firebase
import time

SERVO_PIN = 18
LIGHT_PIN = 17
SPEAKER_PIN = 19
SWITCH_PIN = 23

BUTTON_PRESSED = False


# GPIO Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO_PIN, GPIO.OUT)
GPIO.setup(SPEAKER_PIN, GPIO.OUT)
GPIO.setup(LIGHT_PIN, GPIO.OUT)
GPIO.setup(SWITCH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
servoPWM = GPIO.PWM(SERVO_PIN, 70)
# speakerPWM = GPIO.PWM(SPEAKER_PIN, 100)

servoPWM.start(5)
# speakerPWM.start(0)

firebase = firebase.FirebaseApplication('https://lumohacks-med-disp.firebaseio.com', None)



try:


    while True:
        result = firebase.get('/patients/197214/alert', None)
        input_state = GPIO.input(SWITCH_PIN)
        if input_state == False:
            print("58008: " + str(input_state))
            nDosage = firebase.get('/patients/197214/dosage', None)
            print("nDosage:" + str(nDosage))
            for val in range (0, nDosage):
                GPIO.output(LIGHT_PIN, True)
                servoPWM.ChangeDutyCycle(15)
                # speakerPWM.ChangeDutyCycle(24)
                time.sleep(2)
                # speakerPWM.ChangeDutyCycle(0)
                servoPWM.ChangeDutyCycle(3.5)
                GPIO.output(LIGHT_PIN, False)
                time.sleep(2) 
                BUTTON_PRESSED = False

        elif bool(result) == False: 
            time.sleep(5)
            print('waiting')

        

        else:
            nDosage = firebase.get('/patients/197214/dosage', None)
            print("nDosage:" + str(nDosage))
            for val in range (0, nDosage):
                GPIO.output(LIGHT_PIN, True)
                servoPWM.ChangeDutyCycle(12.5)
                # speakerPWM.ChangeDutyCycle(24)
                time.sleep(2)
                # speakerPWM.ChangeDutyCycle(0)
                servoPWM.ChangeDutyCycle(5)
                GPIO.output(LIGHT_PIN, False)
                time.sleep(2) 
            # input_state = GPIO.input(SWITCH_PIN)

            # Turn Servo
            firebase.put('/patients/197214', "alert", False)
            
except KeyboardInterrupt:
    GPIO.cleanup()


GPIO.cleanup()

# class App:
#
#     def __init__(self, master):
#         GPIO.output(17, False);
#         frame = Frame(master)
#         frame.pack()
#         scale = Scale(frame, from_=2, to=230,
#               orient=HORIZONTAL, command=self.update)
#         scale.grid(row=0)
#
#
#     def update(self, angle):
#         duty = float(angle) / 10.0 + 2.5
#         print duty
#         if(duty == LIGHT_OFF):
#             GPIO.output(17, False)
#         else:
#             GPIO.output(17, True)
#
#         servoPWM.ChangeDutyCycle(duty)
#
#
#
# root = Tk()
# root.wm_title('Servo Control')
# app = App(root)
# root.geometry("200x50+0+0")
# root.mainloop()

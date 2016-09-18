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
servoPWM = GPIO.PWM(SERVO_PIN, 50)
speakerPWM = GPIO.PWM(SPEAKER_PIN, 100)

servoPWM.start(7.5)
speakerPWM.start(0)

firebase = firebase.FirebaseApplication('https://lumohacks-med-disp.firebaseio.com', None)
result = firebase.get('/patients/jeffrey_leung/alert', None)
print(result)


try:
    while True:
        input_state = GPIO.input(SWITCH_PIN)
        if input_state == BUTTON_PRESSED:
            GPIO.output(LIGHT_PIN, True)
            servoPWM.ChangeDutyCycle(12)
            speakerPWM.ChangeDutyCycle(24)
            time.sleep(2)

            speakerPWM.ChangeDutyCycle(0)
            servoPWM.ChangeDutyCycle(2.5)
            GPIO.output(LIGHT_PIN, False)
            time.sleep(2)
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

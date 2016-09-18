from Tkinter import *
import RPi.GPIO as GPIO
import time

# GPIO Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(17, GPIO.OUT)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
pwm = GPIO.PWM(18, 100)
pwm.start(5)

LIGHT_OFF = 2.7

class App:

    def __init__(self, master):
        GPIO.output(17, False);
        frame = Frame(master)
        frame.pack()
        scale = Scale(frame, from_=2, to=230,
              orient=HORIZONTAL, command=self.update)
        scale.grid(row=0)


    def update(self, angle):
        duty = float(angle) / 10.0 + 2.5
        print duty
        if(duty == LIGHT_OFF):
            GPIO.output(17, False)
        else:
            GPIO.output(17, True)

        # pwm.ChangeDutyCycle(duty)



root = Tk()
root.wm_title('Servo Control')
app = App(root)
root.geometry("200x50+0+0")
root.mainloop()

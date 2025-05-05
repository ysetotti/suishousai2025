import gpiozero
from gpiozero import LED,Button
from time import sleep
import threading

led = LED(25)
led.on()

btn = Button(27)
btn2 = Button(17)

# pin = gpiozero.DigitalInputDevice(pin=27, pull_up=False)
def say_hello():
    print("LED toggle")

#button pressed
def irrecieved():
    print("irrecieved!")
    #disable continuous press
    btn2.when_pressed = None
    tm = threading.Timer(1, irrecieved_reset)
    tm.start()
    #enable button
def irrecieved_reset():
    btn2.when_pressed = irrecieved


btn.when_pressed = say_hello

btn2.when_pressed = irrecieved


try:
    while True:
        sleep(1)
        led.toggle()
#        btn2.when_pressed = irrecieved
#        print(btn.is_active)
#        print(pin.value)

except KeyboardInterrupt:
    timer.cancel() # Stop the timer if the program is interrupted
    print("Timer stopped.")
    
finally:
    btn.close()

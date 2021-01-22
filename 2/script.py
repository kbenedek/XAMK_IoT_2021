
from gpiozero import LED, Button
from signal import pause
from time import sleep
class LEDStateMgr:
    def __init__(self, led):
        self.is_red=False
        self.led = led
    def switch_state(self):
        self.is_red = not self.is_red
        for i in range(5):
            self.led.on()
            sleep(0.5)
            self.led.off()
            sleep(0.5)
        if(self.is_red):
            self.led.on()
        else:
            self.led.off()
led = LED(25)
button = Button(2)
mgr = LEDStateMgr(led)
button.when_pressed = mgr.switch_state
pause()


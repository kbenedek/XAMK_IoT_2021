from gpiozero import PWMLED
from time import sleep
from pigpio_encoder import pigpio_encoder
    
class Callback:
    def __init__(self, led,rotary):
        self.led = led
        self.isMemoryValid = False
        self.oldValue = 0
        self.currentValue = 0
        self.resolution = 100
        self.rotary =  rotary
        self.log_message_index= 0
    
    def rotary_callback(self, counter):
        self._invalidateMemory()
        self._updateCurrentValue(counter)
        self._syncValues()
        self.log("Rotator")
    
    def button_callback(self):
        if self.isMemoryValid:
            self._setRotatorValue(self.oldValue)
            self._invalidateMemory()
        else:
            self._saveToMemory()
            self._setRotatorValue(0)

        self._syncValues()
        self.log("Button")
    
    def _updateCurrentValue(self, counter):
        self.currentValue = counter/self.resolution
    def _saveToMemory(self):
        self.isMemoryValid = True
        self.oldValue = self.currentValue
    def _invalidateMemory(self):
        self.isMemoryValid = False
        self.oldValue = None
        
    def _setRotatorValue(self, value):
        self.currentValue = value
        self.rotary.last_counter = int(value*self.resolution)
        self.rotary.counter = int(value*self.resolution)
        
    
    def _syncValues(self):
        self.led.value = self.currentValue
        
    def log(self, Function):
        print(self.log_message_index, Function, "\n",
        self.isMemoryValid,
        self.oldValue ,"\n",
        self.currentValue,
        self.rotary.counter)
        self.log_message_index += 1
    
def main():
    led = PWMLED(16)
    led.value = 0
    rotary = pigpio_encoder.Rotary(clk=24, dt=23, sw=18)
    callback = Callback(led, rotary)
    rotary.setup_rotary(min=0, max=100, scale=10, debounce=100, rotary_callback=callback.rotary_callback)
    rotary.setup_switch(sw_short_callback=callback.button_callback)

    rotary.watch()
    
    
if __name__ == "__main__":
    main()


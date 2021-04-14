from gpiozero import PingServer, LED
from gpiozero.tools import negated
from signal import pause
from tkinter import *

print("running")

window = Tk()
window.title("Home indicator")
window.geometry("300x200")

class HomeLed:
    def __init__(self, _led, _entry):
        self.led = _led
        self.entry = _entry
        self.LedServer = None
        
    def ChangeAddr(self):
        self.LedServer = PingServer(self.entry.get(), 1.0)
        self.LedServer.when_activated = self.led.on
        self.LedServer.when_deactivated = self.led.off
    
    

a = Label(window, text = "Host #1").grid(row = 0, column = 1)
a1 = Entry(window, text = "ip1")
Tom = HomeLed(LED(13), a1)
a1.grid(row = 1, column = 1)

a2 = ttk.Button(window, text = "Add host", command = Tom.ChangeAddr).grid(row = 2, column = 1)

b = Label(window, text = "Host #2").grid(row = 3, column = 1)
b1 = Entry(window, text = "ip2")
Mate = HomeLed(LED(16), b1)
b1.grid(row = 4, column = 1)

b2 = ttk.Button(window, text = "Add host", command = Mate.ChangeAddr).grid(row = 5, column = 1)
print(Tom)
window.mainloop()
    
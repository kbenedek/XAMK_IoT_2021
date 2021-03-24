from gpiozero import LED
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep

factory = PiGPIOFactory(host='172.20.49.4') #replace the IP with the Raspberry Pi’s IP
 
#import necessary libraries 
from gpiozero import PWMLED
from tkinter import * 

#change the RGB LED color 
def change_color(self): 
    led.value = slider.get() 
    print(self) 

#close the window 
def close_window(): 
    window.destroy()

  #(script continues on the next page) 
#create a PWMLED object for each color 
led = PWMLED(16, pin_factory = factory) 

#create window 
window = Tk() 
window.title("PWM LED Controller") 
window.geometry("300x200") 

#create three sliders to control each RGB LED lead 
slider = Scale(window, from_=0, to=1, resolution = 0.01, orient=HORIZONTAL, 
        label="Brightness", troughcolor="white", length=200, command=change_color)
slider.pack()


#create close button 
close_button = Button(window, text="Close", command=close_window) 
close_button.pack() 

mainloop()
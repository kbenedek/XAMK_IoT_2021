#import adafruit_dht
import time 
import random
import adafruit_dht
from tkinter import *
from PIL import Image, ImageTk 

sensor = adafruit_dht.DHT11(4)
window = Tk()
window.title("Weather")
window.geometry("300x200")
hum_var = StringVar()
temp_var = StringVar()
hum = Label(window, 
                 textvariable = hum_var)
temp = Label(window, 
                 textvariable = temp_var)
sun_image = Image.open("/home/pi/Desktop/XAMK_IoT_2021/13/sun.jpeg")
sun = ImageTk.PhotoImage(sun_image)
cloud_image = Image.open("/home/pi/Desktop/XAMK_IoT_2021/13/cloud.jpeg")
cloud = ImageTk.PhotoImage(cloud_image)
image_label = Label(window, image=sun)
hum.pack()
temp.pack()
image_label.pack()



while True:
    try:
        hum, temp = sensor.humidity, sensor.temperature
        #hum, temp = random.randrange(0, 100), random.randrange(0,40)
        hum_var.set("Humidity: {}".format(hum))
        temp_var.set("Temp: {}".format(temp))
        if hum < 50:
            image_label.configure(image=sun)
            image_label.image = sun
        else:
            image_label.configure(image=cloud)
            image_label.image = cloud
            
    except RuntimeError as error: 
        print(error.args[0])
    window.update_idletasks()
    window.update()
    time.sleep(2.0)
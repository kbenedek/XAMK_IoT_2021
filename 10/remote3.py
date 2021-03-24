import socket
import pygame.mixer
from pygame.mixer import Sound
import webbrowser

#factory = PiGPIOFactory(host='172.20.49.4') #replace the IP with the Raspberry Pi’s IP
 
pygame.mixer.init()

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP 
client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1) 
client.bind(("", 42069)) 
while True: 
    data, addr = client.recvfrom(1024) 
    print("received message: {addr}".format(addr=addr))
    bell = Sound("asdasd.wav")
    bell.play()
    
    ie = webbrowser.get()
    ie.open("{addr}:{port}".format(addr=addr[0], port=8000))
    

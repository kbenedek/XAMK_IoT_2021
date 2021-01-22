import pygame.mixer
from pygame.mixer import Sound
from gpiozero import Button
from signal import pause
pygame.mixer.init()
button_sounds = {
        Button(2): Sound("samples/1.wav"),
        Button(3): Sound("samples/2.wav"),
        Button(14): Sound("samples/3.wav"),
        Button(15): Sound("samples/4.wav"),
        Button(17): Sound("samples/5.wav"),
        Button(18): Sound("samples/6.wav"),
        Button(22): Sound("samples/Jeff.wav"),
        Button(27): Sound("samples/8.wav"),
        }
for button, sound in button_sounds.items():
    button.when_pressed = sound.play
    
pause()

import RPi.GPIO as GPIO 
from mfrc522 import SimpleMFRC522
from gpiozero import Buzzer, LED 
from time import sleep 

green_led = LED(18)
red_led = LED(5)
class NFCMock:
    def __init__(self, id):
        self.id = id
        self.text = None
    def read(self):
        return self.id, self.text
    def write(self, text):
        self.text=text
        
HASH_OF_THE_MONTH =42069
bz = Buzzer(26, active_high=False)

def beep_once():
    bz.on()
    sleep(0.05)
    bz.off()

def accept():
    green_led.on()
    beep_once()
    sleep(1)
    green_led.off()
def deny():
    red_led.on()
    for i in range(0, 5):
        beep_once()
        sleep(0.2)
    red_led.off()
def get_amount(reader):
    id, text = reader.read()
    data_list = text.split()
    hasMonthlyPass = int(data_list[0]) == HASH_OF_THE_MONTH
    amount_of_money = int(data_list[1])
    return hasMonthlyPass, amount_of_money

def write_amount(reader, monthly_pass, money):
    if monthly_pass:
        reader.write("{} {}".format(HASH_OF_THE_MONTH, money))
    else:
        reader.write("{} {}".format(0, money))
def deduct(reader, amount):
    monthly_pass, money = get_amount(reader)
    write_amount(reader, monthly_pass, money-amount)
    
def add_monthly_pass(reader):
    monthly_pass, money = get_amount(reader)
    write_amount(reader, True, money)
    
def add_money(reader, amount):
    monthly_pass, money = get_amount(reader)
    write_amount(reader, monthly_pass, money+amount)
    
reader = SimpleMFRC522()
while True:
    #reader = NFCMock(1)
    write_amount(reader, 0, 400)
    #add_money(reader, 200)
    #add_monthly_pass(reader)
#     monthly_pass, money = get_amount(reader)
#     print(monthly_pass, money)
#     if monthly_pass:
#         accept()
#     elif money > 200:
#         deduct(reader, 200)
#     else:
#         deny()
    monthly_pass, money = get_amount(reader)
    print(monthly_pass, money)
    sleep(5)


from machine import Pin, PWM
import time
from time import sleep_ms

servo=PWM(Pin(15))
servo.freq(50)

while True:
    
    for pulso in range(500000, 2500000,500):
        servo.duty_ns(pulso)
        time.sleep_ms(1)
        
    for pulso in range(2500000, 500000,-500):
        servo.duty_ns(pulso)
        time.sleep_ms(1)
        
    
    
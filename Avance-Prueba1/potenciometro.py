from machine import Pin, ADC
from time import sleep
potente = ADC(27)
def potenciometro():
    while True:
        lectura = potente.read_u16()
        if 200 < lectura < 17300:
            print("Producto 1")
            sleep(0.5)

            
        if 17300 < lectura < 40100:
            print("Producto 2")
            sleep(0.5)
            
        if lectura > 40100:
            print("Producto 3")
            sleep(0.5)
            
potenciometro()
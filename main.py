from machine import Pin
from machine import ADC
from utime import sleep

# 7-segment display layout
#       A
#      ---
#  F |  G  | B
#      ---
#  E |     | C
#      ---
#       D




"""
Listas sacadas de un repositorio de github de Anderson Costa:
https://github.com/arcostasi/my-wokwi-projects/blob/main/pico-hello-micropython/main.py
"""


pins = [
    Pin(13, machine.Pin.OUT), # A
    Pin(12, machine.Pin.OUT), # B
    Pin(18, machine.Pin.OUT), # C
    Pin(17, machine.Pin.OUT), # D
    Pin(16, machine.Pin.OUT), # E
    Pin(14, machine.Pin.OUT), # F
    Pin(15, machine.Pin.OUT)  # G
]

number_map = [
    [0, 0, 0, 0, 0, 0, 1],  # 0
    [1, 0, 0, 1, 1, 1, 1],  # 1
    [0, 0, 1, 0, 0, 1, 0],  # 2
    [0, 0, 0, 0, 1, 1, 0],  # 3
    [1, 0, 0, 1, 1, 0, 0],  # 4
    [0, 1, 0, 0, 1, 0, 0],  # 5
    [0, 1, 0, 0, 0, 0, 0],  # 6
    [0, 0, 0, 1, 1, 1, 1],  # 7
    [0, 0, 0, 0, 0, 0, 0],  # 8
    [0, 0, 0, 0, 1, 0, 0]   # 9
]

"""
Función sacada de la página:
https://electrocredible.com/7-segment-display-with-raspberry-pi-pico/
"""
def reset():
    for pin in pins:
        pin.value(1)

def display_number(number):
    pins_values = number_map[number]
    for i in range(len(pins)):
        pins[i].value(pins_values[i])
        
"""
Código Inspirado de:..
https://youtu.be/IkbVy6IKhzU
"""

potente = ADC(27)
producto = 1
def potenciometro():
    global cantidad1, cantidad2, cantidad3, producto
    while True:
        lectura = potente.read_u16()
        
        if 200 < lectura < 17300:
            print("Producto 1")
            display_number(cantidad1)
            producto = 1
            sleep(0.8)
            
        if 17300 < lectura < 40100:
            print("Producto 2")
            display_number(cantidad2)
            producto = 2      
            sleep(0.8)
            
        if lectura > 40100:
            print("Producto 3")
            display_number(cantidad3)
            producto = 3
            sleep(0.8)
            
        if btn.value() == 0:
                seleccion(producto)

def error():
    print("vacío")

btn = Pin(19, Pin.IN, Pin.PULL_UP)
cantidad1 = 9
cantidad2 = 9
cantidad3 = 9


def seleccion(producto):
    
    global cantidad1, cantidad2, cantidad3

    if producto == 1:
        if cantidad1 == 0:
            error()
        else:
            cantidad1 -=1
            print(cantidad1)
            display_number(cantidad1)
                    
    if producto == 2:
        if cantidad2 == 0:
            error()
        else:
            cantidad2 -=1
            print(cantidad2)
            display_number(cantidad2)

    if producto == 3:
        if cantidad3 == 0:
            error()
        else:
            cantidad3 -=1
            print(cantidad3)
            display_number(cantidad3)
    



number = 6
potenciometro()

#display_number(number)
sleep(3)
reset()

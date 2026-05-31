from machine import Pin
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
        
display_number(9)
reset()
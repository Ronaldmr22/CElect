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

led1 = Pin(20, Pin.OUT)
led2 = Pin(21, Pin.OUT)


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
            if cantidad1 == 0:
                led1.value(0)
                led2.value(1)
            else:
                led2.value(0)
                led1.value(1)
            sleep(0.8)
            
        if 17300 < lectura < 40100:
            print("Producto 2")
            display_number(cantidad2)
            producto = 2
            if cantidad2 == 0:
                led1.value(0)
                led2.value(1)
            else:
                led2.value(0)
                led1.value(1)
            sleep(0.8)
            
        if lectura > 40100:
            print("Producto 3")
            display_number(cantidad3)
            producto = 3
            if cantidad3 == 0:
                led1.value(0)
                led2.value(1)
            else:
                led2.value(0)
                led1.value(1)
            sleep(0.8)
            
        if btn.value() == 0:
                seleccion(producto)

def error():
    print("vacío")


servo=PWM(Pin(20))
def caida():
    global producto, btn
    if producto!=0 and btn.value()==1:
        for pulso in range(500000, 1250000,500):
            servo.duty_ns(pulso)
            sleep(0.5)
        sleep(5)
        for pulso in range(1250000, 500000,-500):
            servo.duty_ns(pulso)
            sleep(0.5)
    else:
        caida()

btn = Pin(5, Pin.IN, Pin.PULL_UP)
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
            caida()
            
                    
    if producto == 2:
        if cantidad2 == 0:
            error()
        else:
            cantidad2 -=1
            print(cantidad2)
            display_number(cantidad2)
            caida()

    if producto == 3:
        if cantidad3 == 0:
            error()
        else:
            cantidad3 -=1
            print(cantidad3)
            display_number(cantidad3)
            caida()
    


# main.py (MicroPython)
import network
import socket
import time
from machine import Pin

SSID = "NOMBRE RED WIFI" #No debe tener caracteres especiales
PASSWORD = "12345678"

led = Pin(1, Pin.OUT)

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    
    print("Conectando a WiFi...", end="")
    while not wlan.isconnected():
        print(".", end="")
        time.sleep(0.5)
    print("\nConectado:", wlan.ifconfig())
    return wlan.ifconfig()[0]

def start_server(ip):
    s = socket.socket()
    s.bind((ip, 1717))
    s.listen(1)
    print("Esperando conexión del cliente...")
    conn, addr = s.accept()
    print("Conectado desde:", addr)
    
    while True:
        data = conn.recv(1024)
        if not data:
            break
        msg = data.decode()
        print("Mensaje recibido:", msg)
        
        potenciometro()
        
        
        # Acciones según el potenciometro
        if potenciometro() == 1:
            conn.send(1.encode())
        elif potenciometro() == 2:
            conn.send(2.encode())
        elif potenciometro() == 2:
            conn.send(2.encode())
        else:
            # Enviar eco de vuelta
            conn.send(f"Echo: {msg}".encode())

ip = connect_wifi()
start_server(ip)
number = 6
potenciometro()

#display_number(number)
sleep(3)
reset()

from machine import Pin, PWM
from machine import ADC
from utime import sleep
import network
import socket
import time


# 7-segment display layout
#       A
#      ---
#  F |  G  | B
#      ---
#  E |     | C
#      ---
#       D

led1 = Pin(21, Pin.OUT)
led2 = Pin(22, Pin.OUT)
potente = ADC(26)
producto = 1
cantidad1 = 0
cantidad2 = 0
cantidad3 = 0
estado = "funcionamiento"

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

def display_number(number):
    if number < 0 or number > 9:
        return 
    pins_values = number_map[number]
    for i in range(len(pins)):
        pins[i].value(pins_values[i])
        

def error():
    print("vacío")
    led1.value(0)
    led2.value(1) 


"""
Código sacado de: https://youtu.be/Yr4IAHIj_PU?si=nsrcWIhENvnc668r
"""
servo=PWM(Pin(27))
servo.freq(50)
def caida():
    global btn
    for pulso in range(500000, 1300000,500):
        servo.duty_ns(pulso)
        sleep(0.002)
    sleep(4)
    for pulso in range(1300000, 500000,-500):
        servo.duty_ns(pulso)
        sleep(0.002)

btn = Pin(5, Pin.IN, Pin.PULL_UP)

def seleccion(producto):
    
    global cantidad1, cantidad2, cantidad3

    if producto == 1:
        if cantidad1 == 0:
            error()
            return
        else:
            print(cantidad1)
            display_number(cantidad1)
            caida()
            return 1
            
                    
    if producto == 2:
        if cantidad2 == 0:
            error()
            return
        else:
            print(cantidad2)
            display_number(cantidad2)
            caida()
            return 2

    if producto == 3:
        if cantidad3 == 0:
            error()
            return
        else:
            print(cantidad3)
            display_number(cantidad3)
            caida()
            return 3
    
def mantenimiento():
    patron = [1, 0, 0, 1, 0, 0, 0]

    for i in range(len(pins)):
        pins[i].value(patron[i])
    

SSID = "rasp" #No debe tener caracteres especiales
PASSWORD = "abc12345"

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
    global cantidad1, cantidad2, cantidad3
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((ip, 1717))
    s.listen(1)
    print("Esperando conexión del cliente...")
    conn, addr = s.accept()
    conn.setblocking(False)
    print("Conectado desde:", addr)
    
    

    
    while True:
        """
        Código Inspirado de:..
        https://youtu.be/IkbVy6IKhzU
        """
        global producto, cantidad1, cantidad2, cantidad3, estado
        
        try:
            data = conn.recv(1024)
            msg = data.decode()
            print("Mensaje recibido:", msg)

            if msg == "mantenimiento":
                estado = "mantenimiento"
            elif msg == "funcionamiento":
                estado = "funcionamiento"

            elif estado == "funcionamiento":
                
                cantidades = msg.split(",")
                cantidad1 = int(cantidades[0])
                cantidad2 = int(cantidades[1])
                cantidad3 = int(cantidades[2])

        except:
            pass
        
        if estado == "mantenimiento":
            mantenimiento()
            sleep(0.2)
            continue
        
        lectura = potente.read_u16()
        if 200 < lectura < 17300:
            print("Producto 1")
            producto = 1
            display_number(cantidad1)
            if cantidad1 == 0:
                led1.value(0)
                led2.value(1)
            else:
                led2.value(0)
                led1.value(1)
            
        elif 17300 < lectura < 40100:
            print("Producto 2")
            producto = 2
            display_number(cantidad2)
            if cantidad2 == 0:
                led1.value(0)
                led2.value(1)
            else:
                led2.value(0)
                led1.value(1)
            
        elif lectura > 40100:
            print("Producto 3")
            producto = 3
            display_number(cantidad3)
            if cantidad3 == 0:
                led1.value(0)
                led2.value(1)
            else:
                led2.value(0)
                led1.value(1)
                

        if btn.value() == 0:
            sleep(0.05)
            if btn.value() == 0:
                resultado = seleccion(producto)
                if resultado == 1:
                    conn.send("1".encode())
                    cantidad1 -= 1
                elif resultado == 2:
                    conn.send("2".encode())
                    cantidad2 -= 1
                elif resultado == 3:
                    conn.send("3".encode())
                    cantidad3 -= 1
                while btn.value() == 0:
                    sleep(0.01)
        sleep(0.05)

ip = connect_wifi()
start_server(ip)
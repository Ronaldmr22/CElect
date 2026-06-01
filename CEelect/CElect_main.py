  # cliente_gui.py
import socket
import threading
import tkinter as tk
from tkinter import *

SERVER_IP = "192.168.137.200"  # Cambia esto con la IP de la Pico W
PORT = 1717

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Defino las variables globales
precio_mentas = 100
precio_galletas = 250
precio_popis = 75
cantidad1 = 0
cantidad2 = 0
cantidad3 = 0
ganancias1 = 0
ganancias2 = 0
ganancias3 = 0


def connect():
    global cantidad1, cantidad2, cantidad3
    #Manejo de archivos "txt", fuentes: https://youtu.be/0Uba311CO_A y https://youtu.be/j7CiZl12zcA
    with open("productos.txt", "r") as f:
        contenido = f.read()
        cantidades = contenido.split("\n")
        cantidad1 = int(cantidades[0])
        cantidad2 = int(cantidades[1])
        cantidad3 = int(cantidades[2])
        print(cantidad1, cantidad2, cantidad3)
    try:
        client_socket.connect((SERVER_IP, PORT))
        status_label.config(text="Conectado al servidor")
        actualizar_labels()
        client_socket.send(f"{cantidad1},{cantidad2},{cantidad3}".encode())
        threading.Thread(target=receive_messages, daemon=True).start()
    except Exception as e:
        status_label.config(text=f"Error: {e}")



def receive_messages():
    global cantidad1, cantidad2, cantidad3, ganancias1, ganancias2, ganancias3
    while True:
        try:
            msg = client_socket.recv(1024).decode()
            print(msg)
            if msg == "1":
                cantidad1 -= 1
                ganancias1 += precio_mentas
            elif msg == "2":
                cantidad2 -= 1
                ganancias2 += precio_galletas
            elif msg == "3":
                cantidad3 -= 1
                ganancias3 += precio_popis
            # Manda las nuevas cantidades de vuelta
            client_socket.send(f"{cantidad1},{cantidad2},{cantidad3}".encode())
            actualizar_labels()
            guardar_txt()
        except:
            break

def actualizar_labels():
    cantidad1_lbl.config(text=f"Mentas: {cantidad1}")
    ganancias1_lbl.config(text=f"Ganancias mentas: ₡{ganancias1}")
    cantidad2_lbl.config(text=f"Galletas: {cantidad2}")
    ganancias2_lbl.config(text=f"Ganancias galletas: ₡{ganancias2}")
    cantidad3_lbl.config(text=f"Popis: {cantidad3}")
    ganancias3_lbl.config(text=f"Ganancias popis: ₡{ganancias3}")

def guardar_txt():
    with open("productos.txt", "w") as f:
        f.write(f"{cantidad1}\n{cantidad2}\n{cantidad3}")

def salir():
    try:
        client_socket.close()
    except:
        pass
    ventana_admin.destroy()

# GUI
#Crecion de la ventana de administración
ventana_admin = tk.Tk()
ventana_admin.state('zoomed')



#"Creación de Labels"
cantidad1_lbl = Label(text="Cantidad de mentas")
cantidad1_lbl.place(x=100, y=50)


ganancias1_lbl = Label(text="Ganancias de las mentas")
ganancias1_lbl.place(x=100, y=100)

cantidad2_lbl = Label(text="Cantidad de galletas")
cantidad2_lbl.place(x=300, y=50)
ganancias2_lbl = Label(text="Ganancias de las galletas")
ganancias2_lbl.place(x=300, y=100)

cantidad3_lbl = Label(text="Cantidad de popis")
cantidad3_lbl.place(x=500, y=50)
ganancias3_lbl = Label(text="Ganancias de los popis")
ganancias3_lbl.place(x=500, y=100)

status_label = tk.Label(ventana_admin, text="Desconectado")
status_label.place(x=500, y=20)



connect()
ventana_admin.mainloop()


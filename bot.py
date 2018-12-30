import telepot
import time
import requests as req
from telepot.loop import MessageLoop
from pprint import pprint


TOKEN = '787014842:AAEWP5sPhhBLcYdGKeHJ2a1_kp0sh6_nT3g'
BOT = telepot.Bot(TOKEN)

def verify_input(msg):
	
	content_type, chat_type, chat_id = telepot.glance(msg)
	text = msg['text']
	text = text.split(' ')
	user = msg['chat']['first_name']
	print(user)
	print(chat_id)
	print(text)
	respuesta = 'Mamate un pipi'

	# Verificar que la conversacion sea privada
	if msg['chat']['type'] != 'private':
		return 

	if 'entities' in msg:
		if text[0] == '/start':
			respuesta = 'Bienvenido '
			if user is not None:
				 respuesta += user
		elif text[0] == '/user':
			print('llego a user')
			try:
				path = 'http://localhost:8000/user/'+ text[1] + '.json'
				user = req.get(path)
				user = user.json()
				if user['tiene_deuda'] and user['deuda'] > 0:
					respuesta = 'Usuario ' + user['nombre'] + ' con deuda: ' + str(user['deuda'])
				else:
					respuesta = 'Usuario ' + user['nombre'] + ' no posee deuda'
			except IndexError:
				respuesta = 'Por favor, introduzca el id del usuario, despues de /users'
			except KeyError:
				respuesta = 'Id incorrecto, introduzca el id del usuario nuevamente'
		elif text[0] == '/users':
			path = 'http://localhost:8000/user.json'
			try:
				print('entro al try')
				users = req.get(path)
				users = users.json()
				pprint(users)
				respuesta = 'Nombre 	Deuda\n\n'
				for i in users['results']:
					print(i)
					if i['tiene_deuda'] and i['deuda'] > 0:
						print('entre en el if')
						respuesta += i['nombre'] + ' 	' + str(i['deuda']) + '\n'
						print('le asigne respuesta')
			except:
				respuesta = 'No se encontraron los usuarios'




	####
	# Registrar al usuario si no esta registrado
	####
	BOT.sendMessage(chat_id, respuesta)


def main():
	MessageLoop(BOT,verify_input).run_as_thread()
	print ('Listening ...')

	# Keep the program running.
	while 1:
		time.sleep(10)
		

if __name__ == '__main__':
	main()
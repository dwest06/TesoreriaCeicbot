import telepot
import time
import requests as req
from telepot.loop import MessageLoop
from pprint import pprint

class ComunicacionBot:
	def __init__(self):
		self.state = 0
		# Para manejar mejor las peticiones del usuario
		self.conver = {
			'/start' : 1,
			'/login' : 2,
			'/users' : 3,
			'/user'  : 4
		}
		#Variable para pedir inputs
		self.inputs = 0

	def verify_input(self, msg):
	
		content_type, chat_type, chat_id = telepot.glance(msg)
		text = msg['text']
		text = text.split(' ')
		user = msg['chat']['first_name']

		# Vemos de quien fue la solicitud
		print(user, chat_id, text)
		
		# Inicializamos una respuesta generica
		respuesta = 'Mamate un pipi'

		# Verificar que la conversacion sea privada
		if chat_type != 'private':
			return

		# Buscamos el tipo de peticion
		self.state = self.conver.get(text[0], 0)
		# Llamamos la funcion correspondiente a la paticion
		if self.state == 1:
			self.start(user, chat_id)
		elif self.state == 2:
			self.login(chat_id)
		elif self.state == 3:
			self.users(chat_id)
		elif self.state == 4:
			self.user(chat_id, text[0])

	def start(self,user, chat_id):
		respuesta = 'Bienvenido '
		if user is not None:
			respuesta += user

		BOT.sendMessage(chat_id, respuesta)

		# Se finaliza cambiando el state del objeto
		self.state = 0

	def login(self, chat_id):
		print('No implementado todavia')

		# Se finaliza cambiando el state del objeto
		self.state = 0

	def users(self, chat_id):
		path = HOST + 'user.json'
		try:
			users = req.get(path).json()
			respuesta = 'Nombre'.ljust(20,' ') + 'Deuda\n\n'
			for i in users['results']:
				if i['tiene_deuda'] and i['deuda'] > 0:
					respuesta += i['nombre'].ljust(20,' ') + str(i['deuda']).rjust(5,' ') + '\n'

		except req.ConnectionError:
			print('Ha ocurrido un error en la conexion con el servidor')
			respuesta = 'Ha ocurrido un error, intente mas tarde'

		except req.Timeout:
			print('La comunicacion con el servidor expiró')
			respuesta = 'Ha ocurrido un error, intente mas tarde'

		BOT.sendMessage(chat_id, respuesta)
		# Se finaliza cambiando el state del objeto
		self.state = 0

	def user(self, chat_id, text):

		if type(text) == int and self.inputs == 0:
			try:
				path = HOST + 'user/'+ text[1] + '.json'
				user = req.get(path).json()
				if user['tiene_deuda'] and user['deuda'] > 0:
					respuesta = 'Usuario ' + user['nombre'] + ' con deuda: ' + str(user['deuda'])
				else:
					respuesta = 'Usuario ' + user['nombre'] + ' no posee deuda'
			except IndexError:
				respuesta = 'Por favor, introduzca el id del usuario, despues de /users'

			except KeyError:

				respuesta = 'Id incorrecto, introduzca el id del usuario nuevamente'

			except req.ConnectionError:
				print('Ha ocurrido un error en la conexion con el servidor')
				respuesta = 'Ha ocurrido un error, intente mas tarde'

			except req.Timeout:
				print('La comunicacion con el servidor expiró')
				respuesta = 'Ha ocurrido un error, intente mas tarde'

			# Se finaliza cambiando el state del objeto
			self.state = 0
			self.inputs = 0

		else:
			self.inputs = 1
			respuesta = 'Por favor indica el id del user a consultar'

		BOT.sendMessage(chat_id, respuesta)

	####
	# Registrar al usuario si no esta registrado
	####
	

# Variables de entorno
TOKEN = '787014842:AAEWP5sPhhBLcYdGKeHJ2a1_kp0sh6_nT3g'
BOT = telepot.Bot(TOKEN)
COM = ComunicacionBot()
HOST = 'http://localhost:8000/'

def main():
	MessageLoop(BOT,COM.verify_input).run_as_thread()
	print ('Listening ...')

	# Keep the program running.
	while 1:
		time.sleep(10)
		

if __name__ == '__main__':
	main()
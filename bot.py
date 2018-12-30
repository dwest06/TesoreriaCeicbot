import telepot
import time
import requests as req
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from pprint import pprint

class ComunicacionBot:
	def __init__(self):
		self.state = 0
		# Para manejar mejor las peticiones del usuario
		self.conver = {
			'/help'  : 0,
			'/start' : 1,
			'/login' : 2,
			'/users' : 3,
			'/user'  : 4,
		}
		#Variable para pedir inputs
		self.inputs = 0
		self.keyboard = InlineKeyboardMarkup(inline_keyboard=[
                   [InlineKeyboardButton(text='Ayuda', callback_data='/help'), 
                    InlineKeyboardButton(text='Usuarios', callback_data='/users'),
                    InlineKeyboardButton(text='Usuario', callback_data='/user'),
                    InlineKeyboardButton(text='Ingresar', callback_data='/login')
                    ],
               ])

	def chat(self, msg):
		content_type, chat_type, chat_id = telepot.glance(msg)
		text = msg['text']
		text = text.split(' ')
		user = msg['chat']['first_name']

		# Vemos de quien fue la solicitud
		print(user, chat_id, text)

		# Verificar que la conversacion sea privada
		if chat_type != 'private':
			return

		self.verify(chat_id, text[0], user)

	def query(self, msg):
		query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
		chat_id = msg['from']['id']
		BOT.answerCallbackQuery(query_id)
		self.verify(chat_id, query_data)
		
	def verify(self, chat_id, data, user = None):
		# Buscamos el tipo de peticion
		self.state = self.conver.get(data, self.state)
		# Llamamos la funcion correspondiente a la paticion
		if self.state == 1:
			self.start(chat_id, user)
		elif self.state == 2:
			self.login(chat_id)
		elif self.state == 3:
			self.users(chat_id)
		elif self.state == 4:
			self.user(chat_id, data)
		else:
			self.help(chat_id)
			
	def help(self, chat_id):
		BOT.sendMessage(chat_id, '¿Qué desea hacer?', reply_markup=self.keyboard)

	def start(self, chat_id, user):
		respuesta = 'Bienvenido '
		if user is not None:
			respuesta += user

		BOT.sendMessage(chat_id, respuesta)

		BOT.sendMessage(chat_id, '¿Qué desea hacer?', reply_markup=self.keyboard)

		# Se finaliza cambiando el state del objeto
		self.state = 0

	def login(self, chat_id):
		print('No implementado todavia')
		respuesta = 'Aun no se ha implementado esta funcionalidad'
		BOT.sendMessage(chat_id, respuesta)
		# Se finaliza cambiando el state del objeto
		self.state = 0

	def users(self, chat_id):
		path = HOST + 'user.json'
		try:
			users = req.get(path).json()
			respuesta = 'Nombre'.ljust(19,' ') + 'Deuda\n\n'
			for i in users['results']:
				if i['tiene_deuda'] and i['deuda'] > 0:
					respuesta += i['nombre'].capitalize().ljust(20,' ') + str(i['deuda']).rjust(5,' ') + '\n'

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
		if self.inputs != 0:
			try:
				aux = int(text)
				path = HOST + 'user/'+ text + '.json'
				user = req.get(path).json()
				if user['tiene_deuda'] and user['deuda'] > 0:
					respuesta = user['nombre'].capitalize().ljust(20,' ') + str(user['deuda'])
				else:
					respuesta = 'Usuario ' + user['nombre'].capitalize() + ' no posee deuda'
				# Se finaliza cambiando el state del objeto
				self.state = 0
				self.inputs = 0
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
			except ValueError:
				print('Ingreso un string y no un numero')
				respuesta = 'Ingresa un Número'


		else:
			self.inputs = 1
			respuesta = 'Por favor indica el id(Número) del user a consultar'

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
	MessageLoop(BOT,{'chat' : COM.chat , 
					 'callback_query': COM.query}).run_as_thread()
	print ('Listening ...')

	# Keep the program running.
	while 1:
		time.sleep(10)
		

if __name__ == '__main__':
	main()
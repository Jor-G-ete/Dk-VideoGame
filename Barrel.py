import random
import constants

class Barrel:
	def __init__(self, x=0, y=0, u=0, v=0, life=1, points=100, direccion=0):
		self._x = x
		self._y = y
		self._u = u
		self._v = v
		self._points = points
		self._life = life
		self._direccion = direccion

	def get_down(self, escalera_h):
		# gereramos un numero entre 0.0 y 1.0
		if random.random() <= 0.25:
			# hacemos que descienda y pase a la siguiente plataforma
			self._y += escalera_h
			return True
		else: return False

	# metodo para mover el barrilete
	def move(self, move_x=10, move_y=10, limite_plt_x_start = 10, limite_plt_x_end=constants.ventana_x, limite_plt_y_end = constants.ventana_y):
		'''
		metodo para mover el barrilete

		:param move_x: suma o resta las unidades que le indiquemos a la x del barril
		:param limite_plt_x_start: inicio de la plataforma
		:param limite_plt_x_end:  fin de la plataforma
		:note direccion: derecha ( 0 ) e izquierda ( 1 )
		:return: no devuelve nada
		'''

		# si va a la derecha
		if self._direccion == 0:
			if self._x <= (limite_plt_x_end-move_x): self._x += move_x
			# si no esta en el fin del juego, cae a la siguiente plt
			elif self._y < limite_plt_y_end:
				self._y += move_y
				self._direccion = 1
			else:
				return False
		else:
			if self._x >= (limite_plt_x_start + move_x): self._x -= move_x
			# si no esta en el fin del juego, cae a la siguiente plt
			elif self._y < limite_plt_y_end:
				self._y += move_y
				self._direccion = 0
			else:
				return False
		return True

	def check_destruction(self, limite_y=200, limite_x=190):
		if self._x == limite_x and self._y == limite_y : return True
		else: return False

	# definimos los metodos para las propiedades
	def get_x(self):
		'''
		Devuelve la variable x

		:return: la variable x
		'''
		return self._x

	def set_x(self, x):
		'''
		setea la variable x

		:param x: int
		:return:
		'''
		self._x = x

	def get_y(self):
		'''
		Devuelve la variable y

		:return: la variable y
		'''
		return self._y

	def set_y(self, y):
		'''
		setea la variable y

		:param y: int
		:return:
		'''
		self._y = y

	def get_u(self):
		'''
		Devuelve la variable u

		:return: la variable u
		'''
		return self._u

	def set_u(self, u):
		'''
		setea la variable u

		:param u: int
		:return:
		'''
		self._u = u

	def get_v(self):
		'''
		Devuelve la variable v

		:return: la variable v
		'''
		return self._v

	def set_v(self, v):
		'''
		setea la variable v

		:param v: int
		:return:
		'''
		self._v = v

	def get_points(self):
		'''
		Devuelve los puntos

		:return: los puntos
		'''
		return self._points

	def set_points(self, points):
		'''
		setea la variable puntos

		:param puntos: int
		:return:
		'''
		self._points = points

	def get_life(self):
		'''
		Devuelve las vidas

		:return:  las vidas
		'''
		return self._life

	def set_life(self, life):
		'''
		setea la variable life

		:param life: int
		:return:
		'''
		self._life = life

	def get_direccion(self):
		'''
		devuelve el valor de la direccion

		:return: int : el valor de la direccion
		'''
		return self._direccion

	def set_direccion(self, dir):
		'''
		Fija el valor de la direccion

		:param dir: Integer
		:return:
		'''
		self._direccion = dir


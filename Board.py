# cargamos la libreria
import pyxel
from Barrel import Barrel
from Peach import Peach
import constants
import random


class Board:

	def __init__(self):
		'''
		Definimos el constructor
		'''

		# construimos la ventana
		pyxel.init(constants.ventana_x, constants.ventana_y, caption='Peach dk game')

		# Load varibles
		pyxel.load('./assets/characters.pyxres')
		self._score = 0
		self._Barriles = []
		self._Peach = Peach() # el objeto mario funcional
		self._vidas = self._Peach.get_lives()
		self._posiciones_escaleras = []
		self._animation = 0
		self._h_suelo=[]
		self._win = False

		# ponemos la musica
		pyxel.playm(0, loop=True)

		# empezamos a correr el juego
		pyxel.run(self.update, self.draw)

	def update(self):
		# comprobamos si ha pulsado la tecla de salir
		if pyxel.btnp(pyxel.KEY_Q): pyxel.quit()

		# comprobamos si ha pulsado la tecla de salir
		if pyxel.btnp(pyxel.KEY_R):
			# crear un metodo de reste
			# Volver a poner las variables a su mismo valor inicial
			pyxel.stop()
			pyxel.run(self.update, self.draw)

		# si peach no esta viva no hacemos nada
		if not self._Peach.check_alive(): return

		# comprobamos si hemos ganado
		if self._win: return

		# movemos al jugador
		self.update_player()

		# comprobamos si ha sucedido alguna colision
		self.check_collision()

		# comprobamos que sigue vivo, si no paramos el juego, o le llevamos al menu
		self.check_alive()

		# movemos los barriles
		self.move_barrels()

		# comprobamos si hay 10 barriles en movimiento, sino creamos uno nuevo
		if len(self._Barriles) < 10 and pyxel.frame_count%(constants.speed*2) == 0 and random.random() > 0.75:
			self._Barriles.append(Barrel(x=45, y=35, u=96, v=0))

		# Comprobamos si hemos ganado
		self._win = self.check_end_game()

	def draw(self):
		pyxel.cls(0)

		# pintamos la puntuacion y las vidas
		self.draw_header()

		# comprobamos si peach sigue viva y si no es el caso entonces pintamos la pantalla de fin
		if not self._Peach.check_alive():
			pyxel.text(70, 70, "YOU DIED. Try Again :)", pyxel.frame_count % 16)
			return

		if self._win:
			pyxel.text(50, 70, "YOU SAVED ME!, PEACH.", pyxel.frame_count % 16)
			pyxel.text(50, 90, "YOU WIN BABY", pyxel.frame_count % 16)
			return


		# modificamos las animaciones con la operacion XOR
		if pyxel.frame_count % constants.speed == 0:
			self._animation ^= 1

		# le quitamos la invulnerabilidad con la operacion XOR
		if pyxel.frame_count % (constants.speed * 10) == 0:
			if self._Peach.get_inmunity(): self._Peach.set_inmunity(self._Peach.get_inmunity() ^ 1)

		# dibujamos los elementos estaticos
		self.draw_static_elements()

		# pintamos los barriles
		for i in self._Barriles: pyxel.blt(i.get_x(), i.get_y(), 0, i.get_u()+(16*self._animation), i.get_v(), 16, 16)

		# pintamos a peach, multiplicamos por -1 para hacer el flip horizontal
		# si pasamos el color, ese color se vuelve trasnparatenete, ahora que se pasa el amarillo, cuando se le haga daño
		# se quedara sin pelo
		pyxel.blt(self._Peach.get_x(), self._Peach.get_y(), 0, self._Peach.get_u()+(16*self._animation), self._Peach.get_v(),
		          self._Peach.get_size() * (-1*( 1 if self._Peach.get_dir() else -1)), self._Peach.get_size(),
		          10 if self._Peach.get_inmunity() else 0)

		# pintamos el suelo y las escaleras
		self.draw_floor()

	# ################################### Update Methods ##############################################################
	def update_player(self):
		# movemos a mario a izq o a derecha
		if (pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD_1_LEFT)): #and (self._Peach.get_y() in self._h_suelo):
			self._Peach.move(1, 1)

		if (pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD_1_RIGHT)): # and (self._Peach.get_y() in self._h_suelo):
			self._Peach.move(1, 0)

		# saltamos
		if(pyxel.btn(pyxel.KEY_SPACE)) or self._Peach.get_in_jump():
			self._Peach.jump()
			self.add_score()

		# movemos arriba o abajo
		if pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.GAMEPAD_1_UP):
			for i in self._posiciones_escaleras:
				# ponemos 16 debido a que es el size del jugador y es el que tiene que subir
				if i[0]-5 <= self._Peach.get_x() <= i[2]-5 and i[3]-20 <= self._Peach.get_y() <= i[1]-20:
					self._Peach.move_up(1)

		if pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.GAMEPAD_1_DOWN):
			for i in self._posiciones_escaleras:
				if i[0]-5 <= self._Peach.get_x() <= i[2]-5 and i[3]-20 <= self._Peach.get_y() <= i[1]-20:
					self._Peach.move_down(1)


	# ################################### Draw methods ################################################################

	def draw_header(self):
		'''
		Metodo para pintar la parte de arriba

		:return:
		'''
		# pintamos el score
		s = "SCORE {:>4}".format(self._score)
		pyxel.text(5, 4, s, 12)
		pyxel.text(4, 4, s, 7)

		# pintamos las vidas
		s = "VIDAS {:>4}".format(self._vidas)
		pyxel.text(60, 4, s, 3)
		pyxel.text(59, 4, s, 7)

		# si peach no esta viva no es necesario imprimir el resto de mensajes
		if not self._Peach.check_alive(): return

		# pintamos si se ha hecho daño
		s = "Danyo:"
		pyxel.text(110, 4, s, 7)
		pyxel.text(135, 4, "Si" if self._Peach.get_inmunity() else "No", 8 if self._Peach.get_inmunity() else 11)

		# pintamos si se ha hecho daño
		s = "Inmunidad:"
		pyxel.text(150, 4, s, 7)
		pyxel.text(190, 4, "Si" if self._Peach.get_inmunity() else "No", 10 if self._Peach.get_inmunity() else 8)

		# pintamos las instrucciones
		s = ": ¡Si me quieres salvar sobre mi"
		pyxel.text(70, 15, s, 8)
		s = "tendras que saltar!"
		pyxel.text(70, 25, s, 8)

	def draw_static_elements(self):
		'''
		Funcion para pintar los elementos que son estaticos. Usaremos una variable self._animation para hacer las transiciones
		y dar el efecto de movimiento

		:return:
		'''
		# pintamos los barriles
		pyxel.blt(-16+(14*2), 5+(20*1), 0, 128, 0, 14, 14)
		pyxel.blt(-16+(14*2), 5+(16*2), 0, 128, 0, 14, 14)
		pyxel.blt(-16+(16*1), 5+(20*1), 0, 128, 0, 14, 14)
		pyxel.blt(-16+(16*1), 5+(16*2), 0, 128, 0, 14, 14)
		# pintamos dk
		pyxel.blt(*(constants.dk_coordinates[self._animation]))
		# pintamos mario
		pyxel.blt(*(constants.mario_coordinates[self._animation]))

	def draw_floor(self):
		'''
		Draw the floor and the ladders

		:return:
		'''
		# guardamos la altura de las plataformas y las vamos restando
		esc_y = constants.suelo_y
		for i in range(0, constants.n_plataformas):
			esc_y -= constants.distance_bt_floors
			# dibujamos el suelo
			pyxel.blt(constants.suelo_x, esc_y, 0, 0, 16, constants.ventana_x, constants.suelo_h)
			if len(self._h_suelo) != 6: self._h_suelo.append(esc_y-constants.suelo_h-5)

			if i != 0:
				# dibujamos las escaleras
				pyxel.rectb(constants.escalera_x[i], esc_y + (constants.suelo_h/2), constants.escalera_w, constants.escalera_h-(constants.suelo_h/2), i+1)
				# guardamos las posiciones de la escalera concretamente los lados del rectangulo
				# x1, y1, x2(x1+w), y2(y1+h)
				if len(self._posiciones_escaleras) != 5:
					self._posiciones_escaleras.append(
						(constants.escalera_x[i], esc_y + (constants.suelo_h/2)+constants.escalera_h,
						 constants.escalera_x[i]+ constants.escalera_w, esc_y + (constants.suelo_h/2))
					)

		# escalera para subir hasta mario
		pyxel.rectb(45, 25, constants.escalera_w, constants.escalera_h - (constants.suelo_h / 2), 15)

	# ################################### Utilities ###################################################################

	def move_barrels(self):
		'''
		Funcion para mover automaticamente los barriletes

		:return:
		'''
		# movemos los barriles
		if self._Barriles:
			if pyxel.frame_count % constants.speed == 0:
				for idx, i in enumerate(self._Barriles):
					descenso = False
					for idy, y in enumerate(self._posiciones_escaleras):
						# hay que sumarle los 15 pixeles
						if y[0] <= i.get_x() <= y[2] and y[3] - 5 == i.get_y() + 15:
							descenso = i.get_down(constants.distance_bt_floors)

					# si el barri no ha descendido lo movemos
					if not descenso: i.move(move_y=constants.distance_bt_floors)

					# comprobamos si destruimos el barril
					# le sumamos el tamaño del suelo mas los pixeles
					if i.get_y() >= self._h_suelo[0] + constants.suelo_h + 16: del self._Barriles[idx]

	def check_collision(self):
		'''
		Metodo para comprobar si Peach ha tocado un barri
		:return:
		'''

		# comprobamos que Peach y los barriles esten a una distancia de 16 pixeles, que es lo que ocupa la imagen
		for i in self._Barriles:
			if i.get_x()-10 <= self._Peach.get_x() <= i.get_x()+10 and i.get_y()-5 <= self._Peach.get_y() <= i.get_y()+5 and not self._Peach.get_inmunity():
				self._Peach.decrement_life()
				# usamos un operador ternario para saber hacia donde se dirige el barril y asi restar o sumar 16
				move_x = -16 if i.get_direccion() else 16
				# movemos el barril hacia el lado que deba
				i.move(move_x=move_x, move_y=constants.distance_bt_floors)
				# pintamos el nuevo marcador
				self._vidas = self._Peach.get_lives()
				# le damos unos segundos de inmunidad
				self._Peach.set_inmunity(True)

	def add_score(self):
		for i in self._Barriles:
			# si lo supera aumentamos la score
			if i.get_x()-10 <= self._Peach.get_x() <= i.get_x()+10 and i.get_y()-25 <= self._Peach.get_y() <= i.get_y()+25:
				self._score += i.get_points()

	def check_alive(self):
		'''
		Metodo para comprobar si un jugador sigue vivo o no
		:return:
		'''
		if not self._Peach.check_alive():
			pyxel.stop()
			# pyxel.play(0, 1)

	def check_end_game(self):
		'''
		Funcion que comprubea si hemos ganado
		:return: bool si ha ganado o no el juego
		'''
		if constants.mario_coordinates[0][0] - 16 <= self._Peach.get_x() <= constants.mario_coordinates[0][0] + 16  and constants.mario_coordinates[0][1] - 16 <= self._Peach.get_y() <= constants.mario_coordinates[0][1] + 16:
			return True
		else: return False

if __name__ == "__main__":
	Board()
import constants


class Peach:
    def __init__(self, x=210, y=185, lives=3, image_u=0, image_v=0, ani_size=16, dir=1):
        self._x = x
        self._y = y
        self._in_jump = False
        self._dir_jump = 1
        self._lives = lives
        self._image_u = image_u
        self._image_v = image_v
        self._ani_size = ani_size # -> Tamño de la animacion
        self._dir = dir # -> Direccion del moñeco
        self._inmunity = False
        self._jump_counter = 0



    def check_alive(self):
        if self._lives > 0: return True
        else: return False

    def move(self, x, direction, limite_x_start = 0 , limite_x_end = 190):
        '''
        Mueve el muñeco de mario

        :param x: cantidad de movimiento
        :param direction: ( 0 ) derecha, ( 1 ) izquierda
        :return: None
        '''
        # movemos el moñeco en el eje x
        if direction == 0 and (self._x <= limite_x_end-x): self._x += x
        if direction == 1 and (self._x >= limite_x_start+x): self._x -= x
        # fijamos la direccion
        self._dir = direction

    def jump(self):

        # activamos el salto
        self._in_jump = True

        # salto hacia arriba
        if self._dir_jump:
            # movemos una posicion hacia arriba
            self.move_up(1)
            # aumentamos el contador
            self._jump_counter += 1
        # descensp
        else:
            self.move_down(1)
            # decrementamos el contador
            self._jump_counter -= 1

        # fijamos la direccion
        if self._jump_counter == 0:
            self._dir_jump = 1
            self._in_jump = False
        elif self._jump_counter == constants.max_jump: self._dir_jump = 0

    def move_up(self, escalera_h):
        '''
        Metodo para subir las escaleras
        :return:
        '''

        self._y -= escalera_h

    def move_down(self, escalera_h):
        '''
        Metodo para bajar las escaleras
        :return:
        '''
        self._y += escalera_h

    def get_lives(self):
        return self._lives

    def get_x(self):
        return self._x

    def get_y(self):
        return self._y

    def get_u(self):
        return self._image_u

    def get_v(self):
        return self._image_v
    
    def get_size(self):
        return self._ani_size

    def decrement_life(self):
        '''
        Metodo para quitarle una vida a peach cuando toca un barril
        :return:
        '''
        self._lives -= 1

    def get_dir(self):
        '''
        Devuelve la direccion de peach
        :return:
        '''
        return self._dir

    def set_dir(self, dir):
        '''
        Fija la direccion de peach

        :return:
        '''
        # controlamos la entrada fijando que la direccion solo puede ser 1 o 0
        if dir != 0 or dir != 1: raise Exception("Direccion introducida no valida")
       # fijamos la direccion
        self._dir = dir

    def set_inmunity(self, inmunity):
        '''
        fija la inmunnidad
        :param inmunity:
        :return:
        '''
        self._inmunity = True if inmunity else False

    def get_inmunity(self):
        '''
        Devuelve si tiene inmunidad o no
        :return:
        '''
        return self._inmunity

    def get_in_jump(self):
        '''
        Devuelve si estaa saltando o no
        :return:
        '''
        return self._in_jump
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  8 09:32:43 2019

@author: marinabuitragoperez
"""
import random
# definimos constantes
n_plataformas = 6
ventana_x = 224
ventana_y = 256
suelo_h = 10
suelo_w = 224
suelo_x = 0
distance_bt_floors = 30
suelo_y = 200 + distance_bt_floors
escalera_h = distance_bt_floors
escalera_w = 5
escalera_x = [random.randint(10, 190) for i in range(n_plataformas)]
speed = 15 # tb vale 30
max_jump = 15

dk_coordinates = [(25, 35, 0, 64, 0, 16, 16), (25, 35, 0, 80, 0, 16, 16)]
mario_coordinates = [(50, 15, 0, 32, 0, 16, 16), (50, 15, 0, 48, 0, 16, 16)]
platforms_coordinates = (0,170,0,0,16,220,22)
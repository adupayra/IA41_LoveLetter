# -*- coding: utf-8 -*-
'''
Created on 26 oct. 2020

@author: Antoine
'''

import tkinter as tk
from src.view.View import *

class EndGameScene(tk.Frame):
    '''
    Classe s'occupant de l'affichage du menu de fin
    '''


    def __init__(self, parent):
        '''
        Constructor
        '''
        tk.Frame.__init__(self, parent, bg = 'cyan')
        self.place(relwidth = 1, relheight = 1)
        #self.bouton = tk.Button(self, command = View.get_instance().display_game_scene(), text = "test")
        #self.bouton.pack()
        
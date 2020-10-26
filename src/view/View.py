# -*- coding: utf-8 -*-
'''
Created on 26 oct. 2020

@author: Antoine
'''
import tkinter as tk

from src.view.GameScene import *
from src.view.MenuScene import *
from src.view.EndGameScene import *


class View(object):
    '''
    Classe qui gère la création de la fenêtre ainsi que les transitions entre les différentes scènes UI (entre le menu de 
    séléction, le jeu, et le menu de victoire
    '''
    
    #Unique instance de la classe View
    _instance = None
    _root = None
    _menu_scene = None
    _game_scene = None
    _end_game_scene = None
    
    def __init__(self):
        '''
        Constructor
        '''
    
    
    #Implémentation du pattern singleton afin d'avoir une unique instantiation de la classe
    
    def __new__(cls):
        if(cls._instance is None):
            cls._instance = super(View, cls).__new__(cls)
            cls._root = tk.Tk()
            cls._root.mainloop()
            
        return cls._instance
    
    def initialization(self):
        """
        #Initialition seulement si ça n'a pas déjà été fait
        if(View._root is None):
            #Création de la fenêtre et scale en fonction de la taille de l'écran de l'utilisateur
            View._root = tk.Tk()
            width_value = View._root.winfo_screenwidth()
            height_value = View._root.winfo_screenheight()
            View._root.geometry("%dx%d+0+0" % (width_value, height_value))
            
            #Création des différentes scènes
            View._menu_scene = MenuScene(self._root)
            View._game_scene = GameScene(self._root)
            #self._end_game_scene = EndGameScene(self._root)
            
            View.display_game_scene()
            View._root.mainloop()
        """
    #Getter de l'unique instance de classe
    @classmethod
    def get_instance(cls):
        return View()
    
    @classmethod
    def display_game_scene(self):
        View._game_scene.tkraise()
    
    @classmethod
    def display_end_game_scene(self):
        View._end_game_scene.tkraise()
    
    @classmethod
    def display_menu_scene(self):
        View._menu_scene.tkraise()

test = View()
        
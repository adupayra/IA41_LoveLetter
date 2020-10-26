# -*- coding: utf-8 -*-
'''
Created on 26 oct. 2020

@author: Antoine
'''
import tkinter as tk


def display_game_scene():
    View._game_scene.tkraise()

def display_end_game_scene():
    View._end_game_scene.tkraise()

def display_menu_scene():
    View._menu_scene.tkraise()
    

class View(tk.Tk):
    '''
    Classe qui gère la création de la fenêtre ainsi que les transitions entre les différentes scènes UI (entre le menu de 
    séléction, le jeu, et le menu de victoire
    '''
    _menu_scene = None
    _game_scene = None
    _end_game_scene = None
    
    def __init__(self):
        #Création de la fenêtre
        tk.Tk.__init__(self)
        
        #scale de la fenêtre en fonction de la taille de l'écran de l'utilisateur
        width_value = self.winfo_screenwidth()
        height_value = self.winfo_screenheight()
        self.geometry("%dx%d+0+0" % (width_value, height_value))
        
        #Création des différentes scènes
        View._menu_scene = MenuScene(self)
        View._game_scene = GameScene(self)
        View._end_game_scene = EndGameScene(self)
        
        for f in (View._menu_scene, View._game_scene, View._end_game_scene):
            f.initbuttons()
        display_menu_scene()
        self._menu_scene.button.tkraise()
        self.mainloop()
            



class MenuScene(tk.Frame):
    '''
    Classe responsable de l'affichage du menu
    '''


    def __init__(self, parent):
        '''
        Constructor
        '''
        tk.Frame.__init__(self, parent, bg = 'green')
        self.place(relwidth = 1, relheight = 1)
        self.parent = parent
        self.button = None

    def initbuttons(self):
        self.button=tk.Button(self.parent, command = display_game_scene(),text = "bite")
        self.button.pack()
        self.button.tkraise()
       
        

        
class GameScene(tk.Frame):
    '''
    Cette classe contient les éléments UI du jeu
    '''


    def __init__(self, parent):
        '''
        Constructor
        '''
        tk.Frame.__init__(self, parent, bg = 'blue')
        self.place(relwidth = 1, relheight = 1)
        self.parent= parent
        
        
    def initbuttons(self):
        self.button=tk.Button(self.parent, command = display_menu_scene(),text = "bite")
        self.button.pack()


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
        self.parent = parent
        
    def initbuttons(self):
        self.button=tk.Button(self.parent, command = display_menu_scene(), text = "bite")
        self.button.pack()
        
test = View()

# -*- coding: utf-8 -*-
'''
Created on 26 oct. 2020

@author: Antoine
'''
import tkinter as tk
import src.controller.controller as controller
import abc
from abc import abstractmethod
    

class View(tk.Tk):
    '''
    Classe qui gère la création de la fenêtre ainsi que les transitions entre les différentes scènes UI (entre le menu de 
    séléction, le jeu, et le menu de victoire
    '''
    _scenes = None
    
    def __init__(self):
        #Création de la fenêtre
        tk.Tk.__init__(self)
        
        #scale de la fenêtre en fonction de la taille de l'écran de l'utilisateur
        width_value = self.winfo_screenwidth()
        height_value = self.winfo_screenheight()
        self.geometry("%dx%d+0+0" % (width_value, height_value))
        
        #Création d'un container pour les différentes scènes
        container = tk.Frame(self)
        container.place(relwidth = 1, relheight = 1)
        
        #Création des différentes scènes
        menu_scene = MenuScene(self, container)
        game_scene = GameScene(self, container)
        end_game_scene = EndGameScene(self, container)
        
        View._scenes = {"Menu scene":menu_scene, "Game scene":game_scene, 
                       "End game scene":end_game_scene}
        
        self.display_scene("Menu scene")
        
        self.mainloop()
            
    def display_scene(self, scene_name):
        View._scenes[scene_name].display()



class Scene(tk.Frame, metaclass = abc.ABCMeta):
    """
    Abstract class qui permet la création des différentes scènes (menu, game, end game, end round)
    """
    
    def __init__(self, parent, color):
        tk.Frame.__init__(self, parent, bg = color)
        self.place(relwidth = 1, relheight = 1)
    
    @abstractmethod
    def display(self):
        pass
    

class MenuScene(Scene):
    '''
    Classe responsable de l'affichage du menu
    '''

    def __init__(self, view, parent):
        '''
        Constructor
        '''

        #Création scène        
        Scene.__init__(self, parent, 'green')
        
        #Création bouton transition
        button = tk.Button(self, text = "test", command = lambda:controller.display_scene(view, "Game scene"))
        button.pack()
    
    def display(self):
        self.tkraise()
       
        

        
class GameScene(Scene):
    '''
    Cette classe contient les éléments UI du jeu
    '''
    
    def __init__(self, view, parent):
        '''
        Constructor
        '''
        #Création de la scène
        Scene.__init__(self, parent, 'blue')
        
        #Création du bouton transition
        button=tk.Button(self,text = "encorebite", command = lambda:controller.display_scene(view, "End game scene"))
        button.pack()
        
    def display(self):
        self.tkraise()


class EndGameScene(Scene):
    '''
    Classe s'occupant de l'affichage du menu de fin
    '''
    def __str__(self):
        return "End game scene"


    def __init__(self, view, parent):
        '''
        Constructor
        '''
        
        #Création de la scène
        Scene.__init__(self, parent, 'cyan')
        
        #Texte de victoire
        self.label_text = tk.StringVar()
        self.label = tk.Label(self, text = "")
        self.label.pack()
        
        #Bouton pour revenir au menu
        button = tk.Button(self, text = "Retour au menu", command = lambda:controller.display_scene(view, "Menu scene"))
        button.pack()
        
    #Fonction qui permet l'affichage du vainqueur
    def update_text(self, winner_name):
        self.label_text = winner_name + "a gagné la manche !"
    
    
    def display(self):
        self.tkraise()

        
test = View()

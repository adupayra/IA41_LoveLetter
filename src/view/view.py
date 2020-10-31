# -*- coding: utf-8 -*-
'''
Created on 26 oct. 2020

@author: Antoine
'''
import tkinter as tk
import src.controller.controller as controller
import abc
from abc import abstractmethod
import os

    

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
        self.geometry("%dx%d+0+0" % (500, 500)) #Remplacer par les deux variables du dessus pour fullscreen
        
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
        
        #Création label titre
        titre = tk.Label(self, text = "Love Letter", bg = 'green')
        titre.pack()
        
        #Création bouton transition
        start_button = tk.Button(self, text = "Start Game", command = lambda:controller.display_scene(view, "Game scene"))
        start_button.pack()
    
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
        
        
        #Création du bouton transition test
        button=tk.Button(self,text = "Go to end game scene", command = lambda:controller.victory_test(view))
        button.place(relx = 0, rely = 0)
               
        #Création des boutons de jeu
        HEIGHT = 10
        WIDTH = 10
        
        ia_button1 = tk.Button(self, text = "", height = HEIGHT, width = WIDTH)
        ia_button1.place(rely = 0, relx = 0.5)
        ia_button1.config(state = "disabled")
        
        ia_button2 = tk.Button(self, text = "", height = HEIGHT, width = WIDTH)
        ia_button2.place(rely = 0, relx = 0.5, x = ia_button1.winfo_reqwidth())
        ia_button2.config(state = "disabled")
        
        self._player_button1 = tk.Button(self, text = "", command = lambda:controller.card_played(0), height = HEIGHT, width = WIDTH)
        self._player_button1.place(rely = 1, relx = 0.5, y = -self._player_button1.winfo_reqheight())
        
        self._player_button2 = tk.Button(self, text = "", command = lambda:controller.card_played(1),height = HEIGHT, width = WIDTH)
        self._player_button2.place(rely = 1, relx = 0.5, x = self._player_button1.winfo_reqwidth(), y = -self._player_button1.winfo_reqheight())
        
        #Changement du répertoire courant afin de se trouver dans le répertoire où se trouvent les ressources
        path_ressources = os.path.dirname(os.path.abspath(__file__))
        os.chdir(path_ressources)
        os.chdir(os.pardir)
        os.chdir(os.pardir)
        os.chdir("resources")
        
        #Création des différentes images des cartes
        self._images = {"Espionne":tk.PhotoImage(file = "Espionne.png"), "Garde":tk.PhotoImage(file = "Garde.png"),
                        "Pretre":tk.PhotoImage(file = "Pretre.png"),"Baron":tk.PhotoImage(file = "Baron.png"), "Servante":tk.PhotoImage(file = "Servante.png"),
                        "Prince":tk.PhotoImage(file = "Prince.png"), "Chancelier":tk.PhotoImage(file = "Chancelier.png"), "Roi":tk.PhotoImage(file = "Roi.png"),
                        "Comtesse":tk.PhotoImage(file = "Comtesse.png")}
        
    
    @property
    def images(self):
        return self._images
    
    def display(self):
        self.tkraise()
        controller.start_turn()
        #self.update_buttons(sprite1, sprite2)
    
    def update_buttons(self):
        pass
        
        
        
class EndGameScene(Scene):
    '''
    Classe s'occupant de l'affichage du menu de fin (fin de round et fin de partie)
    '''

    def __init__(self, view, parent):
        '''
        Constructor
        '''
        
        #Création de la scène
        Scene.__init__(self, parent, 'cyan')
        
        #Texte de victoire
        self._label_victory = tk.Label(self, text = "", bg = 'cyan')
        self._label_victory.pack()
        
        #Score label et texte
        self._label_score = tk.Label(self, text = "", bg = 'cyan')
        self._label_score.pack()
        
        
        #Bouton pour revenir au menu/aller au prochain round
        retour_menu_button = tk.Button(self, text = "Retour au menu", 
                                       command = lambda:controller.display_scene(view, "Menu scene"))
        self._next_round_button = tk.Button(self, text = "Prochain round", 
                                      command = lambda:controller.display_scene(view, "Game scene"))
        retour_menu_button.pack()
        self._next_round_button.pack()
        
    #Fonction qui permet l'affichage du vainqueur
    def victory_screen(self, winner_name, score):
        self.display()
         #Dissociation des cas entre fin de round et fin de partie
        if score[0] == 6 or score[1] == 6:
            self._label_victory['text'] = winner_name + " a gagné la partie !"
            self._next_round_button.pack_forget() #Désactivation du bouton next round si fin de partie
        else:
            self._label_victory['text'] = winner_name + " a gagné le round !"
        
        self._label_score['text'] = "Joueur : " + str(score[0]) + "points\nIA : " + str(score[1]) + " points"
        
    def display(self):
        self.tkraise()

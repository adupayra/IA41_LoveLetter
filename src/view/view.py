# -*- coding: utf-8 -*-
'''
Created on 26 oct. 2020

@author: Antoine
'''
import tkinter as tk
import tkinter.font
import src.controller.controller as controller
import abc
from abc import abstractmethod
import os

    

class View(tk.Tk):
    '''
    Classe qui gère la création de la fenêtre ainsi que les transitions entre les différentes scènes UI (entre le menu de 
    séléction, le jeu, et le menu de victoire
    '''
    
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
        
        self._scenes = {"Menu scene":menu_scene, "Game scene":game_scene, 
                       "End game scene":end_game_scene}
        
        self.display_scene("Menu scene")
        
        self.mainloop()
            
    def display_scene(self, scene_name):
        self._scenes[scene_name].display()
        
    @property
    def scenes(self):
        return self._scenes

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
        theme1 = "dark goldenrod1"
        theme2 = "red3"
        button_font = tk.font.Font(family = "Times", size = "20")
        
        #Création scène        
        Scene.__init__(self, parent, theme1)
        
        #Création label titre
        titre = tk.Label(self, text = "Love Letters", font = tk.font.Font(family = "Times", size = "35", weight = "bold", slant = "italic"),
                         bg = theme1, fg = theme2, pady = 25)
        titre.pack(side = tk.TOP, fill = tk.BOTH)
        
        #Création bouton transition
        start_button = tk.Button(self, text = "Commencer partie", command = lambda:controller.start_game(view), pady = 75, bg = theme2, fg = theme1,
                                 relief = tk.RIDGE, font = button_font)
        start_button.pack(side = tk.TOP, fill = tk.BOTH)
        
        #Bouton renvoyant vers l'URL des règles
        rules_button = tk.Button(self, text = "Règles", command = lambda:controller.consulter_regles(), pady = 75, bg = theme2, fg = theme1,
                                 relief = tk.RIDGE, font = button_font)
        rules_button.pack(side = tk.TOP, fill = tk.BOTH)
        
        #Bouton pour quitter le jeu
        exit_button = tk.Button(self, text = "Quitter", command = lambda:controller.quitter_jeu(), pady = 75, bg = theme2, fg = theme1,
                                relief = tk.RIDGE, font = button_font)
        exit_button.pack(side = tk.TOP, fill = tk.BOTH)
    
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
        Scene.__init__(self, parent, 'red3')
        
        #Création du bouton transition test
        button=tk.Button(self,text = "Go to end game scene", command = lambda:controller.victory_test(view))
        button.place(relx = 0, rely = 0)
               
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
                        "Comtesse":tk.PhotoImage(file = "Comtesse.png")} #Carte face cachée et princesse à ajouter
        
        #Boutons correspondant à l'affichage du jeu de l'IA (purement visuel)
        self._ia_buttons = []
        self._ia_buttons.append(tk.Button(self, image = self._images["Comtesse"]))
        self._ia_buttons[0].place(rely = 0, relx = 0.5, x = -self._ia_buttons[0].winfo_reqwidth())
        self._ia_buttons[0].config(state = "disabled")
        
        
        #Boutons de l'utilisateur, servent à choisir la carte à jouer
        self._player_buttons = []
        self._player_buttons.append(tk.Button(self, command = lambda:controller.card_played(0)))
        self._player_buttons[0].place(rely = 1, relx = 0.5, x = -self._ia_buttons[0].winfo_reqwidth(), y = -self._ia_buttons[0].winfo_reqheight())
        
        
        #self._player_buttons[1].place(rely = 1, relx = 0.5, y = -self._player_buttons[0].winfo_reqheight())
        
        """       
        Milieu de plateau : container permettant d'afficher les widgets plus facilement, les 3 cartes du début de partie, et la pioche
        """
        #Création du container
        container = tk.Frame(self, bg = 'white')
        container.place(relx = 0.2, rely = 0.325, relwidth = 0.6, relheight = 0.35)
        
        #Création des boutons sur lesquels on va afficher les images
        self._boutons_milieux = (tk.Button(container), tk.Button(container), tk.Button(container), tk.Button(container, image = self._images["Comtesse"]))
        self._boutons_milieux[0].pack(side = tk.LEFT)
        self._boutons_milieux[1].pack(side = tk.LEFT)
        self._boutons_milieux[2].pack(side = tk.LEFT)
        self._boutons_milieux[3].pack(side = tk.RIGHT)
        for bouton in self._boutons_milieux:
            bouton.config(state = "disabled")

        
    @property
    def images(self):
        return self._images
    
    def display(self):
        self.tkraise()
    
    def init_round(self, three_cards, player_cards):
        #Ajout des 3 cartes montrées au début du jeu
        self.add_three_middlecards(three_cards)
        
        #Ajout des images correspondant aux cartes du joueur
        self.update_player_buttons(player_cards)
        
    def add_three_middlecards(self, cards):
        for i in range(0,3):
            self._boutons_milieux[i].config(image = self._images[cards[i]])
            
    def update_player_buttons(self, cards):
        for i in range(0,cards.__len__()):
            self._player_buttons[i].config(image = self._images[cards[i]])
        
        
        
        
class EndGameScene(Scene):
    '''
    Classe s'occupant de l'affichage du menu de fin (fin de round et fin de partie)
    '''

    def __init__(self, view, parent):
        '''
        Constructor
        '''
        theme1 = "peach puff"
        theme2 = "white"
        text_font = tk.font.Font(family = "Courier", size = "30")
        #Création de la scène
        Scene.__init__(self, parent, theme1)
        
        #Texte de victoire
        self._label_victory = tk.Label(self, text = "", bg = theme1, fg = theme2, font = text_font)
        self._label_victory.pack()
        
        #Score label et texte
        self._label_score = tk.Label(self, text = "", bg = theme1, fg = theme2, font = text_font)
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

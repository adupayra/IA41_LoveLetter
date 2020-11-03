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
        ''''
        width_value = self.winfo_screenwidth()
        height_value = self.winfo_screenheight()
        self.geometry("%dx%d+0+0" % (width_value, height_value)) #Remplacer par les deux variables du dessus pour fullscreen
        '''
        #Fullscreen
        self.attributes('-fullscreen', True)
        
        #Titre
        self.title("Love Letters")
        
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
        start_button = tk.Button(self, text = "Commencer partie", command = lambda:self.display_difficulty_choice(view), pady = 75, bg = theme2, fg = theme1,
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
        
        
        
    def display_difficulty_choice(self, view):
        '''
        choix de difficulté
        '''
        #Création fenetre
        difficulty_window = tk.Toplevel()
        difficulty_window.title("Choix difficulté")
        var = tk.IntVar()
        radio1 = tk.Radiobutton(difficulty_window, text = "Facile", value = 0, 
                                variable = var)
        radio2 = tk.Radiobutton(difficulty_window, text = "Intermédiare", value = 1, 
                                variable = var)
        radio3 = tk.Radiobutton(difficulty_window, text = "Difficile", value = 2, 
                                variable = var)
        radio1.pack(anchor = tk.W)
        radio2.pack(anchor = tk.W)
        radio3.pack(anchor = tk.W)
        validate = tk.Button(difficulty_window, text = "OK", command =lambda:self.validate(difficulty_window, view, var.get()))
        validate.pack(anchor = tk.SE)
    
    def validate(self, window, view, difficulty):
        window.destroy()
        controller.start_game(view, difficulty)
        
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
        #Color themes
        theme1 = 'red4'
        theme2 = 'brown4'
        
        #Création de la scène
        Scene.__init__(self, parent, theme1)
        
        self.init_features(view)
               
        self.change_dir_resources()
        
        #Création des différentes images des cartes
        self._images = {"Espionne":tk.PhotoImage(file = "Espionne.png"), "Garde":tk.PhotoImage(file = "Garde.png"),
                        "Pretre":tk.PhotoImage(file = "Pretre.png"),"Baron":tk.PhotoImage(file = "Baron.png"), "Servante":tk.PhotoImage(file = "Servante.png"),
                        "Prince":tk.PhotoImage(file = "Prince.png"), "Chancelier":tk.PhotoImage(file = "Chancelier.png"), "Roi":tk.PhotoImage(file = "Roi.png"),
                        "Comtesse":tk.PhotoImage(file = "Comtesse.png"), "Princesse":tk.PhotoImage(file = "Princesse.png"), "Cache":tk.PhotoImage(file="Cache.png")} #Carte face cachée et princesse à ajouter
        
        self.init_playersUI(view, theme1)
        
        
        self.init_middleboard(theme2)
    
    
    '''_________________FONCTIONS DINSTANTIATION DES ELEMENTS UI_____________'''
    #Initialise les éléments UI de feature
    def init_features(self, view):
        
        #Création du bouton transition test
        button = tk.Button(self, text="Go to end game scene", command=lambda:controller.victory_test(view))
        button.place(relx=0, rely=0)
        
        #Création d'un bouton quittant l'application
        button_quit = tk.Button(self, text="Quit game", command=lambda:controller.quitter_jeu())
        button_quit.place(relx=0, rely=1, y=-button_quit.winfo_reqheight())
        
        #Création du label affichant les informations de jeu
        self._info_label = tk.Label(self, text="Idle")
        self._info_label.place(rely=0.5)

    #Changement du répertoire courant afin de se trouver dans le répertoire où se trouvent les ressources
    def change_dir_resources(self):
        
        path_ressources = os.path.dirname(os.path.abspath(__file__))
        os.chdir(path_ressources)
        os.chdir(os.pardir)
        os.chdir(os.pardir)
        os.chdir("resources")

    #Initialisation des éléments UI du joueur et de l'IA
    def init_playersUI(self, view, theme1):
        #Boutons correspondant à l'affichage du jeu de l'IA (purement visuel)
        self._ia_labels = (tk.Label(self, image=self._images["Cache"], borderwidth=0, highlightthickness=0), 
                           tk.Label(self, image="", borderwidth=0, highlightthickness=0, bg=theme1), 
                           tk.Label(self, image="", borderwidth=0, highlightthickness=0, bg=theme1))
        self._ia_labels[0].place(rely=0, relx=0.5, x=-self._ia_labels[0].winfo_reqwidth())
        
        #Boutons de l'utilisateur, servent à choisir la carte à jouer
        self._player_buttons = (tk.Button(self, command=lambda:controller.card_played(view, 0), borderwidth=0, highlightthickness=0),
                                tk.Button(self, command=lambda:controller.card_played(view, 1), borderwidth=0, highlightthickness=0),
                                tk.Button(self, command=lambda:controller.card_played(view, 2), borderwidth=0, highlightthickness=0))
        #Le 3e bouton est là pour couvrir le cas du chancelier
        
        self._player_buttons[0].place(rely=1, relx=0.5, x=-self._ia_labels[0].winfo_reqwidth(), y=-self._ia_labels[0].winfo_reqheight())



    def init_middleboard(self, theme2):
        """       
        
        Milieu de plateau : container permettant d'afficher les widgets plus facilement, les 3 cartes du début de partie, et la pioche
        
        """
        #Création du container
        container = tk.Frame(self, bg=theme2, highlightbackground='dark goldenrod1', highlightthickness=3)
        container.place(relx=0.2, rely=0.325, relwidth=0.6, relheight=0.35)
        
        #Création des Labels sur lesquels on va afficher les images
        espace = tk.Label(container, text=" ", bg=theme2).pack(side=tk.LEFT) #Pas d'intérêt, sert à avoir un affichage plus joli
        self._label_milieux = (tk.Label(container, borderwidth=0, highlightthickness=0), 
                               tk.Label(container, borderwidth=0, highlightthickness=0), 
                               tk.Label(container, borderwidth=0, highlightthickness=0), 
                               tk.Label(container, image=self._images["Cache"], borderwidth=0, highlightthickness=0))
        self._label_milieux[0].pack(side=tk.LEFT)
        self._label_milieux[1].pack(side=tk.LEFT)
        self._label_milieux[2].pack(side=tk.LEFT)
        espace = tk.Label(container, text=" ", bg=theme2).pack(side=tk.RIGHT) #Pas d'intérêt, sert à avoir un affichage plus joli
        self._label_milieux[3].pack(side=tk.RIGHT)

    '''______________________FIN DES FONCTIONS DINSTANCIATION DES ELEMENTS UI___________'''
        
    @property
    def images(self):
        return self._images
    
    def display(self):
        self.tkraise()
    
    #Fonction appelée en début de round : elle affiche les 3 cartes montrées en début de jeu
    def init_round(self, three_cards, string_joueur):
        for i in range(0,3):
            self._label_milieux[i].config(image = self._images[three_cards[i]])
        
        self._info_label['text'] = "c'est à " + string_joueur + " de commencer !" #Affiche le joueur qui commence
             
    #Fonction permettant l'actualisation de l'UI en fonction des cartes du joueur
    def update_playerUI(self, cards):
        number_cards_displayed = sum(button.winfo_ismapped() for button in self._player_buttons) #Compte le nombre de boutons de l'utilisateurs
        number_cards_todisplay = cards.__len__() #Nombre de cartes à afficher

        #Disjonction de cas entre les cas où il y a plus de cartes à afficher que de boutons disponibles et les cas où il y a trop de boutons
        #disponibles à l'écran pour le nombre de cartes à afficher
        if(number_cards_todisplay >= number_cards_displayed ):
            #Dans ce cas, on update les cartes sur les boutons déjà disponibles
            for i in range(0,number_cards_displayed):
                self._player_buttons[i].config(image = self._images[cards[i]])
            
            #Puis affiche le nombre de boutons nécessaires afin d'afficher toutes les cartes
            for i in range(number_cards_displayed, number_cards_todisplay):
                self._player_buttons[i].config(image = self._images[cards[i]])
                self._player_buttons[i].place(rely = 1, relx = 0.5, x = (i-1) * self._ia_labels[0].winfo_reqwidth(), y = -self._ia_labels[0].winfo_reqheight())
                
                
        elif(number_cards_displayed > number_cards_todisplay):
            #Actualisation des boutons dont on a besoin
            for i in range(0, number_cards_todisplay):
                self._player_buttons[i].config(image = self._images[cards[i]])
            #On retire les boutons dont on n'a plus besoin
            for i in range(number_cards_todisplay, number_cards_displayed):
                self._player_buttons[i].place_forget()
        
    #Fonction permettant l'actualisation de l'UI en fonction du nombre de cartes de l'IA (meme principe que l'update player)
    def update_iaUI(self, nbcards):
        number_cards_displayed = sum(label["image"] != "" for label in self._ia_labels)

        if(nbcards > number_cards_displayed):
            for i in range(number_cards_displayed, nbcards):
                self._ia_labels[i]['image'] = self._images["Cache"]
                self._ia_labels[i].place(relx = 0.5, x = (i-1) * self._ia_labels[0].winfo_reqwidth())
        elif(number_cards_displayed > nbcards):
            for i in range(nbcards, number_cards_displayed):
                self._ia_labels[i].config(image = "")

    def update_infolabel(self, joueur, action):
        self._info_label['text'] = joueur + " a joué la carte " + action
        
    #Label permettant de vérouiller les boutons lorsque l'IA joue        
    def lock_buttons(self):
        for button in self._player_buttons:
            button.config(state = 'disabled')
    
    def unlock_buttons(self):
        for button in self._player_buttons:
            button.config(state = 'normal')
        
        
        
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
                                      command = lambda:controller.start_game(view, -1))
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

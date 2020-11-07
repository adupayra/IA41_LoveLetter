# -*- coding: utf-8 -*-
'''
Created on 26 oct. 2020

@author: Antoine
'''
import tkinter as tk
import tkinter.font
from src.controller.controller import Controller
import os
from math import floor
from tkinter.constants import BOTH
from prompt_toolkit.application import current

    

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
        
        Controller.addgamescene(game_scene)
        
        self.mainloop()
            
    def display_scene(self, scene_name):
        self._scenes[scene_name].tkraise()
        
    @property
    def game_scene(self):
        return self._game_scene
    
    @property
    def scenes(self):
        return self._scenes


class MenuScene(tk.Frame):
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
        tk.Frame.__init__(self, parent, bg = theme1)
        self.place(relwidth = 1, relheight = 1)
        
        #Création label titre
        titre = tk.Label(self, text = "Love Letters", font = tk.font.Font(family = "Times", size = "35", weight = "bold", slant = "italic"),
                         bg = theme1, fg = theme2, pady = 25)
        titre.pack(side = tk.TOP, fill = tk.BOTH)
        
        #Création bouton transition
        start_button = tk.Button(self, text = "Commencer partie", command = lambda:self.display_difficulty_choice(view), pady = 75, bg = theme2, fg = theme1,
                                 relief = tk.RIDGE, font = button_font)
        start_button.pack(side = tk.TOP, fill = tk.BOTH)
        
        #Bouton renvoyant vers l'URL des règles
        rules_button = tk.Button(self, text = "Règles", command = lambda:Controller.consulter_regles(), pady = 75, bg = theme2, fg = theme1,
                                 relief = tk.RIDGE, font = button_font)
        rules_button.pack(side = tk.TOP, fill = tk.BOTH)
        
        #Bouton pour quitter le jeu
        exit_button = tk.Button(self, text = "Quitter", command = lambda:Controller.quitter_jeu(), pady = 75, bg = theme2, fg = theme1,
                                relief = tk.RIDGE, font = button_font)
        exit_button.pack(side = tk.TOP, fill = tk.BOTH)
        
        
        
    def display_difficulty_choice(self, view):
        '''
        choix de difficulté
        '''
        #Création fenetre
        
        difficulty_window = tk.Toplevel()
        difficulty_window.title("Choix difficulté")
        
        #Création des radio buttons
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
        #Destruction de la seconde fenetre
        window.destroy()
        
        #Démarrage de la partie
        Controller.start_game(view, difficulty)

    
        
class GameScene(tk.Frame):
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
        
        #Font
        text_font = tk.font.Font(family = "Times", size = "14", weight = "bold")
        
        self._view = view
        
        self.change_dir_resources()
        
        #Création des différentes images des cartes
        self._images = {"Espionne":tk.PhotoImage(file = "Espionne.png"), "Garde":tk.PhotoImage(file = "Garde.png"),
                        "Pretre":tk.PhotoImage(file = "Pretre.png"),"Baron":tk.PhotoImage(file = "Baron.png"), "Servante":tk.PhotoImage(file = "Servante.png"),
                        "Prince":tk.PhotoImage(file = "Prince.png"), "Chancelier":tk.PhotoImage(file = "Chancelier.png"), "Roi":tk.PhotoImage(file = "Roi.png"),
                        "Comtesse":tk.PhotoImage(file = "Comtesse.png"), "Princesse":tk.PhotoImage(file = "Princesse.png"), "Cache":tk.PhotoImage(file="Cache.png")} #Carte face cachée et princesse à ajouter
        
        
        #Création de la scène
        tk.Frame.__init__(self, parent, bg = theme1)
        self.place(relwidth = 1, relheight = 1)
        
        self.init_features(view, theme1, parent,text_font)
        
        self.init_playersUI(theme1)

        self.init_middleboard(theme2)
    
    
    '''_________________FONCTIONS DINSTANTIATION DES ELEMENTS UI_____________'''
        
    #Initialise les éléments UI de feature
    def init_features(self, view, theme1, container, text_font):
        theme = 'goldenrod'
        
        #Création du bouton transition test
        button = tk.Button(self, text="Go to end game scene", command=lambda:Controller.victory_test(view))
        button.place(relx=0, rely=0)
        
        #Container du quit button
        quit_frame = tk.Frame(self, bg = theme1, highlightthickness = 3, highlightbackground = theme)
        
        #Création d'un bouton quittant l'application
        button_quit = tk.Button(quit_frame, text="Quit game", command=lambda:Controller.quitter_jeu(), font = text_font, bg = theme1, fg = theme)
        quit_frame.place(relx = 0, rely = 1, y =-button_quit.winfo_reqheight() - 5)
        button_quit.pack()
        
        #Création du label affichant les informations de jeu
        self._info_label = tk.Label(self, text="Idle", font = text_font, fg = theme, bg = theme1)
        self._info_label.place(rely=0.325)
        
        #Création du label montrant la dernière carte jouée
        self._last_card_label = tk.Label(self, bg = theme1, image = self._images["Cache"])
        self._last_card_label.place(rely = 0.325, y = self._info_label.winfo_reqheight())
        
        #Création du label écrivant les détails de la dernière action du jeu
        self._details_label = tk.Label(self, bg = theme1, fg = theme)
        self._details_label.place(rely = 0.4, y = self._last_card_label.winfo_reqheight())
        
        #Création de la frame s'affichant par dessus la scène de jeu lorsque l'utilisateur veut consulter les cartes ou encore
        #qu'il doit faire un choix entre plusieurs options (après avoir joué le prince ou le garde)
        self._special_frame = SpecialFrame(container, theme1, self)
        
        #Container des feature buttons
        container_features = tk.Frame(self, bg = theme1, highlightthickness = 3, highlightbackground = theme)
        container_features.pack(side = tk.RIGHT)
        
        #Bouton permettant d'afficher la liste des cartes du jeu
        boutton_reminder = tk.Button(container_features, command = lambda:self._special_frame.display_reminder(), text = "Rappel des cartes",
                                     bg = theme1, fg = theme, font = text_font)
        boutton_reminder.pack(fill = tk.BOTH)
        
        #Bouton permettant d'afficher toutes les cartes jouées 
        boutton_played_cards = tk.Button(container_features, text = "Consulter cartes jouées", command = lambda:Controller.display_played_cards(self._special_frame),
                                         bg = theme1, fg = theme, font = text_font)
        boutton_played_cards.pack()

    #Changement du répertoire courant afin de se trouver dans le répertoire où se trouvent les ressources
    def change_dir_resources(self):
        
        path_ressources = os.path.dirname(os.path.abspath(__file__))
        os.chdir(path_ressources)
        os.chdir(os.pardir)
        os.chdir(os.pardir)
        os.chdir("resources")

    #Initialisation des éléments UI du joueur et de l'IA
    def init_playersUI(self, theme1):
        #Boutons correspondant à l'affichage du jeu de l'IA (purement visuel)
        self._ia_labels = (tk.Label(self, image=self._images["Cache"], borderwidth=0, highlightthickness=0), 
                           tk.Label(self, image="", borderwidth=0, highlightthickness=0, bg=theme1), 
                           tk.Label(self, image="", borderwidth=0, highlightthickness=0, bg=theme1))
        self._ia_labels[0].place(rely=0, relx=0.5, x=-self._ia_labels[0].winfo_reqwidth())
        
        #Boutons de l'utilisateur, servent à choisir la carte à jouer
        self._player_buttons = (tk.Button(self, command=lambda:Controller.card_played(self, 0), borderwidth=0, highlightthickness=0),
                                tk.Button(self, command=lambda:Controller.card_played(self, 1), borderwidth=0, highlightthickness=0),
                                tk.Button(self, command=lambda:Controller.card_played(self, 2), borderwidth=0, highlightthickness=0))
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
    
    @property
    def view(self):
        return self._view
        
    
    
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
        
        self._ia_labels[0]['image'] = self.images["Cache"] #Sécurité car de toutes facons l'ia aura forcément une carte en main
        
        if(nbcards > number_cards_displayed):
            for i in range(number_cards_displayed, nbcards):
                self._ia_labels[i]['image'] = self._images["Cache"]
                self._ia_labels[i].place(relx = 0.5, x = (i-1) * self._ia_labels[0].winfo_reqwidth())
        elif(number_cards_displayed > nbcards):
            for i in range(nbcards, number_cards_displayed):
                self._ia_labels[i].config(image = "")

    def update_lastcardslabels(self, joueur, card):
        self._info_label['text'] = joueur + " a joué la carte " + card
        self._last_card_label['image'] = self._images[card]
        
    def update_details_label(self, text):
        self._details_label['text'] = text

    #Fonction permettant de vérouiller les boutons lorsque l'IA joue        
    def lock_buttons(self):
        for button in self._player_buttons:
            button.config(state = 'disabled')
    
    #Fonction permettant de les déverouiller
    def unlock_buttons(self):
        for button in self._player_buttons:
            button.config(state = 'normal')
    
    
        
    #Fonction permettant l'affichage de la fenêtre permettant à l'utilisateur de choisir quelle carte deviner (lorsqu'il a joué
    #un garde
    def display_guard_choice(self):
        self._special_frame.display_guard_choice()
    
    #Pareil mais pour le prince
    def display_prince_choice(self, jeu_joueur, jeu_ia):
        self._special_frame.display_prince_choice(jeu_joueur, jeu_ia)
        
    def display_AI_card(self, card):
        self._ia_labels[0]['image'] = self._images[card]


    #Fonction utilisée pour replacer le premier bouton lorsqu'il est place forget
    def replace_button(self):
        self._player_buttons[0].place(rely=1, relx=0.5, x=-self._ia_labels[0].winfo_reqwidth(), y=-self._ia_labels[0].winfo_reqheight())
    
    def display_baron(self, player, ia):
        self._special_frame.display_baron_screen(player, ia)
        
    
    
class SpecialFrame(tk.Frame):
    '''
    Cette classe est un immondice, mais elle marche bien. Pas trop difficile à refaire, faire si on a le temps
    
    classe correspondant à l'affichage d'une nouvelle Frame par dessus la scène de jeu. Permet d'afficher des informations
    comme les cartes jouées ou permet à l'utilisateur de faire des choix lorsqu'il a joué certaines cartes (garde et prince)
    '''
    
    def __init__(self, parent, color, gamescene):
        #Création de la fenetre
        tk.Frame.__init__(self, parent, bg = color)
        
        #Configuration de la fenêtre et déclaration des différentes couleurs et fonts permettant d'avoir une interface plus belle
        self.grid_columnconfigure(0, weight = 1)
        self.grid_columnconfigure(1, weight = 1)
        self.grid_columnconfigure(2, weight = 1)
        theme2 = 'goldenrod'
        
        cards_played_font = tk.font.Font(family = "Times", size = "14")
        
        prince_buttons_color = 'brown4'
        prince_buttons_font = tk.font.Font(family = "Times", size = '30', weight = "bold")
        
        #instance de la gamescene
        self._gamescene = gamescene
        
        #Frame contenant le bouton leave feature
        self._leave_feature_frame = tk.Frame(self, bg = color, highlightbackground = theme2, highlightthickness = 3)
        
        #Bouton permettant de revenir au jeu
        _leave_feature = tk.Button(self._leave_feature_frame, text = "Retourner au jeu", command = lambda:self.stop_display(), font = cards_played_font,
                                        bg = color, fg = theme2)
        _leave_feature.pack()
        
        #Labels permettant d'afficher les cartes jouées ainsi que le rappel des cartes (21 pour 21 cartes au total)
        self._displayerslabels = []
        
        #Boutons permettant de deviner la carte de l'IA lorsque l'utilisateur a joué un garde
        self._actionbuttons = []
        
        #Instantiation des boutons et d'une partie des labels
        for i in range(0,9):
            self._actionbuttons.append(tk.Button(self))

            self._displayerslabels.append(tk.Label(self, bg = color))

        #Instantiation du reste des labels
        for i in range(9, 21):
            self._displayerslabels.append(tk.Label(self, bg = color))
        
        #Frame seulement utilisée de contenant pour les boutons (permet de mettre une bordure en couleur)
        self._prince_frames = (tk.Frame(self, bg = color, highlightbackground = theme2, highlightthickness = 3),
                               tk.Frame( self, bg = color, highlightbackground = theme2, highlightthickness = 3))
        
        #Instantiation des boutons sur lesquels l'utilisateur pourra appuyer pour choisir quel camp doit défausser sa carte
        prince_buttons = (tk.Button(self._prince_frames[0], text = "Votre jeu", command = lambda:Controller.side_chosen(self, prince_buttons[0]['text']), 
                                          bg = prince_buttons_color, highlightbackground = theme2, highlightthickness = 3,font = prince_buttons_font, fg = theme2),
                                tk.Button(self._prince_frames[1], text = "Le jeu adverse", command = lambda:Controller.side_chosen(self, prince_buttons[1]['text']),
                                          highlightbackground = theme2, highlightthickness = 3, bg = prince_buttons_color, font = prince_buttons_font, fg = theme2))
        prince_buttons[0].pack(expand = True, fill = tk.BOTH)
        prince_buttons[1].pack(expand = True, fill = tk.BOTH)
        
        #Labels de textes utilisés lors de l'affichage des cartes jouées
        self._side_labels = (tk.Label(self, text = "Cartes jouées par l'IA", bg = color, fg = theme2, font = cards_played_font),
                             tk.Label(self, text = "Cartes jouées par vous", bg = color,fg = theme2, font = cards_played_font),
                             tk.Label(self, text = "3 premières cartes", bg = color, fg = theme2, font = cards_played_font),
                             tk.Label(self, text = "Choisissez une carte", bg = color, fg = theme2, font = cards_played_font))
        
        #Copie utilisée pour garder en mémoire des widgets dans le cas où l'on veut afficher une autre fenêtre tout en voulant revenir sur l'ancienne
        self._copie = []
        
        #Contenant du bouton
        self._see_played_cards_frame_prince = tk.Frame(self, bg = color, highlightthickness = 3, highlightbackground = theme2)
        
        #Bouton permettant de voir les cartes jouées depuis une autre fenêtre que celle de la gamescene
        see_played_cards_prince = tk.Button(self._see_played_cards_frame_prince, text = "Voir cartes jouées", command = lambda:self.make_copy(), bg = prince_buttons_color, fg = theme2,
                                     font = prince_buttons_font)
        see_played_cards_prince.pack(expand = True, fill = tk.BOTH)
        
        #Contenant du bouton
        self._see_played_cards_frame_garde = tk.Frame(self, bg = color, highlightthickness = 3, highlightbackground = theme2)
        
        #Bouton
        see_played_cards_garde = tk.Button(self._see_played_cards_frame_garde,  text = "Voir cartes jouées", command = lambda:self.make_copy(), bg = prince_buttons_color,
                                           fg = theme2, font = cards_played_font)
        
        see_played_cards_garde.pack(expand = True, fill = tk.BOTH)
        
        #Label d'affichage de l'écran baron
        self._baron_label = tk.Label(self, text = "Un baron a été joué, comparaison de vos cartes : ", bg = color, font = cards_played_font, fg = theme2)
        
        #Contenant du bouton retour à la dernière frame
        self._return_last_frame_frame = tk.Frame(self, bg = color, highlightbackground = theme2, highlightthickness = 3)
        
        #Bouton permettant de revenir à la frame précédente
        return_last_frame = tk.Button(self._return_last_frame_frame, text = "Retour à la séléction", command = lambda:self.retour(), font = cards_played_font, bg = color,
                                            fg = theme2)
        return_last_frame.pack()
        
        #Error label, écran trop petit
        self._error_label = tk.Label(self, text = "Votre écran est trop piti, disoulé :(")
        
        #Attribution des images aux boutons de choix du garde
        self._actionbuttons[0]['image'] = self._gamescene.images['Espionne']
        self._actionbuttons[1]['image'] = self._gamescene.images['Pretre']
        self._actionbuttons[2]['image'] = self._gamescene.images['Baron']
        self._actionbuttons[3]['image'] = self._gamescene.images['Servante']
        self._actionbuttons[4]['image'] = self._gamescene.images['Prince']
        self._actionbuttons[5]['image'] = self._gamescene.images['Chancelier']
        self._actionbuttons[6]['image'] = self._gamescene.images['Roi']
        self._actionbuttons[7]['image'] = self._gamescene.images['Comtesse']
        self._actionbuttons[8]['image'] = self._gamescene.images['Princesse']
        
        #Association des évènements à déclencher en cas de click lorsque le garde est joué
        self._actionbuttons[0].configure(command = lambda:Controller.card_chosen(self, self.search_card(0)))
        self._actionbuttons[1].configure(command = lambda:Controller.card_chosen(self, self.search_card(1)))
        self._actionbuttons[2].configure(command = lambda:Controller.card_chosen(self, self.search_card(2)))
        self._actionbuttons[3].configure(command = lambda:Controller.card_chosen(self, self.search_card(3)))
        self._actionbuttons[4].configure(command = lambda:Controller.card_chosen(self, self.search_card(4)))
        self._actionbuttons[5].configure(command = lambda:Controller.card_chosen(self, self.search_card(5)))
        self._actionbuttons[6].configure(command = lambda:Controller.card_chosen(self, self.search_card(6)))
        self._actionbuttons[7].configure(command = lambda:Controller.card_chosen(self, self.search_card(7)))
        self._actionbuttons[8].configure(command = lambda:Controller.card_chosen(self, self.search_card(8)))
        
    
    #Permet de renvoyer la chaine de caractère correspondant au bouton cliqué par l'utilisateur
    def search_card(self, index):
        if(index == 0):
            return "Espionne"
        elif index == 1:
            return "Pretre"
        elif index == 2:
            return "Baron"
        elif index == 3:
            return "Servante"
        elif index == 4:
            return "Prince"
        elif index == 5:
            return "Chancelier"
        elif index == 6:
            return "Roi"
        elif index == 7:
            return "Comtesse"
        elif index == 8:
            return "Princesse"
    
    
        
    #Affiche toutes les cartes du jeu, il s'agit d'un rappel des différentes cartes au joueur
    def display_reminder(self):
        self.place(relwidth = 1, relheight = 1)
        self.tkraise()
        self._gamescene.place_forget()
        
        #Attribution des images aux labels
        self._displayerslabels[0]['image'] = self._gamescene.images['Espionne']
        self._displayerslabels[1]['image'] = self._gamescene.images['Garde']
        self._displayerslabels[2]['image'] = self._gamescene.images['Pretre']
        self._displayerslabels[3]['image'] = self._gamescene.images['Baron']
        self._displayerslabels[4]['image'] = self._gamescene.images['Servante']
        self._displayerslabels[5]['image'] = self._gamescene.images['Prince']
        self._displayerslabels[6]['image'] = self._gamescene.images['Chancelier']
        self._displayerslabels[7]['image'] = self._gamescene.images['Roi']
        self._displayerslabels[8]['image'] = self._gamescene.images['Comtesse']
        self._displayerslabels[9]['image'] = self._gamescene.images['Princesse']
        
        j= 0
        last_column = self.compute_last_column(0, self._displayerslabels[0].winfo_reqwidth())
        #On boucle sur la longueur du dictionnaire d'images (-1 à cause de l'image face cachée)
        for i in range(0, self._gamescene.images.__len__() - 1):
            #Condition permettant de retourner à la ligne lorsqu'il n'y a plus de place sur l'écran
            if(i != 0 and i%last_column == 0):
                j+=1
                
            #Affichage du label
            self._displayerslabels[i].grid(row = j, column = i%last_column)
        #Affichage du bouton retour au jeu
        self._leave_feature_frame.grid(row = j+1, column = i%last_column)
    
    
        
   
    #Affiche toutes les cartes ayant été jouées durant le round
    def display_allcards(self, ia_cards, player_cards, middle_cards, call_from_special = False):
        self.place(relwidth = 1, relheight = 1)
        self.tkraise()
        self._gamescene.place_forget()
        
        self.grid_columnconfigure(0, weight = 0)
        self.grid_columnconfigure(1, weight = 0)
        self.grid_columnconfigure(2, weight = 0)
        #Affichage des cartes utilisées de l'ia en prenant en compte la largeur de l'écran
        i = self.display_cards_side(ia_cards, 0, self._side_labels[0], 0, self._displayerslabels)
        j = 1
        
        #Affichage des cartes du milieux à la ligne suivante
        self._side_labels[2].grid(row = i, column=0)
        for p in range(ia_cards.__len__(), ia_cards.__len__() + 3):
            self._displayerslabels[p]['image'] = self._gamescene.images[str(middle_cards[j-1])]
            self._displayerslabels[p].grid(row = i, column = j)
            j+=1
        
        #Vérifie si la fonction est appelée via la gamescene ou via la specialframe
        if(call_from_special):
            self._return_last_frame_frame.grid(row = i, column = j) #Si la fonction est appelée de la specialframe, on affiche le boutton
                                                            #permettant de revenir à la specialframe précédente
        else:
            self._leave_feature_frame.grid(row = i, column = j) #Boutton faisant revenir à la gamescene
        i+=1
        
        #Affichage des cartes utilisées du joueur
        self.display_cards_side(player_cards, i, self._side_labels[1], ia_cards.__len__() + 4, self._displayerslabels)
     
     
    #Permet d'afficher les éléments UI de la spécial frame
    #Suivant la taille de l'écran, il peut y avoir des problèmes d'affichage en hauteur
    def display_cards_side(self, side, row, label, labelindex, widgets):
        #Affichage du label descriptif
        j=1
        label.grid(row = row, column = 0)
        
        label_index = labelindex
        
        #Détermination du nombre de cartes que l'on peut placer en largeur avant d'être hors de l'écran en largeur
        last_column = self.compute_last_column(widgets[0].winfo_reqwidth(), self._gamescene.images['Espionne'].width())
        
        #Affichage des cartes
        for p in range(0, side.__len__()):
            
            widgets[label_index].configure(image = self._gamescene.images[str(side[p])])
            widgets[label_index].grid(row = floor(j/(last_column+1)) + row, column = j%(last_column+1))
            label_index += 1
            j+=1
        if self.grid_slaves(row = 3, column = 0) :
            self.stop_display()
            self.display_err()
        return row + 1
    

        
    #Affichage des boutons permettant à l'utilisateur de choisir qui défausse sa carte
    def display_prince_choice(self, jeu_joueur, jeu_ia):
        self.place(relwidth = 1, relheight = 1)
        self.tkraise()
        self._gamescene.place_forget()
        
        self.grid_columnconfigure(0, weight = 1)
        self.grid_columnconfigure(1, weight = 1)
        self.grid_columnconfigure(2, weight = 1)
        
        self._prince_frames[0].winfo_children()[0]['text'] = jeu_joueur
        self._prince_frames[1].winfo_children()[0]['text'] = jeu_ia
        
        self._prince_frames[0].grid(sticky = 'nesw', columnspan = 10, ipady = 50)
        self._prince_frames[1].grid(sticky = 'nesw', columnspan = 10, ipady = 50)
        self._see_played_cards_frame_prince.grid(sticky = 'nesw', columnspan = 10, ipady = 50)
        
    #Affichage des possibilités de cartes que l'utilisateur peut deviner
    def display_guard_choice(self):
        self.place(relwidth = 1, relheight = 1)
        self.tkraise()
        self._gamescene.place_forget()
        
        self.display_cards_side(["Espionne", "Pretre", "Baron", "Servante", "Prince", "Chancelier", "Roi", "Comtesse", 
                                 "Princesse"], 0, self._side_labels[3], 0, self._actionbuttons)
        
        self._see_played_cards_frame_garde.grid()
        
    #Affiche l'écran lorsqu'un baron est joué
    def display_baron_screen(self, currentplayercard, othercard):
        self.place(relwidth = 1, relheight = 1)
        self.tkraise()
        self._gamescene.place_forget()
        
        self._baron_label.grid()
        self._displayerslabels[0]['image'] = self._gamescene.images[str(currentplayercard)]
        self._displayerslabels[1]['image'] = self._gamescene.images[str(othercard)]
        self._displayerslabels[0].grid()
        self._displayerslabels[1].grid()
        
        var = tk.IntVar()
        self.after(3000, var.set, 1)
        self.wait_variable(var)
        self.stop_display()
    #Enleve l'affichage de la frame, pour se faire, enleve l'affichage de tous les éléments qui se trouvent dans la frame,
    #puis enlève la frame
    def stop_display(self):

        for widget in self.winfo_children():
                widget.grid_forget() #"oubli" de ces éléments
        self.place_forget() #"oubli" de la frame
        
        self._gamescene.place(relwidth = 1, relheight = 1)
        
        #Quand on place forget la gamescene, ses boutons sont place forget avec, on doit donc re place le premier bouton du joueur
        self._gamescene.replace_button()
    
    #Permet de déterminer la colonne maximale pouvant rentrer sur l'écran.
    def compute_last_column(self, first_width, unite):
        sum_width = first_width
        last_column = 0
        while(sum_width + unite < self.winfo_screenwidth()):
            sum_width += unite
            last_column +=1
        return last_column
    
    #s'affiche quand il y a trop de cartes pour l'écran
    def display_err(self):
        self._error_label.grid(row = 0, column = 0)
        self._leave_feature_frame.grid(row = 1, column = 0)
        
    #Permet d'effectuer une copie des éléments affichés à l'écran lorsque l'on voudra les rafficher plus tard
    def make_copy(self):
        for x in self.winfo_children():
            if(x.winfo_ismapped()):
                self._copie.append(x)
                
        self.stop_display() #Afin d'afficher de nouveaux éléments, on refresh la frame
        Controller.display_played_cards(self, True) #Affichage des cartes jouées
        
    #Permet de revenir à la configuration de la special frame précédente
    def retour(self):
        self.stop_display() #Actualisation
        if(self._copie[0] is self._prince_frames[0]): #On cherche quelles informations étaient affichées
            Controller.display_prince_choice(self._copie[0].winfo_children()[0]['text'], self._copie[1].winfo_children()[0]['text'])
        else:
            Controller.display_guard_choice()
        self._copie = [] #On clear le buffer
        
class EndGameScene(tk.Frame):
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
        tk.Frame.__init__(self, parent, bg = theme1)
        self.place(relwidth = 1, relheight = 1)
        
        #Texte de victoire
        self._label_victory = tk.Label(self, text = "", bg = theme1, fg = theme2, font = text_font)
        self._label_victory.pack()
        
        #Score label et texte
        self._label_score = tk.Label(self, text = "", bg = theme1, fg = theme2, font = text_font)
        self._label_score.pack()
        
        
        #Bouton pour revenir au menu/aller au prochain round
        retour_menu_button = tk.Button(self, text = "Retour au menu", 
                                       command = lambda:Controller.display_scene(view, "Menu scene"))
        self._next_round_button = tk.Button(self, text = "Prochain round", 
                                      command = lambda:Controller.start_game(view, -1))
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

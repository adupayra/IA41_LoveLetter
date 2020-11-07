# -*- coding: utf-8 -*-
'''
Created on 26 oct. 2020

@author: Antoine
'''

import src.model.model as model
import webbrowser
import sys
import tkinter as tk


class Controller():
    #Ne pas appeler cette variable depuis un module de view afin de garder l'indépendance entre modèle et view    
    
    _modelvar = None
    _game_scene = None
    
    @classmethod
    def addgamescene(cls, game_scene):
        cls._game_scene = game_scene
        
    @classmethod
    def consulter_regles(cls):
        webbrowser.open('https://fr.wikipedia.org/wiki/Love_Letter_(jeu)')
        
    @classmethod
    def quitter_jeu(cls):
        sys.exit(0)
    
    @classmethod
    #Fonction appelée lorsque l'utilisateur lance une partie/finit une partie/retourne au menu
    def display_scene(cls, view, scene_name):
        view.display_scene(scene_name)
    
    @classmethod
    #Fonction lancée lorsque l'utilisateur à choisi la difficulté de la partie
    def start_game(cls, view, difficulty): #difficulty = -1 : nouveau round, difficulté != -1 : nouvelle partie
        current_player = cls._modelvar.init_data(difficulty)
    
        #Affichage du plateau de jeu
        cls.display_scene(view, "Game scene")
    
        #Affichage des 3 premieres cartes et du nom de la personne qui commence
        view.scenes["Game scene"].init_round(cls._modelvar.get_three_cards(), str(cls._modelvar.current_player))
        
        
        #Début du premier tour
        cls.start_turn(current_player, view.scenes["Game scene"])
        
        
    @classmethod
    #Fonction permettant le déroulement d'un tour
    def start_turn(cls, current_player, gamescene):
        
        #Actualisation de l'UI (nombre de cartes de l'IA)
        gamescene.update_iaUI(cls._modelvar.ia.cards.__len__())
        
        #Actualisation de l'UI du vrai joueur (nombre de cartes et images associées du joueur)
        gamescene.update_playerUI(cls._modelvar.player.cards_to_string)
        
        
        #Si le joueur actuel est l'IA, alors l'utilisateur ne peut pas jouer, et le process se fera sans UI, dans le modèle
        if(isinstance(current_player, model.player.IA)):
            
            #Vérification premier tour
            if(cls._modelvar.player.last_card_played is not None):
                
                gamescene.update_lastcardslabels(str(cls._modelvar.player), str(cls._modelvar.player.last_card_played)) #Affichage de la carte jouée par le joueur au dernier tour
            cls.card_playedAI(gamescene)
        else:
            if(cls._modelvar.ia.last_card_played is not None):
                gamescene.update_lastcardslabels(str(cls._modelvar.ia), str(cls._modelvar.ia.last_card_played)) #Affichage de la carte jouée par l'IA au dernier tour
            gamescene.unlock_buttons()
    
    @classmethod
    #L'IA joue une carte
    def card_playedAI(cls, gamescene):
        gamescene.lock_buttons()
        current_player = cls._modelvar.playAI()
        gamescene.view.after(3000, cls.start_turn, current_player, gamescene) #Attente de 3 secondes avant de passer au tour suivant

    @classmethod
    #Fonction appelée lorsqu'un joueur a choisi une carte
    def card_played(cls, gamescene, index):
        #if(not isinstance(cls._modelvar.current_player.last_card_played, model.cards.Chancelier)):
        
        
        #Action de la carte et changement de joueur courant
        current_player = cls._modelvar.play(index)
        
        #Nouveau tour
        cls.start_turn(current_player, gamescene)
    
    @classmethod
    #Prend dans le modèle les cartes ayant été jouées lors du round afin de les redonner à la view qui va les afficher
    def display_played_cards(cls, special_frame, call_from_special = False):
        special_frame.display_allcards(cls._modelvar.cards_played_ia, cls._modelvar.cards_played_player, cls._modelvar.get_three_cards(), call_from_special)
    
    #Si la carte est un garde et que c'est le tour de l'utilisateur, on va afficher une écran lui montrant quelles cartes il peut 
    #deviner
    @classmethod
    def display_guard_choice(cls):
        cls._game_scene.display_guard_choice()
        cls._game_scene.wait_visibility(cls._game_scene)
    
    #Si la carte est un prince, alors il pourra choisir le camp qui défausse sa carte    
    @classmethod
    def display_prince_choice(cls, jeu_joueur, jeu_ia):
        cls._game_scene.display_prince_choice(jeu_joueur, jeu_ia)
        cls._game_scene.wait_visibility(cls._game_scene)
    
    
    @classmethod
    #Fonction appelée lorsque l'utilisateur a tenté de deviner une carte grâce au guarde
    def card_chosen(cls, special_frame, card):
        
        special_frame.stop_display()
        model.cards.Garde.deuxieme_action(card)
        
    @classmethod
    #Fonction appelée lorsque l'utilisateur a joué le prince et choisi le camp qui défausse sa carte
    def side_chosen(cls, special_frame, side):
        special_frame.stop_display()
        model.cards.Prince.deuxieme_action(side)
        
    @classmethod
    def display_AI_card(cls,card):
        var = tk.IntVar()
        cls._game_scene.display_AI_card(str(card))
        cls._game_scene.lock_buttons()
        cls._game_scene.view.after(3000, var.set, 1)
        cls._game_scene.wait_variable(var)
        cls._game_scene.update_iaUI(1)
        cls._game_scene.unlock_buttons()

    @classmethod
    def update_details_label(cls, text):
        cls._game_scene.update_details_label(text)
        
    @classmethod
    #Fonction appelée en cas de fin de manche/partie
    def victory_test(cls, view):
        
        #Simulation d'une victoire de partie/manche
        score = [4,5]
        view._scenes["End game scene"].victory_screen("joueur", score)
        

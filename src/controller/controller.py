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
    _viewvar = None
    
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
            cls.card_playedAI(gamescene)
        else:
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
        
        #Si la carte est un garde et que c'est le tour de l'utilisateur, on va afficher une écran lui montrant quelles cartes il peut 
        #deviner
        if(str(cls._modelvar.current_player.cards[index]) == "Garde"):
            gamescene.display_guard_choice()
            gamescene.wait_visibility(gamescene)
        
        #Si la carte est un prince, alors il pourra choisir le camp qui défausse sa carte
        if(str(cls._modelvar.current_player.cards[index]) == "Prince"):
            gamescene.display_prince_choice()
            gamescene.wait_visibility(gamescene)
        
            
        #Actualisation du label indiquant la carte dernièrement jouée
        gamescene.update_infolabel(str(cls._modelvar.current_player), str(cls._modelvar.current_player.cards[index])) 
        
        #Action de la carte et changement de joueur courant
        current_player = cls._modelvar.play(index)
        
        #Nouveau tour
        cls.start_turn(current_player, gamescene)
    
    @classmethod
    #Prend dans le modèle les cartes ayant été jouées lors du round afin de les redonner à la view qui va les afficher
    def get_played_cards(cls, special_frame):
        special_frame.display_allcards(cls._modelvar.cards_played)
    
    '''
    @classmethod
    def display_guard_choice(cls):
        gamescene.display_guard_choice()
        gamescene.wait_visibility(gamescene)'''
        
    @classmethod
    #Fonction appelée lorsque l'utilisateur a tenté de deviner une carte grâce au guarde
    def card_chosen(cls, special_frame, card):
        print("vous avez choisi " + card)
        special_frame.stop_display()
        
    @classmethod
    #Fonction appelée lorsque l'utilisateur a joué le prince et choisi le camp qui défausse sa carte
    def side_chosen(special_frame, side):
        print("vous avez choisi " + side)
        special_frame.stop_display()
        
        
    @classmethod
    #Fonction appelée en cas de fin de manche/partie
    def victory_test(cls, view):
        
        #Simulation d'une victoire de partie/manche
        score = [4,5]
        view._scenes["End game scene"].victory_screen("joueur", score)
        
            

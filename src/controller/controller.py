# -*- coding: utf-8 -*-
'''
Created on 26 oct. 2020

@author: Antoine
'''

import src.model.model as model
import webbrowser
import sys
import tkinter as tk

#Ne pas appeler cette variable depuis un module de view afin de garder l'indépendance entre modèle et view
modelvar = None

def consulter_regles():
    webbrowser.open('https://fr.wikipedia.org/wiki/Love_Letter_(jeu)')

def quitter_jeu():
    sys.exit(0)
    
#Fonction appelée lorsque l'utilisateur lance une partie/finit une partie/retourne au menu
def display_scene(view, scene_name):
    view.display_scene(scene_name)

#Fonction lancée lorsque l'utilisateur à choisi la difficulté de la partie
def start_game(view, difficulty): #difficulty = -1 : nouveau round, difficulté != -1 : nouvelle partie
    current_player = modelvar.init_data(difficulty)

    #Affichage du plateau de jeu
    display_scene(view, "Game scene")

    #Affichage des 3 premieres cartes et du nom de la personne qui commence
    view.scenes["Game scene"].init_round(modelvar.get_three_cards(), str(modelvar.current_player))
    
    #Début du premier tour
    start_turn(current_player, view.scenes["Game scene"])
    
    
#Fonction permettant le déroulement d'un tour
def start_turn(current_player, gamescene):
    #Actualisation de l'UI (nombre de cartes de l'IA)
    gamescene.update_iaUI(modelvar.ia.cards.__len__())
    
    #Actualisation de l'UI du vrai joueur (nombre de cartes et images associées du joueur)
    gamescene.update_playerUI(modelvar.player.cards_to_string)
    
    #Si le joueur actuel est l'IA, alors l'utilisateur ne peut pas jouer, et le process se fera sans UI, dans le modèle
    if(isinstance(current_player, model.player.IA)):
        gamescene.lock_buttons()
        index = modelvar.choose_cardAI()
        gamescene.view.after(3000, card_played, gamescene, index) #Attente de 3 secondes avant que l'utilisateur puisse jouer
    else:
        gamescene.unlock_buttons()
    
#Fonction appelée lorsqu'un joueur a choisi une carte
def card_played(gamescene, index):
    #if(not isinstance(modelvar.current_player.last_card_played(), model.cards.Chancelier)):
    
    #Si la carte est un garde et que c'est le tour de l'utilisateur, on va afficher une écran lui montrant quelles cartes il peut 
    #deviner
    if(str(modelvar.current_player.cards[index]) == "Garde" and isinstance(modelvar.current_player, model.player.RealPlayer)):
        
        
        gamescene.display_guard_choice()
        gamescene.wait_visibility(gamescene)
    
    #Si la carte est un prince, alors il pourra choisir le camp qui défausse sa carte
    if(str(modelvar.current_player.cards[index]) == "Prince" and isinstance(modelvar.current_player, model.player.RealPlayer)):
        gamescene.display_prince_choice()
        
    #Actualisation du label indiquant la carte dernièrement jouée
    gamescene.update_infolabel(str(modelvar.current_player), str(modelvar.current_player.cards[index])) 
    
    #Action de la carte et changement de joueur courant
    current_player = modelvar.play(index)
    
    #Nouveau tour
    start_turn(current_player, gamescene)

#Prend dans le modèle les cartes ayant été jouées lors du round afin de les redonner à la view qui va les afficher
def get_played_cards(special_frame):
    special_frame.display_allcards(modelvar.cards_played)

#Fonction appelée lorsque l'utilisateur a tenté de deviner une carte grâce au guarde
def card_chosen(special_frame, card):
    print("vous avez choisi " + card)
    special_frame.stop_display()
    
#Fonction appelée lorsque l'utilisateur a joué le prince et choisi le camp qui défausse sa carte
def side_chosen(special_frame, side):
    print("vous avez choisi " + side)
    special_frame.stop_display()
    
    
#Fonction appelée en cas de fin de manche/partie
def victory_test(view):
    
    #Simulation d'une victoire de partie/manche
    score = [4,5]
    view._scenes["End game scene"].victory_screen("joueur", score)
    
        

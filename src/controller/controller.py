# -*- coding: utf-8 -*-
'''
Created on 26 oct. 2020

@author: Antoine
'''

import src.model.model as model
import webbrowser
import sys


#Ne pas appeler cette variable depuis un module de view afin de garder l'indépendance entre modèle et view
modelvar = None

def consulter_regles():
    webbrowser.open('https://fr.wikipedia.org/wiki/Love_Letter_(jeu)')

def quitter_jeu():
    sys.exit(0)

def start_game(view, difficulty): #difficulty = -1 : nouveau round, difficulté != -1 : nouvelle partie
    current_player = modelvar.init_data(difficulty)

    display_scene(view, "Game scene")

    #Affichage des 3 premieres cartes et du nom de la personne qui commence
    view.scenes["Game scene"].init_round(modelvar.get_three_cards(), str(modelvar.current_player))
    
    #Début du premier tour
    start_turn(current_player, view)
    
    
    
    
def start_turn(current_player, view):
    view.scenes["Game scene"].update_iaUI(modelvar.ia.cards.__len__())
    view.scenes["Game scene"].update_playerUI(modelvar.player.cards_to_string)
    if(isinstance(current_player, model.player.IA)):
        view.scenes["Game scene"].lock_buttons()
        index = modelvar.choose_cardAI()
        view.after(3000, card_played, view, index)
    else:
        view.scenes["Game scene"].unlock_buttons()
    
#Fonction appelée lorsque l'utilisateur lance une partie/finit une partie/retourne au menu
def display_scene(view, scene_name):
    view.display_scene(scene_name)


def victory_test(view):
    
    #Simulation d'une victoire de partie/manche
    score = [4,5]
    view._scenes["End game scene"].victory_screen("joueur", score)
    
def card_played(view, index):
    #if(not isinstance(modelvar.current_player.last_card_played(), model.cards.Chancelier)):
    view.scenes["Game scene"].update_infolabel(str(modelvar.current_player), str(modelvar.current_player.cards[index])) 
    current_player = modelvar.play(index)
    
    start_turn(current_player, view)

        

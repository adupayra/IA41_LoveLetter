# -*- coding: utf-8 -*-
'''
Created on 26 oct. 2020

@author: Antoine
'''

import webbrowser
import sys

#Ne pas appeler cette variable depuis un module de view afin de garder l'indépendance entre modèle et view
modelvar = None

def consulter_regles():
    webbrowser.open('https://fr.wikipedia.org/wiki/Love_Letter_(jeu)')

def quitter_jeu():
    sys.exit(0)

def start_game(view, difficulty = 0):
    #view.resetdata
    #modelvar.resetdata
    
    modelvar.init_data()

    #Variables permettant le stockage des différentes listes de cartes du modèle qui nous intéresse sous forme de string
    cards_played_string = []
    players_cards_string = []
    
    #Stockage des string des valeurs des 3 cartes montrées du début de round
    for card in modelvar.cards_played:
        cards_played_string.append(str(card))
    
    #Stockage des string des valeurs des cartes du joueur
    for card in modelvar.player.cards:
        players_cards_string.append(str(card))
        
    view.scenes["Game scene"].init_round(cards_played_string, players_cards_string)
    
    display_scene(view, "Game scene")
    
#Fonction appelée lorsque l'utilisateur lance une partie/finit une partie/retourne au menu
def display_scene(view, scene_name):
    view.display_scene(scene_name)


def victory_test(view):
    
    #Simulation d'une victoire de partie/manche
    score = [4,5]
    view._scenes["End game scene"].victory_screen("joueur", score)
    
def card_played(index):
    pass
        

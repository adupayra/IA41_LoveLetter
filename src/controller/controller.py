# -*- coding: utf-8 -*-
'''
Created on 26 oct. 2020

@author: Antoine
'''

import src.model.model as model

#Fonction appelée lorsque l'utilisateur lance une partie/finit une partie/retourne au menu
def display_scene(view, scene_name):
    view.display_scene(scene_name)
    
def victory_test(view):
    
    #Simulation d'une victoire de partie/manche
    score = [4,5]
    view._scenes["End game scene"].victory_screen("joueur", score)
    
def card_played(index):
    pass
        

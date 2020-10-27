# -*- coding: utf-8 -*-
'''
Created on 26 oct. 2020

@author: Antoine
'''


def display_scene(view, scene_name):
    view.display_scene(scene_name)
    
def card_played(view):
    
    #Simulation d'une victoire de partie/manche
    score = [4,5]
    view._scenes["End game scene"].victory_screen("joueur", score)
        
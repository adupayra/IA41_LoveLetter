# -*- coding: utf-8 -*-
'''
Created on 28 oct. 2020

@author: Antoine
'''
import src.model.cards as cards
from random import shuffle
import src.model.player as player

class Model(object):
    '''
    classdocs
    '''
    
    _cards = []
    _card_played = []
    _card_remained = []
    _deck = []
    _player = None
    _ia = None
    

    def __init__(self):
        '''
        Constructor
        '''
        Model._cards.append(cards.Roi())
        Model._cards.append(cards.Comtesse())
        Model._cards.append(cards.Princesse())
        
        for _ in range(0,2):
            Model._cards.append(cards.Espionne())
            Model._cards.append(cards.Garde())
            Model._cards.append(cards.Pretre())
            Model._cards.append(cards.Servante())
            Model._cards.append(cards.Prince())
            Model._cards.append(cards.Chancelier())
            
        for _ in range(0, 4):
            Model._cards.append(cards.Garde())
    
        #Fonction qui permet de compter le nombre d'instances d'une classe dans la liste, ici, garde
        #elle sert à rien, c'est juste au cas où vous ayez besoin de ça
        
        #count = sum(isinstance(x, cards.Garde) for x in Model._cards)
        
        
        
    def init_data(self,difficulty):
        #Mélange des cartes
        shuffle(Model._cards)
        
        #Création des joueurs
        self.creer_joueurs(difficulty)
        
        #distribution des cartes dans les différentes listes
        self.distribution()
        
    def creer_joueurs(self, difficulty):
        Model._player = player.RealPlayer()
        if difficulty == 0:
            Model._ia = player.IAFacile()
        elif difficulty == 1:
            Model._ia = player.IAMoyenne()
        else:
            Model._ia = player.IADifficile()
            
    def distribution(self):
        pass
            
            
        
        
test = Model()
            
                
        
            
        
# -*- coding: utf-8 -*-
'''
Created on 28 oct. 2020

@author: Antoine
'''

import abc
from abc import abstractmethod

class Player(metaclass = abc.ABCMeta):
    '''
    Classe servant de template pour la classe vraie joueur et les classes d'IA
    '''
    

    def __init__(self):
        '''
        Constructor
        '''
        self._cards = []
        self._nb_cards = 0
        
    @property
    def cards(self):
        return self._cards
    
    @property
    def nb_cards(self):
        return self._nb_cards
    
    def add_card(self, new_card):
        self._cards.append(new_card)
        
    def remove_card(self, index):
        self._cards.pop(index)
    
    

class RealPlayer(Player):
    
    def __init__(self):
        Player.__init__(self)
    
    
class IA(Player, metaclass = abc.ABCMeta):
    '''
    Classe servant de template pour les différentes IA
    '''
    
    def __init__(self):
        Player.__init__(self)
    

    def next_states(self):
        pass
    
    @abstractmethod
    def algorithme(self):
        pass
    
class IAFacile(IA):
    
    def __init__(self):
        IA.__init__(self)
    
    def algorithme(self):
        pass

class IAMoyenne(IA):
    
    def __init__(self):
        IA.__init__(self)
    
    def algorithme(self):
        pass

class IADifficile(IA):
    
    def __init__(self):
        IA.__init__(self)
    
    def algorithme(self):
        pass
    

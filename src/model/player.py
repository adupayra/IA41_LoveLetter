# -*- coding: utf-8 -*-
'''
Created on 28 oct. 2020

@author: Antoine
'''

import abc
from abc import abstractmethod

#Liste circulairement chainée, contenant les noeuds contenant chaque joueur, ainsi que le noeud du joueur courant
class CircleLinkedList(object):

    def __init__(self, head, tail):
        self._real_player_node = head
        self._ia_node = tail
        self._current_node = None
    
    #Passe au prochain joueur
    def next_turn(self):
        self._current_node = self._current_node.next_player
        return self._current_node
    
    @property
    def real_player_node(self):
        return self._real_player_node
    
    @property
    def ia_node(self):
        return self._ia_node
    
    @property
    def real_player(self):
        return self._real_player_node.player
    
    @property
    def ia(self):
        return self._ia_node.player
    
    @property
    def current_node(self):
        return self._current_node
    
    @current_node.setter
    def current_node(self, player):
        if(self._current_node is None):
            self._current_node = player
        
    @property
    def current(self):
        return self._current_node.player
    
    @property
    def next_player_node(self):
        return self._current_node.next_player
    
    @property
    def next_player(self):
        return self._current_node.next_player.player
    

#Noeud contenant l'instance d'un joueur et la référence vers le noeud suivant
class Node(object):
    
    def __init__(self, player):
        self._player = player
    
    @property
    def next_player(self):
        return self._next_player
    
    @next_player.setter
    def next_player(self, next_player):
        self._next_player = next_player
        
    @property
    def player(self):
        return self._player


class Player(metaclass = abc.ABCMeta):
    '''
    Classe servant de template pour la classe vraie joueur et les classes d'IA
    '''
    

    def __init__(self):
        '''
        Constructor
        '''
        self._score = 0
        self._cards = []
        self._last_card_played = None #Utilisé pour le chancelier
        self._cards_to_string = []
        self._immune = False
        
    @property
    def cards(self):
        return self._cards

    @property 
    def cards_to_string(self):
        self._cards_to_string = []
        for card in self._cards:
            self._cards_to_string.append(str(card))
        return self._cards_to_string
    
    @property
    def last_card_played(self):
        return self._last_card_played
    
    @last_card_played.setter
    def last_card_played(self, value):
        self._last_card_played = value   
         
    @property
    def immune(self):
        return self._immune
    
    @immune.setter
    def immune(self):
        self._immune = not self._immune
        return self._immune
    
    @property
    def score(self):
        return self._score
    
    def win(self, value):
        self._score += value
        
    def add_card(self, new_card, index):
        self._cards.insert(index, new_card)
        
    def remove_card(self, index):
        self._cards.pop(index)
        
    def reset_values(self):
        self._cards = []
        self._last_card_played = None
        self._immune = False
    
    

class RealPlayer(Player):
    
    def __init__(self):
        Player.__init__(self)
    
    def __str__(self):
        return "Joueur"
    
class IA(Player, metaclass = abc.ABCMeta):
    '''
    Classe servant de template pour les différentes IA
    '''
    
    def __init__(self, model):
        Player.__init__(self)
        self._model = model
    
    def __str__(self):
        return "IA"

    def next_states(self):
        pass
    
    @abstractmethod
    def algorithme(self):
        pass

    @abstractmethod
    def algorithmeGuard(self):
        pass
    
    @abstractmethod
    def algorithmePrince(self):
        pass
    
    @abstractmethod
    def algorithmeChancelier(self):
        pass
    
class IAFacile(IA):
    
    def __init__(self, model):
        IA.__init__(self, model)
    
    def __str__(self):
        return "IA Facile"
    
    def algorithme(self):
        pass

    def algorithmeGuard(self):
        pass
    
    def algorithmePrince(self):
        pass
    
    def algorithmeChancelier(self):
        pass
    
class IAMoyenne(IA):
    
    
    def __init__(self, model):
        IA.__init__(self, model)
    
    def __str__(self):
        return "IA Moyenne"
    
    def algorithme(self):
        pass
    
    def algorithmeGuard(self):
        pass
    
    def algorithmePrince(self):
        pass
    
    def algorithmeChancelier(self):
        pass

class IADifficile(IA):
    
    def __init__(self, model):
        IA.__init__(self, model)
    
    def __str__(self):
        return "IA Difficile"
    
    def algorithme(self):
        pass
    
    def algorithmeGuard(self):
        pass
    
    def algorithmePrince(self):
        pass
    
    def algorithmeChancelier(self):
        pass
    

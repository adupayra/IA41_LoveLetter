# -*- coding: utf-8 -*-
'''
Created on 27 oct. 2020

@author: Antoine
'''

import abc
from abc import abstractmethod
from builtins import classmethod
import src.model.player as player
from random import randrange

class Card(metaclass = abc.ABCMeta):
    '''
    template pour toutes les cartes du jeu
    '''
    
    _model = None
    
    #Permet d'afficher la string retournée par __str__ lorsque l'on veut print une instance d'une carte
    def __repr__(self):
        return self.__str__()
    
    def __init__(self, model):
        self._model = model
        
    
    #Propriété des cartes (valeur)
    @property
    @abstractmethod
    def value(self):
        pass
    
    #Action effectuée par la carte une fois jouée
    @abstractmethod
    def action(self):
        pass
    

class TwoActionCards(Card, metaclass = abc.ABCMeta):
    '''
    classe abstraite parente des classes se déroulant en deux temps du point de vue utilisateur (choix de la carte -> second choix -> action sur le modèle)
    '''
    
    def __init__(self, model):
        Card.__init__(self, model)
        
class Espionne(Card):
    '''
    Classe définissant la carte espionne
    '''
    
    #Permet de print Espionne à la place de la référence de l'objet en mémoire
    def __str__(self):
        return "Espionne"
    
    
    def __init__(self, model):
        Card.__init__(self, model)
    
    @classmethod
    def value(cls):
        return 0
    
    
    @classmethod
    def action(cls):
        pass
    
    
class Garde(TwoActionCards):
    '''
    Classe définissant la carte garde
    '''
    
    def __str__(self):
        return "Garde"
    
    def __init__(self, model):
        Card.__init__(self, model)
    
    @classmethod
    def value(cls):
        return 1
    
    @classmethod
    def action(cls):
        if(isinstance(Card._model.current_player, player.RealPlayer)):
            Card._model.controller.display_guard_choice()
        else:
            #algo ia
            pass
    
    @classmethod
    def deuxieme_action(cls, chosen_card):
        print("vous avez choisi " + chosen_card)
        
        
            
    
class Pretre(Card):
    '''
    Classe définissant la carte pretre
    '''
    
    def __str__(self):
        return "Pretre"
    
    def __init__(self, model):
        Card.__init__(self, model)
    
    @classmethod
    def value(cls):
        return 2
    
    @classmethod
    def action(cls):
        if(isinstance(Card._model.current_player, player.RealPlayer)):
            Card._model.controller.display_AI_card(Card._model.ia.cards[0])
            
class Baron(Card):
    '''
    Classe définissant la carte baron
    '''
    
    def __str__(self):
        return "Baron"
    
    def __init__(self, model):
        Card.__init__(self, model)
    
    @classmethod
    def value(cls):
        return 3
    
    @classmethod
    def action(cls):
        if(isinstance(Card._model.current_player.cards[0], Baron)):
            Card._model.controller.display_baron(Card._model.current_player.cards[1], Card._model.players_list.current_node.next().player.cards[0])
        else:
            Card._model.controller.display_baron(Card._model.current_player.cards[0], Card._model.players_list.current_node.next().player.cards[0])
    
class Servante(Card):
    '''
    Classe définissant la carte servante
    '''
    def __str__(self):
        return "Servante"
    
    def __init__(self, model):
        Card.__init__(self, model)
    
    @classmethod
    def value(cls):
        return 4
    
    @classmethod
    def action(cls):
        pass
    
class Prince(TwoActionCards):
    '''
    Classe définissant la carte prince
    '''
    
    def __str__(self):
        return "Prince"
    
    def __init__(self, model):
        Card.__init__(self, model)
    
    _player_side = "Jeu joueur"
    _ia_side = "Jeu IA"
    
    @classmethod
    def value(cls):
        return 5
    
    @classmethod
    def action(cls):
        if(isinstance(Card._model.current_player, player.RealPlayer)):
            Card._model.controller.display_prince_choice(Prince._player_side, Prince._ia_side)
        else:
            alea = randrange(2)
            if(alea == 0):
                Prince.deuxieme_action(Prince._player_side)
            else:
                Prince.deuxieme_action(Prince._ia_side)
    
    @classmethod
    def deuxieme_action(cls, chosen_side):
        print(str(Card._model.current_player) + " a choisi " + chosen_side)
        
class Chancelier(Card):
    '''
    Classe définissant la carte chancelier
    '''
    
    _choix_cartes = None
    
    def __str__(self):
        return "Chancelier"
    
    def __init__(self, model):
        Card.__init__(self, model)
    
    @classmethod
    def value(cls):
        return 6
    
    @classmethod
    def action(cls):
        pass

class Roi(Card):
    '''
    Classe définissant la carte comtesse
    '''
    
    def __str__(self):
        return "Roi"
    
    def __init__(self, model):
        Card.__init__(self, model)
    
    @classmethod
    def value(cls):
        return 7
    
    @classmethod
    def action(cls):
        pass
    
class Comtesse(Card):
    '''
    Classe définissant la carte comtesse
    '''
    
    def __str__(self):
        return "Comtesse"
    
    def __init__(self, model):
        Card.__init__(self, model)
    
    @classmethod
    def value(cls):
        return 8
    
    @classmethod
    def action(cls):
        pass
    
class Princesse(Card):
    '''
    Classe définissant la carte princesse
    '''
    
    def __str__(self):
        return "Princesse"
    
    def __init__(self, model):
        Card.__init__(self, model)
    
    @classmethod
    def value(cls):
        return 9
    
    @classmethod
    def action(cls):
        pass
    

    
    
    
    
    
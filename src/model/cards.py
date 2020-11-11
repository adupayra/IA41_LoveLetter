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
        #Vérification du joueur courant afin d'afficher ou non quelque chose sur l'UI
        if(isinstance(cls._model.current_player, player.RealPlayer)):
            cls._model.controller.display_guard_choice()
            print(cls.__name__())
        else:
            
            #algo ia
            pass
    
    #Action effectuée une fois que la carte à deviner a été choisi
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
        if(isinstance(cls._model.current_player, player.RealPlayer)):
            cls._model.controller.display_AI_card(cls._model.ia.cards[0])
            
            
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
        #Caching des valeurs auxquelles on va beaucoup accéder dans la fonction
        current_player = cls._model.current_player
        next_player= cls._model.next_player
        
        #Chaine de caractere de victoire
        chaine = " gagne 1 point, en ayant joué un baron"
        
        #Vérifie quelle carte n'est pas un baron dans la main du joueur courant (afin de ne pas comparer le baron joué avec la carte de l'autre joueur)
        #Ici, on veut comparer la deuxieme carte du joueur courant (la première étant le baron joué)
        if(isinstance(cls._model.current_player.cards[0], Baron)):
            #Affichage de l'écran
            cls._model.controller.display_baron(current_player.cards[1], next_player.cards[0])
            
            #Check du gagnant
            if(current_player.cards[1].value() > next_player.cards[0].value()):
                cls._model.game_victory(current_player, str(current_player) + chaine)
                                         
            elif(current_player.cards[1].value() < next_player.cards[0].value()):
                cls._model.game_victory(next_player, str(next_player) + chaine)  
        else:
            #Ici, on veut comparer la première carte du joueur courant (la deuxieme étant le baron joué)
            #Affichage de l'écran
            cls._model.controller.display_baron(current_player.cards[0], next_player.cards[0])
            
            #Check du gagnant
            if(current_player.cards[0].value() > next_player.cards[0].value()):
                cls._model.game_victory(current_player, str(current_player) + chaine)
                
            elif(current_player.cards[0].value() < next_player.cards[0].value()):
                cls._model.game_victory(next_player, str(next_player) + chaine)  
        
        
        
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
        if(isinstance(cls._model.current_player, player.RealPlayer)):
            cls._model.controller.display_prince_choice(cls._player_side, cls._ia_side)
        else:
            alea = randrange(2)
            if(alea == 0):
                cls.deuxieme_action(cls._player_side)
            else:
                cls.deuxieme_action(cls._ia_side)
    
    @classmethod
    def deuxieme_action(cls, chosen_side):
        print(str(cls._model.current_player) + " a choisi " + chosen_side)
        
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
    

    
    
    
    
    
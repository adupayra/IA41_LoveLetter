# -*- coding: utf-8 -*-
'''
Created on 27 oct. 2020

@author: Antoine
'''

import abc
from abc import abstractmethod
from builtins import classmethod

class Card(metaclass = abc.ABCMeta):
    '''
    template pour toutes les cartes du jeu
    '''
    
    #Permet d'afficher la string retournée par __str__ lorsque l'on veut print une instance d'une carte
    def __repr__(self):
        return self.__str__()
    
    def __init__(self):
        pass
    
    #Propriété des cartes (valeur)
    @property
    @abstractmethod
    def value(self):
        pass
    
    #Action effectuée par la carte une fois jouée
    @abstractmethod
    def action(self):
        pass
    

class Espionne(Card):
    '''
    Classe définissant la carte espionne
    '''
    
    #Permet de print Espionne à la place de la référence de l'objet en mémoire
    def __str__(self):
        return "Espionne"
    
    
    def __init__(self):
        Card.__init__(self)
    
    @classmethod
    def value():
        return 0
    
    
    @classmethod
    def action(self):
        pass
    
    
class Garde(Card):
    '''
    Classe définissant la carte garde
    '''
    
    def __str__(self):
        return "Garde"
    
    def __init__(self):
        Card.__init__(self)
    
    @classmethod
    def value(self):
        return 1
    
    @classmethod
    def action(self):
        pass
    
class Pretre(Card):
    '''
    Classe définissant la carte pretre
    '''
    
    def __str__(self):
        return "Pretre"
    
    def __init__(self):
        Card.__init__(self)
    
    @classmethod
    def value(self):
        return 2
    
    @classmethod
    def action(self):
        pass
    
class Baron(Card):
    '''
    Classe définissant la carte baron
    '''
    
    def __str__(self):
        return "Baron"
    
    def __init__(self):
        Card.__init__(self)
    
    @classmethod
    def value(self):
        return 3
    
    @classmethod
    def action(self):
        pass
    
class Servante(Card):
    '''
    Classe définissant la carte servante
    '''
    def __str__(self):
        return "Servante"
    
    def __init__(self):
        Card.__init__(self)
    
    @classmethod
    def value(self):
        return 4
    
    @classmethod
    def action(self):
        pass
    
class Prince(Card):
    '''
    Classe définissant la carte prince
    '''
    
    def __str__(self):
        return "Prince"
    
    def __init__(self):
        Card.__init__(self)
    
    @classmethod
    def value(self):
        return 5
    
    @classmethod
    def action(self):
        pass
    
class Chancelier(Card):
    '''
    Classe définissant la carte chancelier
    '''
    
    def __str__(self):
        return "Chancelier"
    
    def __init__(self):
        Card.__init__(self)
    
    @classmethod
    def value(self):
        return 6
    
    @classmethod
    def action(self):
        pass

class Roi(Card):
    '''
    Classe définissant la carte comtesse
    '''
    
    def __str__(self):
        return "Roi"
    
    def __init__(self):
        Card.__init__(self)
    
    @classmethod
    def value(self):
        return 7
    
    @classmethod
    def action(self):
        pass
    
class Comtesse(Card):
    '''
    Classe définissant la carte comtesse
    '''
    
    def __str__(self):
        return "Comtesse"
    
    def __init__(self):
        Card.__init__(self)
    
    @classmethod
    def value(self):
        return 8
    
    @classmethod
    def action(self):
        pass
    
class Princesse(Card):
    '''
    Classe définissant la carte princesse
    '''
    
    def __str__(self):
        return "Princesse"
    
    def __init__(self):
        Card.__init__(self)
    
    @classmethod
    def value(self):
        return 9
    
    @classmethod
    def action(self):
        pass
    

    
    
    
    
    
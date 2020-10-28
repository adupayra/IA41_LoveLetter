# -*- coding: utf-8 -*-
'''
Created on 27 oct. 2020

@author: Antoine
'''

import abc
from abc import abstractmethod


class Card(metaclass = abc.ABCMeta):
    '''
    template pour toutes les cartes du jeu
    '''

    
    
    def __init__(self):
        pass
    
    @property
    @abstractmethod
    def value(self):
        pass
    
    @abstractmethod
    def action(self):
        pass
    

class Espionne(Card):
    '''
    Classe définissant la carte espionne
    '''
    
    def __init__(self):
        Card.__init__(self)
    
    @classmethod
    def value(self):
        return 0
    
    @classmethod
    def action(self):
        pass
    
class Garde(Card):
    '''
    Classe définissant la carte garde
    '''
    
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
    
    def __init__(self):
        Card.__init__(self)
    
    @classmethod
    def value(self):
        return 9
    
    @classmethod
    def action(self):
        pass
    
test = Garde()
    
    
    
    
    
# -*- coding: utf-8 -*-
'''
Created on 28 oct. 2020

@author: Antoine
'''
import src.model.cards as cards
from random import shuffle
import src.model.player as player
import os

class Model(object):
    '''
    classdocs
    '''
    
    _cards_played = []
    _instance = None

    def __init__(self):
        '''
        Le constructeur va permettre l'instantiation de toutes les cartes, seule donnée persistante du programme (afin de ne pas avoir à ré instancier les cartes
        à chaque début de partie/début de round
        '''
        
        if(Model._instance is None):
            #Définition des différents attributs
            self._cards = []
            self._cards_played = []
            self._burnt_card = None
            self._deck = []
            self._player = None
            self._ia = None
            
            #Instantiation de toutes les cartes
            self._cards.append(cards.Roi())
            self._cards.append(cards.Comtesse())
            self._cards.append(cards.Princesse())
            
            for _ in range(0,2):
                self._cards.append(cards.Espionne())
                self._cards.append(cards.Garde())
                self._cards.append(cards.Pretre())
                self._cards.append(cards.Baron())
                self._cards.append(cards.Servante())
                self._cards.append(cards.Prince())
                self._cards.append(cards.Chancelier())
                
            for _ in range(0, 4):
                self._cards.append(cards.Garde())
            Model._instance = self

        
        #print(Model._cards[0])
        #Fonction qui permet de compter le nombre d'instances d'une classe dans la liste, ici, garde
        #elle sert à rien, c'est juste au cas où vous ayez besoin de ça
        
        #count = sum(isinstance(x, cards.Garde) for x in self._cards)
        
        
        
    #Fonction permettant l'initialisation des données non persistantes (appel à chaque début de partie et début de round)
    def init_data(self,difficulty = 0):
        #Mélange des cartes
        shuffle(self._cards)
        
        
        #Création des joueurs si il s'agit d'un début de partie
        if self._player is None:
            self.creer_joueurs(difficulty)
        
        #distribution des cartes dans les différentes listes
        self.distribution()
        
    def creer_joueurs(self, difficulty = 0):
        self._player = player.RealPlayer()
        if difficulty == 0:
            self._ia = player.IAFacile()
        elif difficulty == 1:
            self._ia = player.IAMoyenne()
        else:
            self._ia = player.IADifficile()
    
    def distribution(self):
        self._player.add_card(self._cards[0])
        self._ia.add_card(self._cards[1])
        self._burnt_card = self._cards[2]
        self._cards_played.append(self._cards[3])
        self._cards_played.append(self._cards[4])
        self._cards_played.append(self._cards[5])
        for i in range (6, self._cards.__len__()):
            self._deck.append(self._cards[i])
        
    @property
    def cards(self):
        return self._cards
    
    @property
    def cards_played(self):
        return self._cards_played

    @property
    def burnt_card(self):
        return self._burnt_card
        
    @property
    def deck(self):
        return self._deck

    @property
    def player(self):
        return self._player
        
    @property
    def ia(self):
        return self._ia
    
    def add_cards_played(self, new_card):
        self._cards_played.append(new_card)

    def pick_card(self, card):
        self.deck.remove(card)
            
            
        
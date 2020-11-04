# -*- coding: utf-8 -*-
'''
Created on 28 oct. 2020

@author: Antoine
'''
import src.model.cards as cards
from random import shuffle
from random import randrange
import src.model.player as player

class Model(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Le constructeur va permettre l'instantiation de toutes les cartes, seule donnée persistante du programme (afin de ne pas avoir à ré instancier les cartes
        à chaque début de partie/début de round
        '''
        #Définition des différents attributs
        self._cards = [] #Liste de toutes les cartes
        self._cards_played = [] #Liste des cartes jouées (comprenant les 3 cartes montrées au début)
        self._burnt_card = None #La carte inconnue
        self._deck = [] #La pioche
        self._player = None #Le vrai joueur
        self._ia = None #l'ia
        self._players = [] #Utilisé afin de connaitre le prochain joueur
        self._current_player = None #Utilisé pour savoir qui doit jouer 
        
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
    
    @property
    def current_player(self):
        return self._current_player
        
        
    #Fonction permettant l'initialisation des données non persistantes (appel à chaque début de partie et début de round)
    def init_data(self,difficulty = -1):
        
        #Réinitialisation des données du round précédent
        self._cards_played = []
        self._burnt_card = None
        self._deck = [] 
        
        #Mélange des cartes
        shuffle(self._cards)
        
        #Création des joueurs si il s'agit d'un début de partie
        if difficulty != -1: #-1 veut dire qu'aucun argument n'a été envoyé à la fonction, ce qui veut dire qu'il s'agit d'un nouveau round et non d'une nouvelle 
                            #partie
            self.creer_joueurs(difficulty)
        else: #Nouveau round, on réinitialise donc la main de l'ia et du joueur
            self._ia.reset_values()
            self._player.reset_values()
        
        #distribution des cartes dans les différentes listes
        self.distribution()
        
        #Détermine le premier joueur
        premier_joueur = randrange(0,2)
        
        if premier_joueur == 0:
            self._current_player = self._player
            self._players.append(self._player)
            self._players.append(self._ia)
        else:
            self._current_player = self._ia
            self._players.append(self._ia)
            self._players.append(self._player)
        self._current_player.add_card(self.pick_card(),1)
        
        
        return self._current_player
        
    #Instanciation des joueurs
    def creer_joueurs(self, difficulty = 0):
        self._player = player.RealPlayer()
        if difficulty == 0:
            self._ia = player.IAFacile()
        elif difficulty == 1:
            self._ia = player.IAMoyenne()
        else:
            self._ia = player.IADifficile()
    
    #Distribution des cartes dans les différentes listes
    def distribution(self):
        self._player.add_card(self._cards[0], 0) #Une carte au joueur
        self._ia.add_card(self._cards[1],0) #Une à l'IA
        self._burnt_card = self._cards[2] #La carte qui restera cachée le long de la partie
        
        #Les 3 cartes visibles dès le début
        self._cards_played.append(self._cards[3]) 
        self._cards_played.append(self._cards[4])
        self._cards_played.append(self._cards[5])
        
        #la pioche
        for i in range (6, self._cards.__len__()):
            self._deck.append(self._cards[i])
        
        
    #Ajoute une carte à la liste des cartes jouées dans le round
    def add_cards_played(self, new_card):
        self._cards_played.append(new_card)

    #Pioche une carte
    def pick_card(self):
        return self._deck.pop(0)
        
    #Retourne les 3 première cartes de jeu (celles affichées au milieu du plateau)
    def get_three_cards(self):
        return str(self._cards_played[0]), str(self._cards_played[1]), str(self._cards_played[2])
    
    #Effectue l'action de la carte à l'index associée du joueur courrant
    def play(self, index):
        self._cards_played.append(self._current_player.cards[index])#Ajout de cette carte à la liste des cartes jouées
        self._current_player.cards[index].action()#Action de la carte
        self._current_player.remove_card(index)#Suppression de la carte dans la main du joueur courrant
        self.next_turn(index)

        return self._current_player
        
    #Définition du prochain joueur
    def next_turn(self, index):
        if(isinstance(self._current_player, player.RealPlayer)):
            self._current_player = self._ia
        else:
            self._current_player = self._player
        self._current_player.add_card(self.pick_card(), index)
    
    #Choix de la carte jouée par l'IA
    def choose_cardAI(self):
        #Appeler algo de l'IA ici

        return randrange(0,1)
            
        
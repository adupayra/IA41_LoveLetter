# -*- coding: utf-8 -*-
'''
Created on 28 oct. 2020

@author: Antoine
'''

import src.model.cards as cards
from random import shuffle
from random import randrange
import src.model.player as player
import copy


class Model(object):
    '''
    classdocs
    '''


    def __init__(self, controller):
        '''
        Le constructeur va permettre l'instantiation de toutes les cartes, seule donnée persistante du programme (afin de ne pas avoir à ré instancier les cartes
        à chaque début de partie/début de round
        '''
        #Définition des différents attributs
        self._controller = controller
        self._cards = [] #Liste de toutes les cartes
        self._cards_played = [] #Liste des cartes jouées (comprenant les 3 cartes montrées au début)
        self._burnt_card = None #La carte inconnue
        self._deck = [] #La pioche
        self._players_list = None #Liste chainée contenant le joueur courant, le vrai joueur et l'ia
        self._victory = False
        self._winner = None
        cards.Card._model = self
        self._cartes_defaussees = [] #Cartes défaussées lorsque le prince est joué
        self._current_state = None
        self._issimul = False
        self._islearning = False
        self._victorylearning= False
        
        #Instantiation de toutes les cartes
        self._cards.append(cards.Roi(self))
        self._cards.append(cards.Comtesse(self))
        self._cards.append(cards.Princesse(self))
        
        for _ in range(0,2):
            self._cards.append(cards.Espionne(self))
            self._cards.append(cards.Garde(self))
            self._cards.append(cards.Pretre(self))
            self._cards.append(cards.Baron(self))
            self._cards.append(cards.Servante(self))
            self._cards.append(cards.Prince(self))
            self._cards.append(cards.Chancelier(self))
            
        for _ in range(0, 4):
            self._cards.append(cards.Chancelier(self))

    @property
    def controller(self):
        return self._controller
    
    @property
    def cards(self):
        return self._cards
    
    @property
    def cards_played(self):
        return self._cards_played
    
    #Utilisé en cas de sauvegarde du model (pour les simulations)
    @cards_played.setter
    def cards_played(self,value):
        self._cards_played = value
    
    @property
    def cards_played_ia(self):
        return self._cards_played_ia
    
    @property
    def cards_played_player(self):
        return self._cards_played_player

    @property
    def burnt_card(self):
        return self._burnt_card
        
    @property
    def deck(self):
        return self._deck

    #Utilisé en cas de sauvegarde du model (pour les simulations)
    @deck.setter
    def deck(self, value):
        self._deck = value
        
    @property
    def players_list(self):
        return self._players_list

    @property
    def player(self):
        return self._players_list.real_player
        
    @property
    def ia(self):
        return self._players_list.ia
    
    @property
    def current_player(self):
        return self._players_list.current
    
    @property
    def next_player(self):
        return self._players_list.next_player
        
    @property
    def victory(self):
        return self._victory
    
    @victory.setter
    def victory(self, value):
        self._victory=value
        
    @property
    def winner(self):
        return self._winner
        
    @property
    def cartes_defaussees(self):
        return self._cartes_defaussees
    
    @property
    def issimul(self):
        return self._issimul
    
    @issimul.setter
    def issimul(self, value):
        self._issimul = value
        
    @property
    def islearning(self):
        return self._islearning
        
    @property
    def current_state(self):
        return self._current_state
    
    @current_state.setter
    def current_state(self, value):
        self._current_state = value
        
    def add_defausse(self, card):
        self._cartes_defaussees.append(card)
                
    
    #Fonction permettant l'initialisation des données non persistantes (appel à chaque début de partie et début de round)
    def init_data(self,difficulty = -1):
        
        #Réinitialisation des données du round précédent
        self._cards_played = []
        self._cards_played_ia = []
        self._cards_played_player = []
        self._burnt_card = None
        self._deck = [] 
        self._victory = False
        self._cartes_defaussees = []
        self._current_state = None
        
        #Mélange des cartes
        shuffle(self._cards)
        
        #Création des joueurs si il s'agit d'un début de partie
        if difficulty != -1: #-1 veut dire qu'aucun argument n'a été envoyé à la fonction, ce qui veut dire qu'il s'agit d'un nouveau round et non d'une nouvelle 
                            #partie
            self.creer_joueurs(difficulty)
        else: #Nouveau round, on réinitialise donc la main de l'ia et du joueur
            self.ia.reset_values()
            self.player.reset_values()
            
        #distribution des cartes dans les différentes listes
        self.distribution()
        
        #Détermine le premier joueur aléatoirement
        premier_joueur = randrange(0,2)

        if premier_joueur == 0:
            self._players_list.current_node = self._players_list.real_player_node
        else:
            self._players_list.current_node = self._players_list.ia_node

        self._players_list.current.add_card(self.pick_card())

        if(self._islearning and difficulty != -1):
            self.play_simu()
            
        return self._players_list.current
        
    #Instanciation des joueurs
    def creer_joueurs(self, difficulty = 0):
        #Création du noeud contenant l'instance du vrai joueur
        player_node = player.Node(player.RealPlayer())
        
        #Création de l'instance de l'ia
        ia = None
        if difficulty == 0:
            ia = player.IAMoyenne(self)
        else:
            player_node = player.Node(player.IADifficile(self))
            ia = player.IADifficile(self)
            self._islearning = True
            
            
        #Création du noeud contenant l'instance de l'ia
        ia_node = player.Node(ia)
        
        #Définition de l'attribut next player des noeuds, qui est une référence du noeud du prochain joueur
        player_node.next_player = ia_node
        ia_node.next_player = player_node
        
        #Création de la liste circulaire chaînée
        self._players_list = player.CircleLinkedList(player_node, ia_node)
        
        
    
    #Distribution des cartes dans les différentes listes
    def distribution(self):
        self.player.add_card(self._cards[0]) #Une carte au joueur
        self.ia.add_card(self._cards[1]) #Une à l'IA
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
        if(self._deck):
            if(not self._issimul):
                return self._deck.pop(0)
        elif(self._victory is False):
            self.victory_emptydeck()
        
    
    #Fonction permettant de déterminer la fin de pioche lors de la simulation de l'IA, de simuler la pioche lors de la simulation de l'IA,
    #et permet également le bon déroulement de la simulation dans des cas de pioche particulieres (Prince et Chancelier)
    def pick_card_simu(self, card = None):
        #Lorsqu'on parcourt l'arbre de jeu, le joueur courant ne sait pas quelle carte est brulée. La carte peut donc théoriquement 
        #être piochée par le joueur adverse. Elle est donc mélangée à la pioche le temps de la simulation. Avoir une longueur de pioche de 1 pendant
        #la simulation signifie donc que la pioche serait vide hors simulation
        if(not self._deck or self._deck.__len__() == 1):
            self.victory_emptydeck()
        elif card is None:
            cards = self.get_drawable_cards()
            card_to_remove = list(cards.keys())[0]
            self._deck.remove(card_to_remove)
            return card_to_remove
        else:
            self._deck.remove(card)
    

    #Retourne les 3 première cartes de jeu (celles affichées au milieu du plateau)
    def get_three_cards(self):
        return str(self._cards_played[0]), str(self._cards_played[1]), str(self._cards_played[2])
    
    def play_simu(self):
        while(self.ia.score <= 2000):
            self.playAI()
            
            
    #Choix de la carte jouée par l'IA
    def playAI(self):
        
        #Si l'ia a une princesse elle n'est pas jouée
        if(isinstance(self.current_player.cards[0], cards.Princesse)):
            self.play(1)
            return
        elif(isinstance(self.current_player.cards[1], cards.Princesse)):
            self.play(0)
            return
        
        #Si l'ia possède une comtesse et un prince ou un roi, alors pas besoin de lancer la simulation, la comtesse est jouée
        play_comtesse = self.current_player.must_play_comtesse()
        if play_comtesse != -1:
            self.play(play_comtesse)
        else:
            index = self.ia.algorithme()
            #self.play(randrange(0,2))
            self.play(index)
        
    
    #Effectue l'action de la carte à l'index associée du joueur courrant
    def play(self, index):

        last_card_played = self.current_player.cards[index]
        self.current_player.add_cards_played(last_card_played)

        self.current_player.remove_card(last_card_played)#Suppression de la carte dans la main du joueur courrant
        self._cards_played.append(last_card_played)#Ajout de cette carte à la liste des cartes jouées
        last_card_played.action()#Action de la carte
        if(not self._victorylearning):
            self.next_player.immune = False
            self.current_player.last_card_played = last_card_played
           
            self.next_turn()
        else:
            self._victorylearning = False
        
        
            
    #Définition du prochain joueur
    def next_turn(self):
        
        self._players_list.next_turn() #On passe au prochain joueur
        
        temp = self.pick_card()
        if(self._victorylearning):
            self._victorylearning = False
        else:
            if(temp is not None):
                self.current_player.add_card(temp)
    
    #Fonction appelée lorsque la pioche est vide
    def victory_emptydeck(self):
        string_to_pass = ""
        
        #Exception à cause du cas du prince : dernière carte jouée est un prince donc l'un des deux joueurs n'a plus de carte en main
        if(self.player.cards.__len__() == 0):
            if(self.player.cards_played[self.player.cards_played.__len__() - 1].value() > self.ia.cards[0].value()):
                winner = self.player
                string_to_pass = "Pioche vide : \nJoueur a gagné car sa dernière carte jouée était plus forte"
            else:
                winner = self.ia
                string_to_pass = "Pioche vide : \nIA a gagné car sa dernière carte jouée était plus forte"
        elif(self.ia.cards.__len__() == 0):
            if(self.ia.cards_played[self.ia.cards_played.__len__() - 1].value() > self.player.cards[0].value()):
                winner = self.ia
                string_to_pass = "Pioche vide : \nIA a gagné car sa dernière carte jouée était plus forte"
            else:
                winner = self.player
                string_to_pass = "Pioche vide : \nJoueur a gagné car sa dernière carte jouée était plus forte"
        else:
            #Cas usuel
            if(self.ia.cards[0].value() > self.player.cards[0].value()):
                winner = self.ia
                string_to_pass = "Pioche vide : \nIA a gagné car sa carte était plus forte"
            else:
                winner = self.player
                string_to_pass = "Pioche vide : \nJoueur a gagné car sa carte était plus forte"

        #Victoire
        self.game_victory(winner, string_to_pass)
    
    #Fonction appelée chaque foiqu'il y a victoire
    def game_victory(self, winner, chaine):
        
        self._victory = True 
        
        self._winner = winner
        if(not self.issimul):
            #On affiche l'écran de fin de jeu en passant par le controller
            self._winner.win(1) #Le joueur ayant gagné gagne un point de score
            
            if(self.player.espionne_played):
                self.player.win(1)
                chaine += "\nVous avez joué l'espionne, vous gagnez\n1 jeton supplémentaire !"
            elif self.ia.espionne_played:
                self.ia.win(1)
                chaine+= "\nL'IA a joué l'espionne, elle gagne\n1 jeton supplémentaire :/"
            if(not self._islearning):
                self.controller.display_victory(chaine, [self.player.score, self.ia.score])
            else:
                self._victorylearning = True
                self.init_data()

    #Sauvegarde des variables
    def save_attributes(self):
        return {"Deck" : copy.copy(self._deck), "Cards played" : copy.copy(self._cards_played),
                "Victory" : self._victory}
        
    #Restauration des variables avec recopie de la sauvegarde afin de ne pas la corrompre
    def set_attributes(self, attributes):
        self._deck = copy.copy(attributes["Deck"])
        self._cards_played = copy.copy(attributes["Cards played"])
        self._victory = attributes["Victory"]
        
    
    #Fonction permettant de définir les cartes pouvant être piochée ainsi que leur probabilité d'être piochée
    def get_drawable_cards(self):
        drawable_cards = {}
        for card in self._deck:
            if(not any(isinstance(x, card.__class__) for x in drawable_cards)): #Vérifie si la carte possède déjà une instance dans la liste
                proba = sum(isinstance(x, card.__class__) for x in self._deck)/self._deck.__len__() #Calcul du pourcentage associé
                drawable_cards[card] = proba
                
            #Si la liste contient 10 cartes, elle contient tous les types de carte possible du jeu, on sort donc de la boucle
            if(drawable_cards.__len__() == 10):
                break
        return {k:v for k,v in sorted(drawable_cards.items(), key = lambda item:item[1], reverse = True)} #Tri du dictionnaire en fonction de ses valeurs (décroissant)
        #return drawable_cards


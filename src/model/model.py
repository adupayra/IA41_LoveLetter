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
import pickle

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
        cards.Card._model = self
        self._cartes_defaussees = [] #Cartes défaussées lorsque le prince est joué
        self._current_state = None
        self._issimul = False
        
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

    @deck.setter
    def deck(self, value):
        self._deck = value
        
    @property
    def players_list(self):
        return self._players_list
    
    @players_list.setter
    def players_list(self, value):
        self._players_list = value
    
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
    def cartes_defaussees(self):
        return self._cartes_defaussees
    
    @property
    def issimul(self):
        return self._issimul
    
    @issimul.setter
    def issimul(self, value):
        self._issimul = value
    
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

        return self._players_list.current
        
    #Instanciation des joueurs
    def creer_joueurs(self, difficulty = 0):
        #Création du noeud contenant l'instance du vrai joueur
        player_node = player.Node(player.RealPlayer())
        
        #Création de l'instance de l'ia
        ia = None
        if difficulty == 0:
            ia = player.IAFacile(self)
        elif difficulty == 1:
            ia = player.IAMoyenne(self)
        else:
            ia = player.IADifficile(self)
            
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
        #être piochée par le joueur adverse. Elle est donc mélangée à la pioche le temps de la simulation. Avoir une longueur de pioche de 1 signifie pendant
        #la simulation signifie donc que la pioche serait vide hors simulation
        if(not self._deck or self._deck.__len__() == 1):
            self.victory_emptydeck()
        elif card is None: #Cas particulier (prince et chancelier)
            return self._deck.pop(0)
        else:
            self._deck.remove(card)
            
        
            
        
    #Retourne les 3 première cartes de jeu (celles affichées au milieu du plateau)
    def get_three_cards(self):
        return str(self._cards_played[0]), str(self._cards_played[1]), str(self._cards_played[2])
    
    
    #Choix de la carte jouée par l'IA
    def playAI(self):
        #Test d'une simulation en depth 1, à modifier à terme
        if(self.issimul is False):
            self.issimul = True
            self.deck.append(self.burnt_card)
            state = State(self, self._current_state)
            self._current_state = state
            self._current_state.next_states()
            self.deck.remove(self.burnt_card)
            self.issimul = False
        #Appeler algo de l'IA ici
        self.play(randrange(0,2))
    
        
    
    #Effectue l'action de la carte à l'index associée du joueur courrant
    def play(self, index):
        last_card_played = self.current_player.cards[index]
        self.current_player.add_cards_played(last_card_played)

        self.current_player.remove_card(last_card_played)#Suppression de la carte dans la main du joueur courrant
        self._cards_played.append(last_card_played)#Ajout de cette carte à la liste des cartes jouées
        last_card_played.action()#Action de la carte
        self.current_player.last_card_played = last_card_played
        self.next_turn()
        
        return self.current_player
        
            
    #Définition du prochain joueur
    def next_turn(self):
        
        self._players_list.next_turn() #On passe au prochain joueur
        temp = self.pick_card()
        if(temp is not None):
            self.current_player.add_card(temp)
    
    #Fonction appelée lorsque la pioche est vide
    def victory_emptydeck(self):
        string_to_pass = ""
        
        #Exception à cause du cas du prince : dernière carte jouée est un prince donc l'un des deux joueurs n'a plus de carte en main
        if(self.player.cards.__len__() == 0):
            if(self.cards_played_player[self.cards_played_player.__len__() - 1].value() > self.ia.cards[0].value()):
                winner = self.player
                string_to_pass = "Pioche vide : \nJoueur a gagné car sa dernière carte jouée était plus forte"
            else:
                winner = self.ia
                string_to_pass = "Pioche vide : \nIA a gagné car sa dernière carte jouée était plus forte"
        elif(self.ia.cards.__len__() == 0):
            if(self.cards_played_ia[self.cards_played_ia.__len__() - 1].value() > self.player.cards[0].value()):
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
        
        if(not self.issimul):
            #On affiche l'écran de fin de jeu en passant par le controller
            winner.win(1) #Le joueur ayant gagné gagne un point de score
            self.controller.display_victory(chaine, [self.player.score, self.ia.score])
        
    #Permet la sauvegarde des attributs de l'environnements rattachés à la classe du modèle afin de ne pas les perdre lorsque l'on effectue la recherche dans l'arbre
    #de jeu
    def save_attributes(self):
        return (copy.copy(self._cards_played), copy.copy(self._deck), copy.copy(self._victory), copy.copy(self._cartes_defaussees))
    
    #Récupération des attributs
    def set_attributes(self, attributes):
        self._cards_played = attributes[0]
        self._deck = attributes[1]
        self._victory = attributes[2]
        self._cartes_defaussees = attributes[3]
    
class State():
    
    
    def __str__(self):
        return ("State : " + str(self._current_player) + "\nCards played : " + str(self._model.cards_played) + 
                "\nNumber of remaining cards : " + str(self._cards_remained) + "\nPossible cards enemy can play " + str(self._possible_cards) +
                "\nHand : " + str(self._current_player.cards) + "\nDeck : " + str(self._model.deck) +
                 "\nBurnt card : " + str(self._model.burnt_card) + "\nOpponent's card : " + str(self._opponent.cards) + "\n")

    def __init__(self, model, parent):
        self._save = Save()
        self._model = model
        self._current_player = model.current_player
        self._opponent = model.next_player

        self._cards_remained = model.deck.__len__()
        
        self._possible_cards = self.get_possible_cards()
        
        
        
        
        self._parent = parent
        
    def next_states(self): 
        #On boucle sur les cartes du joueur courant, pour chaque carte, on boucle sur toutes les cartes possibles que le prochain joueur peut piocher
        for i in range(0, self._model.current_player.cards.__len__()) :
            for card in self._possible_cards:
                    self._save.save(self._model) #Sauvagarde de l'environnement
                    
                    #Simulation
                    self._opponent.add_card(card)
                    self._model.pick_card_simu(card)
                    self._model.play(i)
                    
                    #Génération de l'état correspondant
                    state = State(self._model, self)

                    self._save.backup() #Restauration de lenvironnement
                    
                    

    #retourne une liste contenant une instance de chaque carte pouvant être piochée par le prochain joueur    
    def get_possible_cards(self):
        possible_cards = []
        for card in self._model.deck:
            if(not any(isinstance(x, card.__class__) for x in possible_cards)):
                possible_cards.append(card)
            if(possible_cards.__len__() == 10):
                break
        return possible_cards

        
class Save():
    '''
    Classe permettant de sauvegarder l'état courant du jeu lors d'une simulation. Cette manière de faire est loin d'être la meilleure, implémenter un command 
    pattern aurait été plus bénéfique, bien que rendant l'architecture des fichiers moins lisibles
    '''
    #Copie de l'environnement courant 
    def save(self, model):
        self._model = model
        
        self._ia_save = self._model.ia.save_attributes()
        self._player_save = self._model.player.save_attributes()
        self._model_save = self._model.save_attributes()
        
    #Restauration de l'environnement
    def backup(self):
        self._model.players_list.next_turn()
        
        self._model.ia.set_attributes(self._ia_save)
        self._model.player.set_attributes(self._player_save)
        self._model.set_attributes(self._model_save)


        
        
        
         
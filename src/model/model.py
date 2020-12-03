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
from prompt_toolkit.key_binding.bindings.named_commands import self_insert

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
            self._cards.append(cards.Garde(self))

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
            return self._deck.pop(0)
        elif(self._victory is False):
            self._victory = True
            self.victory_emptydeck()
            
        
    #Retourne les 3 première cartes de jeu (celles affichées au milieu du plateau)
    def get_three_cards(self):
        return str(self._cards_played[0]), str(self._cards_played[1]), str(self._cards_played[2])
    
    
    #Choix de la carte jouée par l'IA
    def playAI(self):
        self.issimul = True
        '''
        file = open("test.b", "wb")
        pickle.dump(self, file)
        file.close()
        '''
        
        state = State(self, self._current_state)
        self._current_state = state
        self._current_state.next_states()
        
        '''
        file2 = open("test.b", "rb")
        self = pickle.load(file2)
        file2.close()
        print(self._cards_played)'''
        
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
        self.issimul = False
        self.current_player.last_card_played = last_card_played
        self.next_turn()
        
        return self.current_player
        
            
    #Définition du prochain joueur
    def next_turn(self):
        
        self._players_list.next_turn() #On passe au prochain joueur
        self.current_player.add_card(self.pick_card())
    
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
        winner.win(1) #Le joueur ayant gagné gagne un point de score
        self._victory = True 
        
        if(not self.issimul):
            #On affiche l'écran de fin de jeu en passant par le controller
            self.controller.display_victory(chaine, [self.player.score, self.ia.score])
        
        
    def save_attributes(self):
        return (copy.copy(self._cards_played), copy.copy(self._deck), copy.copy(self._victory))
    
    def set_attributes(self, attributes):
        self._cards_played = attributes[0]
        self._deck = attributes[1]
        self._victory = attributes[2]
    
class State():
    
    def __init__(self, model,parent):
        self._model = model
        self._current_player = model.current_player
        '''
        self._current_player = copy.deepcopy(model.current_player)
        self._opponent = copy.deepcopy(model.next_player)
        self._cards_played = copy.copy(model.cards_played)
        self._deck = copy.copy(model.deck)'''
        self._hand = self._current_player.cards
        
        self._save = Save()
        self._parent = parent
        
    def next_states(self): 
       
        for i in range(0, self._hand.__len__()) :
            print(self._model.ia.cards)
            self._save.save(self._model)
            print(self._model.current_player)
            self._model.play(i)
            state = State(self._model, self)
            self._save.backup()



        
class Save():


    def save(self, model):
        self._model = model
        #Copie de l'environnement courant 
        self._ia_save = model.ia.save_attributes()
        self._player_save = model.player.save_attributes()
        self._model_save = self._model.save_attributes()
        
    def backup(self):
        self._model.players_list.next_turn()
        
        self._model.ia.set_attributes(self._ia_save)
        self._model.player.set_attributes(self._player_save)
        self._model.set_attributes(self._model_save)
        

        
        
        
         
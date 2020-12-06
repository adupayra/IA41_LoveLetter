# -*- coding: utf-8 -*-
'''
Created on 28 oct. 2020

@author: Antoine
'''

import abc
from abc import abstractmethod
import copy
import random
import src.model.cards as cards

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
        self._cards_played = []
    
    @property
    def next_player(self):
        return self._next_player
    
    @next_player.setter
    def next_player(self, next_player):
        self._next_player = next_player
        
    @property
    def player(self):
        return self._player
    
    @player.setter
    def player(self,value):
        self._player = value
    
    

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
        self._last_card_played = None
        self._cards_to_string = []
        self._immune = False
        self._play_chancelier = False
        self._cards_played = []
        self._espionne_played = False
        self._knows_card = False
    
    #Permet de sauvegarder l'état du joueur dans le cas d'une simulation
    def save_attributes(self):
        return {"Cards" : copy.copy(self._cards), "Cards played" : copy.copy(self._cards_played)}
    
    #Restauration de la sauvegarde
    def set_attributes(self, attributes):
        self._cards = attributes["Cards"] 
        
        self._cards_played = attributes["Cards played"] 
        '''
        self._last_card_played = attributes["Last card played"] 
        self._immune = attributes["Immune"]
        self._espionne_played = attributes["Espionne played"]
        self._knows_card = attributes["Knows card"]
        self._play_chancelier = attributes["Play chancelier"]
        '''
    @property
    def espionne_played(self):
        return self._espionne_played
    
    @espionne_played.setter
    def espionne_played(self, value):
        self._espionne_played = value
        
    @property
    def knows_card(self):
        return self._knows_card
    
    @knows_card.setter
    def knows_card(self, value):
        self._knows_card = value
        
    @property
    def cards(self):
        return self._cards
    
    @cards.setter
    def cards(self,value):
        self._cards = copy.copy(value)

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
    
    @property
    def play_chancelier(self):
        return self._play_chancelier
    
    @play_chancelier.setter
    def play_chancelier(self, value):
        self._play_chancelier = value
        
    
    def win(self, value):
        self._score += value
        
    def add_card(self, new_card):
        self._cards.append(new_card)
        
    def remove_card(self, card):
        self._cards.remove(card)
        
    def reset_values(self):
        self._cards = []
        self._last_card_played = None
        self._immune = False
        self._cards_played = []
    
    
    @property
    def cards_played(self):
        return self._cards_played
    
    @cards_played.setter
    def cards_played(self, value):
        self._cards_played = value
    
    def add_cards_played(self, card):
        self._cards_played.append(card)

    
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
        self._depth = 1
    
    def __str__(self):
        return "IA Facile"
    
    def algorithme(self):
        self._model.deck.append(self._model.burnt_card)
        state = State(self._model, self._model.current_state)
        value, card = self.max_val(state, 2)
        print(value)
        print(card)
        index = self.cards.index(card)
        self._model.current_state = state
        self._model.deck.remove(self._model.burnt_card)
        print(self._model.deck)
        return index
    
    def algorithmeGuard(self):
        pass
    
    def algorithmePrince(self):
        pass
    
    def algorithmeChancelier(self):
        pass
    
    def minmax(self, depth):
        pass
    
    def max_val(self, state, depth):
        if state.is_final or depth == 0:
            return state.eval(), state.last_card_played
        print(state)
        last_card_played = None
        value = -10
        for s in state.next_states():
            print(s)
            temp, last_card_played = self.min_val(s, depth-1)
            value = max(temp, value)
        
        return value, last_card_played
    
    def min_val(self, state, depth):
        if(state.is_final or depth == 0):
            return -state.eval(), state.last_card_played
        
        last_card_played = None
        value = 10
        for s in state.next_states():
            temp, last_card_played = self.max_val(s, depth-1)
            value = min(value, temp)
            
        return value, last_card_played
            
        
            
    
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
    
class State():
    
    
    def __str__(self):
        return ("State : " + str(self._current_player) + "\nProbability : " + str(self._probability) + "\nCards played : " + str(self._save.get_ia_save("Cards played")) + 
                "\nNumber of remaining cards : " + str(self._cards_remained) + "\nPossible cards enemy can play " + str(self._possible_cards) +
                "\nHand : " + str(self._save.get_ia_save("Cards")) + "\nDeck : " + str(self._save.get_model_save("Deck")) +
                 "\nBurnt card : " + str(self._model.burnt_card) + "\nOpponent's card : " + str(self._save.get_player_save("Cards")) + "\nCard played by opponent " +
                 str(self._last_card_played) + "\n")

    def __init__(self, model, parent, probability = 1):
        
        self._model = model
        self._save = Save(self._model)
        self._current_player = model.current_player
        self._opponent = model.next_player
        
        self._last_card_played = self._opponent.last_card_played
        self._cards_remained = model.deck.__len__()
        
        self._possible_cards = self.get_possible_cards()
        
        self._probability = probability
        
        self._parent = parent
       
    @property
    def is_final(self):
        if(self._model.victory):
            return True
        else:
            return False
    @property
    def last_card_played(self):
        return self._last_card_played
    
    @property
    def save(self):
        return self._save
    
    def next_states(self): 
       
        drawable_cards = self.get_drawable_cards()
        states = []
        #On boucle sur les cartes du joueur courant, pour chaque carte, on boucle sur toutes les cartes possibles que le prochain joueur peut piocher
        for i in range(0, self._model.current_player.cards.__len__()) :
            for card in drawable_cards:
                
                self._save.save() #Sauvagarde de l'environnement
                #Simulation
                self._opponent.add_card(card)
                self._model.pick_card_simu(card)
                self._model.play(i)
                
                #Génération de l'état correspondant
                state = State(self._model, self, drawable_cards[card])
                states.append(state)
                self._save.backup() #Restauration de lenvironnement
                
                    
        return states

    #retourne une liste contenant une instance de chaque carte pouvant être piochée par le prochain joueur    
    def get_possible_cards(self):
        possible_cards = []
        self._model.deck.append(self._opponent.cards[0])
        for card in self._model.deck:
            if(not any(isinstance(x, card.__class__) for x in possible_cards)):
                possible_cards.append(card)
            if(possible_cards.__len__() == 10):
                break
        self._model.deck.remove(self._opponent.cards[0])
        return possible_cards
    
    def get_drawable_cards(self):
        drawable_cards = {}
        for card in self._model.deck:
            if(not any(isinstance(x, card.__class__) for x in drawable_cards)):
                proba = sum(isinstance(x, card.__class__) for x in self._model.deck)/self._model.deck.__len__()
                drawable_cards[card] = proba
            if(drawable_cards.__len__() == 10):
                break
        return {k:v for k,v in sorted(drawable_cards.items(), key = lambda item:item[1], reverse = True)}
    
    def eval(self):
        if(self._model.victory):
            return 1
        else:
            return self._probability
        
class Save():
    '''
    Classe permettant de sauvegarder l'état courant du jeu lors d'une simulation. Cette manière de faire est loin d'être la meilleure, implémenter un command 
    pattern aurait été plus bénéfique, bien que rendant l'architecture des fichiers moins lisibles
    '''
    def __init__(self, model):
        self._model = model
        self._ia_save = {}
        self._player_save = {}
        self._model_save = {}
        self._ia_save = model.current_player.save_attributes()
        self._player_save = model.next_player.save_attributes()
        self._model_save = model.save_attributes()
        
    #Copie de l'environnement courant 
    def save(self):
        
        self._ia_save = self._model.current_player.save_attributes()
        self._player_save = self._model.next_player.save_attributes()
        self._model_save = self._model.save_attributes()
        
        
    def get_ia_save(self, key):
        return self._ia_save[key]
    
    def get_player_save(self, key):
        return self._player_save[key]
    
    def get_model_save(self, key):
        return self._model_save[key]
    
    #Restauration de l'environnement
    def backup(self):
        self._model.players_list.next_turn()
        
        self._model.ia.set_attributes(self._ia_save)
        self._model.player.set_attributes(self._player_save)
        self._model.set_attributes(self._model_save)
        
        self.save()

    

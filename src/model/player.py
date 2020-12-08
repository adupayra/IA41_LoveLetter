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
        self._next_player = None

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
        self._knows_card = [False, None]
    
    def save_attributes(self):
        #Sauvegarde des variables
        return {"Cards" : copy.copy(self._cards), "Cards played" : copy.copy(self._cards_played), "Immune" : self._immune, "Espionne played" : self._espionne_played, 
                "Knows card" : copy.deepcopy(self._knows_card)}
    
    def set_attributes(self, attributes):
        #Restauration des variables avec recopie de la sauvegarde (afin de ne pas la corrompre)
        self._cards = copy.copy(attributes["Cards"])
        self._cards_played = copy.copy(attributes["Cards played"])
        self._immune = attributes["Immune"]
        self._espionne_played = attributes["Espionne played"]
        self._knows_card = copy.deepcopy(attributes["Knows card"])
       
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
        self._knows_card[0] = value[0]
        self._knows_card[1] = value[1]
        
    @property
    def cards(self):
        return self._cards

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
    def immune(self, value):
        self._immune = value
    
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
        self._espionne_played = False
        self._knows_card[0] = False
        self._knows_card[1] = None
    
    #Fonction utilisée pour vérifier si le joueur possède la comtesse et le roi ou le prince
    def must_play_comtesse(self):
        if (any(isinstance(x, cards.Comtesse) for x in self._cards)):
            if(any(isinstance(y, cards.Roi) or isinstance(y, cards.Prince) for y in self._cards)):
                if(isinstance(self._cards[0], cards.Comtesse)): 
                    return 0
                else: return 1
        return -1
        
    @property
    def cards_played(self):
        return self._cards_played
    
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
    
    #Algorithme de décision de la carte à jouer de l'IA facile
    def algorithme(self):
        
        self._model.deck.append(self._model.burnt_card) #Ajout de la carte brûlée à la pioche car le joueur ne connaît pas cette carte. Elle doit donc être théoriquement piochable
        
        state = State(self._model, None) #Etat courant
 
        (value, best_state) = self.max_val(state, 2) #Appel de l'algorithme minmax qui va nous retourner la valeur du meilleur état ainsi que l'état correspondant
        
        print(value)

        #Grâce à l'état trouvé avec le minmax, on retrouve la carte à jouer menant à cet état
        while(best_state.parent is not state):
            best_state = best_state.parent
        index = 0
        if(isinstance(self._cards[0], best_state.last_card_played.__class__)):
            index = 0
        else:
            index = 1
        
        
        self._model.current_state = state
        self._model.deck.remove(self._model.burnt_card) #On retire la carte brûlée
        
        return index
    
    def algorithmeGuard(self):
        pass
    
    def algorithmePrince(self):
        pass
    
    def algorithmeChancelier(self):
        pass
    
    def minmax(self, depth):
        pass
    
    #Algorithme classique d'un noeud max
    def max_val(self, state, depth):
        #Condition d'arrêt
        if state.is_final or depth == 0:
            return (state.eval(), state.parent)
        print(state)
        
        value = (-10, None)
        for s in state.next_states():
            print(s)
            temp = self.min_val(s, depth-1)
            value = max(temp, value, key = lambda x:x[0]) #Puisqu'on a un couple (valeur, état parent), on cherche le maximum des deux couples en fonction de la valeur
        
        return value
    
    #Algorithme classique d'un noeud min
    def min_val(self, state, depth):
        #Condition d'arrêt
        if(state.is_final or depth == 0):
            return (-state.eval(), state.parent)
        
        value = (10,None)
        
        for s in state.next_states():
            print(s)
            temp = self.max_val(s, depth-1)
            value = min(value, temp, key = lambda x:x[0]) #Puisqu'on a un couple (valeur, état parent), on cherche le minimum des deux couples en fonction de la valeur
            
        return value
            
        
            
    
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
        return ("State : " + str(self._probability) + "\n" + str(self._model.current_player) + "\nCards remained : " + str(self._cards_remained)+
                "\nCards played by current : " + str(self._model.current_player.cards_played) +
                "\nLast card played by current : " + str(self._model.current_player.last_card_played) + "\nHand : " + str(self._model.current_player.cards) + 
                "\nOpponent's cards played : " + str(self._model.next_player.cards_played) + "\nLast card played in game : " + 
                str(self._last_card_played) + "\nOpponent's hand : " + str(self._model.next_player.cards) + 
                "\nDeck : " + str(self._model.deck) + "\nPossible cards : " + str(self._possible_cards) + "\nKnows card : " + str(self._current_player.knows_card[0])
                + "\nOpponent knowscard : " + str(self._model.next_player.knows_card[0]) + "\nCurrent immune : " + str(self._current_player.immune) +
                "\nOpponent immune : " + str(self._opponent.immune) + "\nCurrent espionne : " + str(self._model.current_player.espionne_played) +
                "\nOpponent espionne : " + str(self._model.next_player.espionne_played) + "\n")
        
        

    def __init__(self, model, parent, probability = 1):
        
        self._save = Save(model)
        self._model = self._save.get_model()
        
        self._current_player = self._model.current_player
        self._opponent = self._model.next_player

        self._last_card_played = self._opponent.last_card_played
        self._cards_remained = self._model.deck.__len__()

        self._possible_cards = self.get_possible_cards()
        
        self._parent = parent
        
        self._probability = probability
        
    @property
    def parent(self):
        return self._parent
    
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
        
        play_comtesse = self._current_player.must_play_comtesse()
        if play_comtesse != -1:
            self.play_simu(states, drawable_cards, play_comtesse)
        else:
            #On boucle sur les cartes du joueur courant, pour chaque carte, on boucle sur toutes les cartes possibles que le prochain joueur peut piocher
            for i in range(0, self._model.current_player.cards.__len__()) :
                self.play_simu(states, drawable_cards, i)
            
        return states
    
    def play_simu(self, states, drawable_cards, i):
        for card in drawable_cards:
            #Simulation
            self._opponent.add_card(card)
            self._model.pick_card_simu(card)
            self._model.play(i)
            #Génération de l'état correspondant
            state = State(self._model, self, drawable_cards[card])
            states.append(state)
            
            #Restauration de l'environnement
            self._save.backup() 
                
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
    
    #Fonction permettant de définir les cartes pouvant être piochée ainsi que leur probabilité d'être piochée
    def get_drawable_cards(self):
        drawable_cards = {}
        for card in self._model.deck:
            if(not any(isinstance(x, card.__class__) for x in drawable_cards)): #Vérifie si la carte possède déjà une instance dans la liste
                proba = sum(isinstance(x, card.__class__) for x in self._model.deck)/self._model.deck.__len__() #Calcul du pourcentage associé
                drawable_cards[card] = proba
                
            #Si la liste contient 10 cartes, elle contient tous les types de carte possible du jeu, on sort donc de la boucle
            if(drawable_cards.__len__() == 10):
                break
        return {k:v for k,v in sorted(drawable_cards.items(), key = lambda item:item[1], reverse = True)} #Tri du dictionnaire en fonction de ses valeurs (décroissant)
            
    def eval(self):
        if(self._model.victory):
            return 1
        else:
            return self._probability
        
class Save():
    '''
    Classe permettant de sauvegarder l'état courant du jeu lors d'une simulation. Cette manière de faire est loin d'être la meilleure, implémenter un command 
    pattern aurait été plus bénéfique, bien que rendant l'architecture des fichiers moins lisible
    '''
    def __init__(self, model):
        #Création d'un environnement propre à l'état courant, afin de ne pas manipuler l'environnement hors de l'état courant
        self._model = copy.deepcopy(model)
        
        self._current_player = self._model.current_player
        self._next_player = self._model.next_player
        
        #Sauvagarde des éléments de l'environnement
        self._modelsave = self._model.save_attributes()
        self._current_player_save = self._model.current_player.save_attributes()
        self._next_player_save = self._model.next_player.save_attributes()
        
    def get_model(self):
        return self._model

    #Restauration de l'environnement
    def backup(self):
        
        self._current_player.set_attributes(self._current_player_save)
        self._next_player.set_attributes(self._next_player_save)
        self._model.set_attributes(self._modelsave)
        
        #La restauration ne se fait que sur les listes de carte, il faut revenir au joueur courant manuellement
        self._model.players_list.next_turn()
        

    

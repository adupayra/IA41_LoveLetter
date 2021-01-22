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
        The constructor will allow the instantiation of all the cards, only persistant data of the program (So that we don't have to instantiate again every card
        at every beginning of game/start of round)
        '''
        
        #Definition of the different attributes
        self._controller = controller
        self._cards = [] #List of all cards
        self._cards_played = [] #List of the played cards (contains the 3 cards of the beginning)
        self._burnt_card = None #The unknown card
        self._deck = [] #The deck
        self._players_list = None #Linked list containing the current player, the real player and the AI
        self._victory = False
        self._winner = None
        cards.Card._model = self
        self._cartes_defaussees = [] #Thrown cards when the prince is played
        self._current_state = None
        self._issimul = False
        self._islearning = False
        self._victorylearning= False
        
        #Instantiation of all the cards
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
    
    #Used in case of save of the model (during the simulations)
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

    #Used in case of save of the model (during the simulations)
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
                
    #Function used for the initialization of non persistant data (called at each beginning of round)
    def init_data(self,difficulty = -1):
        
        #Reset the data of the precedant round
        self._cards_played = []
        self._cards_played_ia = []
        self._cards_played_player = []
        self._burnt_card = None
        self._deck = [] 
        self._victory = False
        self._cartes_defaussees = []
        self._current_state = None
        
        #Shuffle the cards
        shuffle(self._cards)
        
        #Creation of the players if it is the beginning of a game
        if difficulty != -1: #-1 means that no parameters wer passed to the function, which means that it's a new round an not a new game
            self.creer_joueurs(difficulty)
        else: #New round, we reset the AI and user's hands
            self.ia.reset_values()
            self.player.reset_values()
            
        #Share the cards in the differnt lists
        self.distribution()
        
        #Tells randomly the first player
        premier_joueur = randrange(0,2)

        if premier_joueur == 0:
            self._players_list.current_node = self._players_list.real_player_node
        else:
            self._players_list.current_node = self._players_list.ia_node

        self._players_list.current.add_card(self.pick_card())

        if(self._islearning and difficulty != -1):
            self.play_simu()
            
        return self._players_list.current
    
    #Instantiates the players
    def creer_joueurs(self, difficulty = 0):
        #Creation of a node containing the instance of the user
        player_node = player.Node(player.RealPlayer())
        
        #Creation of the AI
        ia = None
        if difficulty == 0:
            ia = player.IAMoyenne(self)
        else:
            player_node = player.Node(player.IADifficile(self))
            ia = player.IADifficile(self)
            self._islearning = True
            
            
        #Creation of the node containing the instance of the AI
        ia_node = player.Node(ia)
        
        #Definition of the next player's attribute of the nodes, who is a reference of the node of the next player
        player_node.next_player = ia_node
        ia_node.next_player = player_node
        
        #Creation of the circular linked list
        self._players_list = player.CircleLinkedList(player_node, ia_node)
        
        
    #Distribution of the cards in the differnt lists
    def distribution(self):
        self.player.add_card(self._cards[0]) #A card for the player
        self.ia.add_card(self._cards[1]) #One for the AI
        self._burnt_card = self._cards[2] #The cazrd which will remain hidden during the game
        
        #The 3 visible cards of the beginning
        self._cards_played.append(self._cards[3]) 
        self._cards_played.append(self._cards[4])
        self._cards_played.append(self._cards[5])
        
        #The deck
        for i in range (6, self._cards.__len__()):
            self._deck.append(self._cards[i])
        
    #Adds a card to the list of the played cards during the round
    def add_cards_played(self, new_card):
        self._cards_played.append(new_card)
    
    #Draws a card
    def pick_card(self):
        if(self._deck):
            if(not self._issimul):
                return self._deck.pop(0)
        elif(self._victory is False):
            self.victory_emptydeck()
        
    #Function used to determine the end of the deck when simulating an AI's play, to simulate the deck when the the AI is simulating, and to allow the good process of
    #the simulation in the cases of particular draw of cards (Prince and Counselor)
    def pick_card_simu(self, card = None):
        #When going through the game's tree, the current player doesn't know which card is burnt. The card can therefore theoretically be drawned by the opponent's 
        #player. It is therefore placed inside the deck during the simulation. Having a deck's lenght of 1 during the simulation then means that the deck would
        #be empty outside the simulation
        if(not self._deck or self._deck.__len__() == 1):
            self.victory_emptydeck()
        elif card is None:
            cards = self.get_drawable_cards()
            card_to_remove = list(cards.keys())[0]
            self._deck.remove(card_to_remove)
            return card_to_remove
        else:
            self._deck.remove(card)
    
    #Returns the 3 first cards (the one displayed in the middle of the board)
    def get_three_cards(self):
        return str(self._cards_played[0]), str(self._cards_played[1]), str(self._cards_played[2])
    
    def play_simu(self):
        while(self.ia.score <= 2000):
            self.playAI()
            
    #Chosing of the card played by the AI
    def playAI(self):
        index = self.ia.algorithme()
        #self.play(randrange(0,2))
        self.play(index)
        
    #Performs the action of the card at the given index of the current player
    def play(self, index):
        last_card_played = self.current_player.cards[index]
        self.current_player.add_cards_played(last_card_played)

        self.current_player.remove_card(last_card_played)#Removes the card in the hand of the current player
        self._cards_played.append(last_card_played)#Adds the card to the list of played cards
        last_card_played.action()#Action of the card
        if(not self._victorylearning):
            self.next_player.immune = False
            self.current_player.last_card_played = last_card_played
           
            self.next_turn()
        else:
            self._victorylearning = False
        
        
    #Decides the next player
    def next_turn(self):
        
        self._players_list.next_turn() #Next player
        
        temp = self.pick_card()
        
        if(self._victorylearning):
            self._victorylearning = False
        else:
            if(temp is not None):
                self.current_player.add_card(temp)
    
    #Function called when the deck is empty
    def victory_emptydeck(self):
        string_to_pass = ""
        
        #Exception due to the prince's case : last card played is a prince therefore one of the player has no cards left in it hand
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
            #Usual case
            if(self.ia.cards[0].value() > self.player.cards[0].value()):
                winner = self.ia
                string_to_pass = "Pioche vide : \nIA a gagné car sa carte était plus forte"
            else:
                winner = self.player
                string_to_pass = "Pioche vide : \nJoueur a gagné car sa carte était plus forte"

        #Victory
        self.game_victory(winner, string_to_pass)
    
    #Function called each time there's victory
    def game_victory(self, winner, chaine):
        
        self._victory = True 
        
        self._winner = winner
        if(not self.issimul):
            #We display the end game screen thanks to the controller
            self._winner.win(1) #The player which won gets a point
            
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
                
    #Save the variables
    def save_attributes(self):
        return {"Deck" : copy.copy(self._deck), "Cards played" : copy.copy(self._cards_played),
                "Victory" : self._victory}
        
    #Reset the variables and copies the save in order not to corupt them
    def set_attributes(self, attributes):
        self._deck = copy.copy(attributes["Deck"])
        self._cards_played = copy.copy(attributes["Cards played"])
        self._victory = attributes["Victory"]
        
    #Function used to define the cards which can be drawned and their probability to be drawned
    def get_drawable_cards(self):
        drawable_cards = {}
        for card in self._deck:
            if(not any(isinstance(x, card.__class__) for x in drawable_cards)): #Checks whether the card already has an instance in the list or not
                proba = sum(isinstance(x, card.__class__) for x in self._deck)/self._deck.__len__() #Compute associated percentage
                drawable_cards[card] = proba
            
            #If the list contains 10 cards, then it contains every possible types of cards, therefore we leave the loop
            if(drawable_cards.__len__() == 10):
                break
        return {k:v for k,v in sorted(drawable_cards.items(), key = lambda item:item[1], reverse = True)} #Sort dictionnary thanks to its values (Decreasingly)
        #return drawable_cards


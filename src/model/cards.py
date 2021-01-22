# -*- coding: utf-8 -*-
'''
Created on 27 oct. 2020

@author: Antoine
'''

import abc
from abc import abstractmethod
import src.model.player as player
from random import randrange

class Card(metaclass = abc.ABCMeta):
    '''
    template for every cards of the game
    '''
    
    _model = None
    
    #Used to print a card
    def __repr__(self):
        return self.__str__()
    
    def __init__(self, model):
        self._model = model
    
    #Property of the cards (value)
    @property
    @abstractmethod
    def value(self):
        pass
    
    #Action performed by the card once played
    @abstractmethod
    def action(self):
        #If the opponent knew the current player's card, then he doesn't know it anymore
        if self._model.next_player.knows_card[0] and isinstance(self, self._model.next_player.knows_card[1]):
            self._model.next_player.knows_card = [False, None]
    
class TwoActionCards(Card, metaclass = abc.ABCMeta):
    '''
    Parent abstract class of the classes which performs two actions on the point of view of the user (Chose the card -> second choice -> action on the model)
    '''
    
    def __init__(self, model):
        Card.__init__(self, model)
    
    @abstractmethod 
    def action(self):
        Card.action(self)
        
    @abstractmethod
    def deuxieme_action(self):
        pass
    
    
class Espionne(Card):
    '''
    Class defining the spy card
    '''
    
    #Used to print Espionne instead of the reference to the object in memory
    def __str__(self):
        return "Espionne"
    
    
    def __init__(self, model):
        Card.__init__(self, model)
    
    @classmethod
    def value(cls):
        return 0
     
    def action(self):
        Card.action(self)
        current = self._model.current_player
        next_player = self._model.next_player
        if(not current.espionne_played and not next_player.espionne_played):
            current.espionne_played = True
        elif not current.espionne_played and next_player.espionne_played:
            next_player.espionne_played = False
    
    
class Garde(TwoActionCards):
    '''
    Class defining the guard card
    '''
    
    def __str__(self):
        return "Garde"
    
    def __init__(self, model):
        Card.__init__(self, model)
    
    @classmethod
    def value(cls):
        return 1
    _model=None
     
    def action(self):
        TwoActionCards.action(self)
        if(not self._model.next_player.immune):
            Garde._model=self._model
            #Checks the current player in order to display or not something on the GUI
            if(isinstance(self._model.current_player, player.IAMoyenne) or self._model.issimul):
                
                guess=self._model.current_state.evalgarde(False)
                #print(guess)
                array = [Espionne.__name__, Pretre.__name__, Baron.__name__, Servante.__name__, Prince.__name__, Chancelier.__name__, Roi.__name__, 
                         Comtesse.__name__, Princesse.__name__]
                if(not self._model.issimul):
                    self._model.controller.display_guard_ialabel(array[guess]) #Displays the recapitulative label
                
                self.deuxieme_action(array[guess])
                    
            else:
                self._model.controller.display_guard_choice()
                    
                
                
            
    #Action performed once the card to guess has been chosen
    @classmethod
    def deuxieme_action(cls, chosen_card):
        if(chosen_card == str(cls._model.next_player.cards[0])):
            cls._model.game_victory(cls._model.current_player, str(cls._model.current_player) +" gagne un point en ayant deviné la carte avec le garde !") 
            
    
class Pretre(Card):
    '''
    Class defining the Priest card
    '''
    
    def __str__(self):
        return "Pretre"
    
    def __init__(self, model):
        Card.__init__(self, model)
    
    @classmethod
    def value(cls):
        return 2
    
     
    def action(self):
        Card.action(self)
        if(not self._model.next_player.immune):
            #Indicates that the current player knows the opponent's card, also indicates the instance of this card
            self._model.current_player.knows_card = [True,self._model.next_player.cards[0].__class__]
            if(isinstance(self._model.current_player, player.RealPlayer) and not self._model.issimul): #Don't display in simulation
                self._model.controller.display_AI_card(self._model.ia.cards[0])

            
            
class Baron(Card):
    '''
    Class defining the Baron's card
    '''
    
    def __str__(self):
        return "Baron"
    
    def __init__(self, model):
        Card.__init__(self, model)
    
    @classmethod
    def value(cls):
        return 3
    
     
    def action(self):
        Card.action(self)
        if(not self._model.next_player.immune):
            
            #Caching the values which we will use a lot in the function
            current_player = self._model.current_player
            next_player= self._model.next_player
            
            #Victory string
            chaine = " gagne 1 point, grâce à un baron"
        
            if(not self._model.issimul):
                self._model.controller.display_baron(current_player.cards[0], next_player.cards[0])
            
            #Check the winner
            if(current_player.cards[0].value() > next_player.cards[0].value()):
                self._model.game_victory(current_player, str(current_player) + chaine)                     
            elif(current_player.cards[0].value() < next_player.cards[0].value()):
                self._model.game_victory(next_player, str(next_player) + chaine)
            
        
        
class Servante(Card):
    '''
    Class defining the servant's card
    '''
    def __str__(self):
        return "Servante"
    
    def __init__(self, model):
        Card.__init__(self, model)
    
    @classmethod
    def value(cls):
        return 4
    
     
    def action(self):
        Card.action(self)
        self._model.current_player.immune = True
    
class Prince(TwoActionCards):
    '''
    Class defining the Prince's card
    '''
    
    def __str__(self):
        return "Prince"
    
    def __init__(self, model):
        Card.__init__(self, model)
    
    _player_side = "Jeu joueur"
    _ia_side = "Jeu IA"
    
    _model = None
    
    @classmethod
    def value(cls):
        return 5
    
    def action(self):
        TwoActionCards.action(self)
        Prince._model = self._model 
        #Displays the screen of selection of the side if the current's player is the user
        if(isinstance(self._model.current_player, player.RealPlayer) and not self._model.issimul):
                self._model.controller.display_prince_choice(self._player_side, self._ia_side)
        else:
            if(not isinstance(self._model.ia, player.IADifficile)):
                #else AI algo
                choix=self._model.current_state.evalprince(False)
                if(choix == 1):
                    self.deuxieme_action(self._player_side)
                else:
                    self.deuxieme_action(self._ia_side)
    
    @classmethod
    def deuxieme_action(cls, chosen_side):
        #_player is the player which gets its card thrown
        if(chosen_side == cls._player_side):
            _player = cls._model.player
        else:
            _player = cls._model.ia

        if(not _player.immune):
            if(not cls._model.issimul):
                cls._model.controller.display_prince_detailslabel(cls._model.current_player, chosen_side, _player.cards[0]) #Displays the recapitulative label
            
            #Case where the thrown card is the princess
            if(_player.cards[0].value() == 9 and isinstance(_player, player.RealPlayer)):
                cls._model.game_victory(cls._model.ia, "L'IA remporte 1 point car le vrai joueur s'est fait défaussé une princesse !")
            elif(_player.cards[0].value() == 9 and isinstance(_player, player.IA)):
                cls._model.game_victory(cls._model.player, "Le vrai joueur remporte 1 point car l'IA s'est fait défaussé une princesse !")
            
            #Other case
            else:
                cls._model.add_defausse(_player.cards[0])
                _player.remove_card(_player.cards[0])
                if(not cls._model.issimul):
                    card = cls._model.pick_card()
                    if(card is not None):
                        _player.add_card(card)
                else:
                    _player.add_card(cls._model.pick_card_simu())
                
        
class Chancelier(TwoActionCards):
    '''
    Class defining the counselor's card
    '''
    
    _choix_cartes = None
    
    #Used to avoid problems of reference to the wrong model when used in simulation (not clean, to modify if we have time)
    _model = None
    
    def __str__(self):
        return "Chancelier"
    
    def __init__(self, model):
        Card.__init__(self, model)
    
    @classmethod
    def value(cls):
        return 6
    
    '''
    Explanation of how it works : When one of the two players is about to play the counselor, he'll have to chose the order of the cards he wants to see at the 
    bottom of the deck (he then choses (but exception) the 2 cards he doesn't want to keep)
    Once a card has been selected, we'll check the number of remaining cards in the player's hand.
    If he owns more than a card, it means that the player still needs to choose a card that he doesn't want ant the process starts again.
    Else, it means that the player has either finished his selection, or that we are in the case of an exception where there's only one card left in the deck
    (in which case the player only has one card to select). We therefore stop the process.
    '''
     
    def action(self):
        TwoActionCards.action(self)
        #print(self._model.current_player.cards,self._model.deck)

        if(self._model.deck.__len__() != 0 and (not self._model.issimul or self._model.deck.__len__() != 1)):
            Chancelier._model = self._model
            current_player = self._model.current_player
            current_player.play_chancelier = True #Variable used to know if the player is currently playing a counselor or not when he hits a button
            
            #Checks that there's at least 2 remaining cards in the deck
            if(self._model.deck.__len__() >= 2):
                if(not self._model.issimul):
                    current_player.add_card(self._model.pick_card())
                    current_player.add_card(self._model.pick_card())
                else:
                    current_player.add_card(self._model.pick_card_simu())
                    if(self._model.deck.__len__() != 1):
                        current_player.add_card(self._model.pick_card_simu())
                                                              
            else:
                current_player.add_card(self._model.pick_card())
            
            #If the AI played the counselor, then we call the associated functions
            if(isinstance(current_player, player.IA) or self._model.issimul):
                if(not self._model.issimul):
                    self._model.controller.update_chancelier_IA(current_player, self._model.ia.cards.__len__())
                #faut mettre l'algo ici
                #genre bite=evalchancelier
                #pareil pour ligne 353
                defaussecarte = None
                if(self._model.issimul):
                    defaussecarte=self._model.current_state.evalchancelier(False, self._model.current_state.model)
                else:
                    defaussecarte=self._model.current_state.evalchancelier(False, self._model)
                Chancelier.deuxieme_action(current_player.cards[defaussecarte])
                #algo IA
            else:
                #Same but for the user
                self._model.controller.update_chancelier_player(current_player, self._model.player.cards_to_string)
        
    
    #Function called when the current user selected a card that he doesn't wanna keep
    @classmethod
    def deuxieme_action(cls, card_chosen):
        #print(card_chosen)
        current_player = cls._model.current_player
        current_player.remove_card(card_chosen)
        cls._model.deck.append(card_chosen)
    
        if(current_player.cards.__len__() == 2):
            if(isinstance(current_player, player.IA) or cls._model.issimul):
                defaussecarte = None
                if(cls._model.issimul):
                    defaussecarte=cls._model.current_state.evalchancelier(False, cls._model.current_state.model)
                else:
                    defaussecarte=cls._model.current_state.evalchancelier(False, cls._model)    
                cls.deuxieme_action(current_player.cards[defaussecarte])
            else:
                cls._model.controller.update_chancelier_player(current_player, cls._model.player.cards_to_string)
                
        current_player.play_chancelier = False
            
        #print(cls._model.current_player.cards,cls._model.deck)
        
class Roi(Card):
    '''
    Classe définissant la carte comtesse
    '''
    
    def __str__(self):
        return "Roi"
    
    def __init__(self, model):
        Card.__init__(self, model)
    
    @classmethod
    def value(cls):
        return 7
    
     
    def action(self):
        Card.action(self)
        if(not self._model.next_player.immune):
            current_player = self._model.current_player
            current_card = current_player.cards.pop(0)
            next_player = self._model.next_player
            next_card = next_player.cards.pop(0)
            self._model.next_player.add_card(current_card)
            self._model.current_player.add_card(next_card)
            
            #Indicates that each player knows the card of the other
            current_player.knows_card = [True,current_card.__class__]
            next_player.knows_card = [True, next_card.__class__]
    
class Comtesse(Card):
    '''
    Classe définissant la carte comtesse
    '''
    
    def __str__(self):
        return "Comtesse"
    
    def __init__(self, model):
        Card.__init__(self, model)
    
    @classmethod
    def value(cls):
        return 8
    
     
    def action(self):
        Card.action(self)
    
class Princesse(Card):
    '''
    Classe définissant la carte princesse
    '''
    
    def __str__(self):
        return "Princesse"
    
    def __init__(self, model):
        Card.__init__(self, model)
    
    @classmethod
    def value(cls):
        return 9
    
     
    def action(self):
        Card.action(self)
        if(isinstance(self._model.current_player, player.RealPlayer)):
            self._model.game_victory(self._model.ia, "L'IA remporte 1 point car le vrai joueur à joué la Princesse !")
        else:
            self._model.game_victory(self._model.player, "Le vrai joueur remporte 1 point car l'IA à joué la Princesse !")
        

    
    
    
    
    
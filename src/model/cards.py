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
    template pour toutes les cartes du jeu
    '''
    
    _model = None
    
    #Permet d'afficher la string retournée par __str__ lorsque l'on veut print une instance d'une carte
    def __repr__(self):
        return self.__str__()
    
    def __init__(self, model):
        self._model = model
    
    #Propriété des cartes (valeur)
    @property
    @abstractmethod
    def value(self):
        pass
    
    #Action effectuée par la carte une fois jouée
    @abstractmethod
    def action(self):
        #Si le joueur adverse connaissait la carte du joueur courant, alors il ne la connait plus
        if self._model.next_player.knows_card[0] and isinstance(self, self._model.next_player.knows_card[1]):
            self._model.next_player.knows_card = [False, None]
    
class TwoActionCards(Card, metaclass = abc.ABCMeta):
    '''
    classe abstraite parente des classes se déroulant en deux temps du point de vue utilisateur (choix de la carte -> second choix -> action sur le modèle)
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
    Classe définissant la carte espionne
    '''
    
    #Permet de print Espionne à la place de la référence de l'objet en mémoire
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
    Classe définissant la carte garde
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
            #Vérification du joueur courant afin d'afficher ou non quelque chose sur l'UI
            if(isinstance(self._model.current_player, player.IAMoyenne) or self._model.issimul):
                
                guess=self._model.current_state.evalgarde(False)
                #print(guess)
                array = [Espionne.__name__, Pretre.__name__, Baron.__name__, Servante.__name__, Prince.__name__, Chancelier.__name__, Roi.__name__, 
                         Comtesse.__name__, Princesse.__name__]
                if(not self._model.issimul):
                    self._model.controller.display_guard_ialabel(array[guess]) #Affichage du label récapitulatif
                
                self.deuxieme_action(array[guess])
                    
            else:
                self._model.controller.display_guard_choice()
                    
                
                
            
            
    #Action effectuée une fois que la carte à deviner a été choisi
    @classmethod
    def deuxieme_action(cls, chosen_card):
        if(chosen_card == str(cls._model.next_player.cards[0])):
            cls._model.game_victory(cls._model.current_player, str(cls._model.current_player) +" gagne un point en ayant deviné la carte avec le garde !") 
            
    
class Pretre(Card):
    '''
    Classe définissant la carte pretre
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
            #Indique que le joueur courant connait la carte du joueur adverse, indique également l'instance de cette carte
            self._model.current_player.knows_card = [True,self._model.next_player.cards[0].__class__]
            if(isinstance(self._model.current_player, player.RealPlayer) and not self._model.issimul): #Pas d'affichage en simulation
                self._model.controller.display_AI_card(self._model.ia.cards[0])

            
            
class Baron(Card):
    '''
    Classe définissant la carte baron
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

            #Caching des valeurs auxquelles on va beaucoup accéder dans la fonction
            current_player = self._model.current_player
            next_player= self._model.next_player
            
            #Chaine de caractere de victoire
            chaine = " gagne 1 point, grâce à un baron"
        
            if(not self._model.issimul):
                self._model.controller.display_baron(current_player.cards[0], next_player.cards[0])
            
            #Check du gagnant
            if(current_player.cards[0].value() > next_player.cards[0].value()):
                self._model.game_victory(current_player, str(current_player) + chaine)                     
            elif(current_player.cards[0].value() < next_player.cards[0].value()):
                self._model.game_victory(next_player, str(next_player) + chaine)
            
    #Fonction appelée lors d'une simulation de jeu de baron afin de déterminer les probabilités de gagner
    @classmethod
    def algorithme_simulation(cls):
        return 0.5
        
        
        
class Servante(Card):
    '''
    Classe définissant la carte servante
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
    Classe définissant la carte prince
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
        #Affichage de l'écran de séléction du camp si le joueur est le joueur courrant
        if(isinstance(self._model.current_player, player.RealPlayer) and not self._model.issimul):
                self._model.controller.display_prince_choice(self._player_side, self._ia_side)
        else:
            if(not isinstance(self._model.ia, player.IADifficile)):
                #Sinon algo ia
                #faut mettre self.deuxieme_action(fonction eval prince qui renvoie le camp) genre 0=self._player_side et 1=self._ia_side
                choix=self._model.current_state.evalprince(False)
                if(choix == 1):
                    self.deuxieme_action(self._player_side)
                else:
                    self.deuxieme_action(self._ia_side)
    
    @classmethod
    def deuxieme_action(cls, chosen_side):
        # player est le joueur qui se fait deffausser ses cartes
        if(chosen_side == cls._player_side):
            _player = cls._model.player
        else:
            _player = cls._model.ia

        if(not _player.immune):
            if(not cls._model.issimul):
                cls._model.controller.display_prince_detailslabel(cls._model.current_player, chosen_side, _player.cards[0]) #Affichage du label récapitulatif
            
            #cas ou la carte déffaussé est une princesse
            if(_player.cards[0].value() == 9 and isinstance(_player, player.RealPlayer)):
                cls._model.game_victory(cls._model.ia, "L'IA remporte 1 point car le vrai joueur s'est fait défaussé une princesse !")
            elif(_player.cards[0].value() == 9 and isinstance(_player, player.IA)):
                cls._model.game_victory(cls._model.player, "Le vrai joueur remporte 1 point car l'IA s'est fait défaussé une princesse !")
            
            #autre cas
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
    Classe définissant la carte chancelier
    '''
    
    _choix_cartes = None
    
    #Utilisé pour éviter les problèmes de référence au mauvais model lorsque l'on est en simulation (pas propre, à modifier si il y a le temps)
    _model = None
    
    def __str__(self):
        return "Chancelier"
    
    def __init__(self, model):
        Card.__init__(self, model)
    
    @classmethod
    def value(cls):
        return 6
    
    '''
    Explication du fonctionnement : Lorsqu'un des deux joueurs va jouer un chancelier, il va devoir choisir dans l'ordre les cartes qu'il veut voir
    au fond de la pioche (il choisit donc (sauf exception) les 2 cartes qu'il ne veut pas garder)
    Une fois qu'une carte a été sélectionnée, on va vérifier le nombre de cartes restantes du joueur.
    si il possède plus d'une carte, cela signifie que le joueur doit encore choisir une carte qu'il ne veut pas et le processus est relancé
    sinon, cela signifie soit que le joueur a finit sa séléction, soit que nous nous trouvons dans le cas d'exception où il n'y a qu'une carte dans la pioche
    (auquel cas le joueur n'a qu'une carte a séléctionner). On arrête donc le processus.
    '''
     
    def action(self):
        TwoActionCards.action(self)
        #print(self._model.current_player.cards,self._model.deck)
        #Si il n'y a plus de carte dans la pioche, ou si il y a simulation, alors jouer le chancelier n'aura pas d'effet
        if(self._model.deck.__len__() != 0 and (not self._model.issimul or self._model.deck.__len__() != 1)):
            Chancelier._model = self._model
            current_player = self._model.current_player
            current_player.play_chancelier = True #Variable permettant de savoir si le joueur est en pleine action de chancelier ou non lorsqu'il clique sur un bouton
            
            #Vérifie si il y a bien deux cartes restantes dans la pioche au moins
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
            
            #Si l'IA a joué le chancelier, alors on appelle les fonctions appropriées
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
                #Pareil pour le joueur
                self._model.controller.update_chancelier_player(current_player, self._model.player.cards_to_string)
        
    
    #Fonction appelée lorsque le joueur courant a séléctionné une carte qu'il ne voulait pas
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
            
            #Indique que chaque joueur connait la carte de l'autre
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
        

    
    
    
    
    
# -*- coding: utf-8 -*-
'''
Created on 27 oct. 2020

@author: Antoine
'''

import abc
from abc import abstractmethod
from builtins import classmethod
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
        pass
    
class TwoActionCards(Card, metaclass = abc.ABCMeta):
    '''
    classe abstraite parente des classes se déroulant en deux temps du point de vue utilisateur (choix de la carte -> second choix -> action sur le modèle)
    '''
    
    def __init__(self, model):
        Card.__init__(self, model)
        

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
        pass
    
    
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
    
     
    def action(self):
        #Vérification du joueur courant afin d'afficher ou non quelque chose sur l'UI
        print(self._model.ia.cards[0].value())
        if(isinstance(self._model.current_player, player.RealPlayer)):
            self._model.controller.display_guard_choice()
            
        else:
            
            #algo ia
            pass
    
    #Action effectuée une fois que la carte à deviner a été choisi
    @classmethod
    def deuxieme_action(cls, chosen_card):
        
        print("vous avez choisi " + chosen_card)
        if(chosen_card == str(cls._model.next_player.cards[0])):
            cls._model.game_victory(cls._model.player, "Le vrai joueur gagne un point en ayant deviné la carte avec le garde !") 
        
            
    
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
        if(isinstance(self._model.current_player, player.RealPlayer)):
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
        #Caching des valeurs auxquelles on va beaucoup accéder dans la fonction
        current_player = self._model.current_player
        next_player= self._model.next_player
        
        #Chaine de caractere de victoire
        chaine = " gagne 1 point, en ayant joué un baron"

        #Affichage de l'écran
        self._model.controller.display_baron(current_player.cards[0], next_player.cards[0])
            
        #Check du gagnant
        if(current_player.cards[0].value() > next_player.cards[0].value()):
            self._model.game_victory(current_player, str(current_player) + chaine)                     
        elif(current_player.cards[0].value() < next_player.cards[0].value()):
            self._model.game_victory(next_player, str(next_player) + chaine)
        
        
        
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
        pass
    
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
    
    @classmethod
    def value(cls):
        return 5
    
     
    def action(self):
        if(isinstance(self._model.current_player, player.RealPlayer)):
            self._model.controller.display_prince_choice(self._player_side, self._ia_side)
        else:
            alea = randrange(2)
            if(alea == 0):
                self.deuxieme_action(self._player_side)
            else:
                self.deuxieme_action(self._ia_side)
    
    @classmethod
    def deuxieme_action(cls, chosen_side):
        print(str(cls._model.current_player) + " a choisi " + chosen_side)
        
        
        # player est le joueur qui se fait deffausser ses cartes
        if(chosen_side == cls._player_side):
            _player = cls._model.player
        else:
            _player = cls._model.ia
            
            
        #cas ou la carte déffaussé est une princesse
        if(_player.cards[0].value() == 9 and isinstance(_player, player.RealPlayer)):
            cls._model.game_victory(cls._model.ia, "L'IA remporte 1 point car le vrai joueur s'est fait défaussé une princesse !")
        elif(_player.cards[0].value() == 9 and isinstance(_player, player.IA)):
            cls._model.game_victory(cls._model.player, "Le vrai joueur remporte 1 point car l'IA s'est fait défaussé une princesse !")
        
        #autre cas
        else:
            #a refaire mdr
            cls._model.add_cards_played(_player.cards[0])
            _player.remove_card(_player.cards[0])
            _player.add_card(cls._model.pick_card())
        
        
class Chancelier(TwoActionCards):
    '''
    Classe définissant la carte chancelier
    '''
    
    _choix_cartes = None
    
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
        #Si il n'y a plus de carte dans la pioche, alors jouer le chancelier ne fera rien
        if(self._model.deck.__len__() != 0):
            current_player = self._model.current_player
            current_player.play_chancelier = True #Variable permettant de savoir si le joueur est en pleine action de chancelier ou non lorsqu'il clique sur un bouton
            
            #Vérifie si il y a bien deux cartes restantes dans la pioche au moins
            if(self._model.deck.__len__() >= 2):
                current_player.add_card(self._model.pick_card())
                current_player.add_card(self._model.pick_card())
            else:
                #Cas particulier où il ne reste qu'une carte dans la pioche
                current_player.add_card(self._model.pick_card())
          
            #Si l'IA a joué le chancelier, alors on appelle les fonctions appropriées
            if(isinstance(current_player, player.IA)):
                self._model.controller.update_chancelier_IA(current_player, self._model.ia.cards.__len__())
                Chancelier.deuxieme_action(self._model.ia.cards[randrange(0, 3)])
                #algo IA
            else:
                #Pareil pour le joueur
                self._model.controller.update_chancelier_player(current_player, self._model.player.cards_to_string)
        
    
    #Fonction appelée lorsque le joueur courant a séléctionné une carte qu'il ne voulait pas
    @classmethod
    def deuxieme_action(cls, card_chosen):
        current_player = cls._model.current_player
        
        current_player.remove_card(card_chosen)
        
        cls._model.deck.append(card_chosen)
    
        if(current_player.cards.__len__() == 2):
            if(isinstance(current_player, player.IA)):
                cls.deuxieme_action(cls._model.ia.cards[randrange(0,2)])
            else:
                cls._model.controller.update_chancelier_player(current_player, cls._model.player.cards_to_string)
                
        current_player.play_chancelier = False
            
        
        
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
        pass
    
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
        pass
    
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
        pass
    

    
    
    
    
    
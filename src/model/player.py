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

#Circular linked list, containing the nodes containing each player, and the node containing the current player
class CircleLinkedList(object):

    def __init__(self, head, tail):
        self._real_player_node = head
        self._ia_node = tail
        self._current_node = None
    
    #Get to the next player
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
    
#Node containing the instance of a player and the reference to the next node
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
    Class used as a template for the class realPlayer and the AI classes
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
        #Save of the variables
        return {"Cards" : copy.copy(self._cards), "Cards played" : copy.copy(self._cards_played), "Immune" : self._immune, "Espionne played" : self._espionne_played, 
                "Knows card" : copy.deepcopy(self._knows_card)}
    
    def set_attributes(self, attributes):
        #Reset of the variables and copies of the save (in order not to corrupt it)
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
    
    #Function used to check if the player owns a comtess and the king or the prince
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
    Class used as a template for the different AIs
    '''
    
    def __init__(self, model):
        Player.__init__(self)
        self._model = model
        
    
    def __str__(self):
        return "IA"

    
    @abstractmethod
    def algorithme(self):
        pass

    
class IAMoyenne(IA):
    
    def __init__(self, model):
        IA.__init__(self, model)
        self._depth = 3
    
    def __str__(self):
        return "IA Moyenne"
    
    #Algorithm used by the Intermediate AI to decide the card to play
    def algorithme(self):
        self._model.issimul = True
            
        self._model.deck.append(self._model.burnt_card) #Adds the burnt card to the deck since the player doesn't know that card 
                                                        #It therefore must be drawable
        
        #In order for the AI not to discover the card of its opponent during the simulation, we give the user the card that he might have with the highest possibility
        #(not the most optimal way, the best would be to cover all possibile cases)
        opponent = self._model.next_player
        card = opponent.cards[0] 
        self._model.deck.append(card) #Adds the card to the opponent's deck
        opponent.remove_card(card) #Remove the card from its hand
        newcard = self._model.pick_card_simu() 
        opponent.add_card(newcard) #Get the most probable card
        
        state = State(self._model, None) #Current state
        
        self._model.current_state=state
        
        index = 0
        #If the AI has the comtess and a prince or a king, then no need to start the algorithm, the comtess is played
        play_comtesse = self.must_play_comtesse()
        
        #If the AI has a princess, it doesn't play it, the alpha beta doesn't start then
        if(isinstance(self.cards[0], cards.Princesse)):
            index = 1
        elif(isinstance(self.cards[1], cards.Princesse)):
            index = 0
        elif play_comtesse != -1:
            index = play_comtesse
        else:

        
            temp = copy.copy(self._depth)
            
            #Call to the alpha beta algorithm which will find the value of the best state and the corresponding state
            (value, best_state) = self.max_val(self._model.current_state, float('-inf'), float('inf'), int(temp)) 
            
            
            if(self._depth < 5):
                self._depth += 0.5;
            
            
            
            #Partie à décommenter pour test la succession des états
            '''
            #print(state)
            test = state.next_states()
            #print(test[0])
            test2 = test[0].next_states()
            for i in range(0,10):
                #print(test2[i])
            '''
            
            #Partie à commenter pour test la succession d'états (ne pas oublier de commenter l'appel à max_val)
            '''
            '''
            path = []
            
            #Thanks to the state found with the alpha beta, we find the card which lead to that state
            while(best_state.parent is not state):
                path.append(best_state)
                best_state = best_state.parent
            path.append(best_state)
            path.append(state)
            path.reverse()
            for state in path:
                print(state)
            print("//////////////////////////////////////")
            print()
            if(isinstance(self._cards[0], best_state.last_card_played.__class__)):
                index = 0
            else:
                index = 1

        self._model.deck.remove(self._model.burnt_card) #Remove the burnt card
        
        opponent.remove_card(newcard) #Remove intermediary card from the deck
        opponent.add_card(card)#Give back to the player its real card
        self._model.deck.append(newcard) #Replace the card that the player had in the deck
        self._model.deck.remove(card) #Remove the player's card
        '''
        '''
        self._model.issimul = False
        return index
    
    
    #Classic algorithm of a MAX node
    def max_val(self, state, alpha, beta, depth):
        #Stop condition
        if state.is_final or depth == 0:
            return (state.eval(),state)
        
        value = (float('-inf'), None)
        for s in state.next_states():
            
            temp = self.min_val(s, alpha, beta, depth-1)
            value = max(temp, value, key = lambda x:x[0]) #Since we have a couple (value, parent's state), we search the maximum of the two couples using the value
                                                            #each couple
            if(value[0] >= beta):
                return value
            alpha = max(alpha, value[0])
        return value
    
    #Classic algorithm of a MIN node
    def min_val(self, state, alpha, beta, depth):
        #stop condition
        if(state.is_final or depth == 0):
            return (-state.eval(),state)
        
        value = (float('inf'),None)
        
        for s in state.next_states():
            
            temp = self.max_val(s, alpha, beta, depth-1)
            value = min(value, temp, key = lambda x:x[0]) #Since we have a couple (value, parent's state), we search the minimum of the two couples using the value of
                                                            #each couple
            if(value[0] <= alpha):
                return value
            beta = min(beta, value[0])
        return value
            
    
    def reset_values(self):
        IA.reset_values(self)
        self._depth = 3
            
    
class IADifficile(IA):
    
    
    def __init__(self, model):
        IA.__init__(self, model)
    
    def __str__(self):
        return "IA Difficile"
    
    def algorithme(self):
        return random.randrange(0,2);

class State():
        
    
    def __str__(self):
        return ("State : " + str(self._probability) + "\n" + str(self._model.current_player) + "\nCards remained : " + str(self._cards_remained)+
                "\nCards played by current : " + str(self._model.current_player.cards_played) +
                "\nLast card played by current : " + str(self._model.current_player.last_card_played) + "\nHand : " + str(self._model.current_player.cards) + 
                "\nOpponent's cards played : " + str(self._model.next_player.cards_played) + "\nLast card played in game : " + 
                str(self._last_card_played) + 
                "\nDeck : " + str(self._model.deck) + "\nKnows card : " + str(self._current_player.knows_card[0])
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

        
        self._parent = parent
        
        self._probability = probability
        self._model.current_state = self
        
        self._dicocarte, self._nbcarte=self.info()   
        self._model.current_state = self
        
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
    
    @property
    def model(self):
        return self._model    
    def next_states(self): 
        
        if(not self.is_final):
            drawable_cards = self._model.get_drawable_cards()
            states = []
            
            #Checks if the player has to play comtess or not
            play_comtesse = self._current_player.must_play_comtesse()
            if play_comtesse != -1:
                self.play_simu(states, drawable_cards, play_comtesse)
            else:
                #Looping on the cards of the current player, for each card, we loop through each possible card the next player can draw
                for i in range(0, self._model.current_player.cards.__len__()) :
                    self.play_simu(states, drawable_cards, i)
            
        return states
    
    def play_simu(self, states, drawable_cards, i):
        
        for card in drawable_cards:
            #Simulation
            self._model.pick_card_simu(card)
            self._opponent.add_card(card)
            self._model.play(i)
            
            #Generates the corresponding state
            state = State(self._model, self, drawable_cards[card])
            states.append(state)
            
            #Save the environnement
            self._save.backup() 
                
    def info(self):
        i=0
        nbespionne=0
        nbgarde=0
        nbpretre=0
        nbbaron=0
        nbservante=0
        nbprince=0
        nbchancelier=0
        nbroi=0
        nbcomtesse=0
        nbprincesse=0
            
        mondeck=self._model.deck
        mondeck.append(self._model.next_player.cards[0])
          
        while i<len(mondeck):
            if(isinstance(mondeck[i],cards.Espionne)):
                nbespionne=nbespionne+1
            if(isinstance(mondeck[i],cards.Garde)):
                nbgarde=nbgarde+1
            if(isinstance(mondeck[i],cards.Pretre)):
                nbpretre=nbpretre+1
            if(isinstance(mondeck[i],cards.Baron)):
                nbbaron=nbbaron+1
            if(isinstance(mondeck[i],cards.Servante)):
                nbservante=nbservante+1
            if(isinstance(mondeck[i],cards.Prince)):
                nbprince=nbprince+1
            if(isinstance(mondeck[i],cards.Chancelier)):
                nbchancelier=nbchancelier+1
            if(isinstance(mondeck[i],cards.Roi)):
                nbroi=nbroi+1
            if(isinstance(mondeck[i],cards.Comtesse)):
                nbcomtesse=nbcomtesse+1
            if(isinstance(mondeck[i],cards.Princesse)):
                nbprincesse=nbprincesse+1
            i=i+1
            
        mondeck.remove(self._model.next_player.cards[0])
        
        return {cards.Espionne:nbespionne,cards.Garde:nbgarde,cards.Pretre:nbpretre,cards.Baron:nbbaron,cards.Servante:nbservante,cards.Prince:nbprince,cards.Chancelier:nbchancelier,cards.Roi:nbroi,cards.Comtesse:nbcomtesse,cards.Princesse:nbprincesse},i
        
        
    def eval(self):
        if(self._model.victory):
            return 1
        else:
            #print("Nombre d'Espionne =",self._dicocarte[cards.Espionne]," Nombre de Garde =",self._dicocarte[cards.Garde]," Nombre de Pretre =",self._dicocarte[cards.Pretre]," Nombre de Baron =",self._dicocarte[cards.Baron]," Nombre de Servante =",self._dicocarte[cards.Servante]," Nombre de Prince =",self._dicocarte[cards.Prince]," Nombre de Chancelier =",self._dicocarte[cards.Chancelier]," Nombre de Roi =",self._dicocarte[cards.Roi]," Nombre de Comtesse =",self._dicocarte[cards.Comtesse]," Nombre de Princesse =",self._dicocarte[cards.Princesse],"Nombre total de carte :",self._nbcarte)
            if(isinstance(self._model.current_player.cards[0],cards.Espionne)):
                poids1=100*(self._dicocarte[cards.Espionne]/self._nbcarte)  #Faut pas chercher plus longtemps, si on a l'espionne, faut la jouer

            if(isinstance(self._model.current_player.cards[0],cards.Garde)):
                if(self._model.next_player.knows_card[0]==True):
                    probagarde=self._dicocarte[cards.Garde]/self._nbcarte*100
                    poids1=(100-probagarde)*(self._dicocarte[cards.Garde]/self._nbcarte)
                else:
                    poids1=self.evalgarde(True)*(self._dicocarte[cards.Garde]/self._nbcarte)

            if(isinstance(self._model.current_player.cards[0],cards.Pretre)):
                if(self._model.next_player.knows_card[0]==True):
                    probagarde=self._dicocarte[cards.Garde]/self._nbcarte*100
                    poids1=(100-probagarde)*(self._dicocarte[cards.Garde]/self._nbcarte)
                else:
                    if(self._opponent.immune==True):
                        poids1=20*(self._dicocarte[cards.Pretre]/self._nbcarte)
                    else:
                        poids1=70*(self._dicocarte[cards.Pretre]/self._nbcarte)

            if(isinstance(self._model.current_player.cards[0],cards.Baron)):
                probaespionne=self._dicocarte[cards.Espionne]/self._nbcarte*100
                probagarde=(self._dicocarte[cards.Espionne]+self._dicocarte[cards.Garde])/self._nbcarte*100
                probapretre=(self._dicocarte[cards.Espionne]+self._dicocarte[cards.Garde]+self._dicocarte[cards.Pretre])/self._nbcarte*100
                probabaron=(self._dicocarte[cards.Espionne]+self._dicocarte[cards.Garde]+self._dicocarte[cards.Pretre]+self._dicocarte[cards.Baron])/self._nbcarte*100
                probaservante=(self._dicocarte[cards.Espionne]+self._dicocarte[cards.Garde]+self._dicocarte[cards.Pretre]+self._dicocarte[cards.Baron]+self._dicocarte[cards.Servante])/self._nbcarte*100
                probaprince=(self._dicocarte[cards.Espionne]+self._dicocarte[cards.Garde]+self._dicocarte[cards.Pretre]+self._dicocarte[cards.Baron]+self._dicocarte[cards.Servante]+self._dicocarte[cards.Prince])/self._nbcarte*100
                probachancelier=(self._dicocarte[cards.Espionne]+self._dicocarte[cards.Garde]+self._dicocarte[cards.Pretre]+self._dicocarte[cards.Baron]+self._dicocarte[cards.Servante]+self._dicocarte[cards.Prince]+self._dicocarte[cards.Chancelier])/self._nbcarte*100
                probaroi=(self._dicocarte[cards.Espionne]+self._dicocarte[cards.Garde]+self._dicocarte[cards.Pretre]+self._dicocarte[cards.Baron]+self._dicocarte[cards.Servante]+self._dicocarte[cards.Prince]+self._dicocarte[cards.Chancelier]+self._dicocarte[cards.Roi])/self._nbcarte*100
                probacomtesse=(self._dicocarte[cards.Espionne]+self._dicocarte[cards.Garde]+self._dicocarte[cards.Pretre]+self._dicocarte[cards.Baron]+self._dicocarte[cards.Servante]+self._dicocarte[cards.Prince]+self._dicocarte[cards.Chancelier]+self._dicocarte[cards.Roi]+self._dicocarte[cards.Comtesse])/self._nbcarte*100
                #print("Les proba du Baron : Espionne :",probaespionne,"Garde :",probagarde,"Pretre :",probapretre,"Baron :",probabaron,"Servante :",probaservante,"Prince :",probaprince,"Chancelier :",probachancelier,"Roi :",probaroi,"Comtesse :",probacomtesse)
                if(self._model.next_player.knows_card[0]==True):
                    probagarde=self._dicocarte[cards.Garde]/self._nbcarte*100
                    poids1=(100-probagarde)*(self._dicocarte[cards.Garde]/self._nbcarte)
                else:
                    if(self._opponent.immune==True):
                        poids1=35*(self._dicocarte[cards.Baron]/self._nbcarte)
                    else:
                        if(isinstance(self._model.current_player.cards[1],cards.Espionne)):
                            poids1=probaespionne*(self._dicocarte[cards.Baron]/self._nbcarte)
                        if(isinstance(self._model.current_player.cards[1],cards.Garde)):
                            poids1=probagarde*(self._dicocarte[cards.Baron]/self._nbcarte)
                        if(isinstance(self._model.current_player.cards[1],cards.Pretre)):
                            poids1=probapretre*(self._dicocarte[cards.Baron]/self._nbcarte)
                        if(isinstance(self._model.current_player.cards[1],cards.Baron)):
                            poids1=probabaron*(self._dicocarte[cards.Baron]/self._nbcarte)
                        if(isinstance(self._model.current_player.cards[1],cards.Servante)):
                            poids1=probaservante*(self._dicocarte[cards.Baron]/self._nbcarte)
                        if(isinstance(self._model.current_player.cards[1],cards.Prince)):
                            poids1=probaprince*(self._dicocarte[cards.Baron]/self._nbcarte)
                        if(isinstance(self._model.current_player.cards[1],cards.Chancelier)):
                            poids1=probachancelier*(self._dicocarte[cards.Baron]/self._nbcarte)
                        if(isinstance(self._model.current_player.cards[1],cards.Roi)):
                            poids1=probaroi*(self._dicocarte[cards.Baron]/self._nbcarte)
                        if(isinstance(self._model.current_player.cards[1],cards.Comtesse)):
                            poids1=probacomtesse*(self._dicocarte[cards.Baron]/self._nbcarte)
                        if(isinstance(self._model.current_player.cards[1],cards.Princesse)):
                            poids1=100*(self._dicocarte[cards.Baron]/self._nbcarte)
                        
            if(isinstance(self._model.current_player.cards[0],cards.Servante)):
                if(self._model.next_player.knows_card[0]==True):
                    probagarde=self._dicocarte[cards.Garde]/self._nbcarte*100
                    poids1=(100-probagarde)*(self._dicocarte[cards.Garde]/self._nbcarte)
                else:
                    poids1=75*(self._dicocarte[cards.Servante]/self._nbcarte) #Même si le joueur en face a aussi joué une servante, dans le cas de la servante onsenbalécouilles

            if(isinstance(self._model.current_player.cards[0],cards.Prince)):
                if(self._model.next_player.knows_card[0]):
                    probagarde=self._dicocarte[cards.Garde]/self._nbcarte*100
                    poids1=(100-probagarde)*(self._dicocarte[cards.Garde]/self._nbcarte)
                else:
                    poids1=self.evalprince(True)*(self._dicocarte[cards.Prince]/self._nbcarte)

            if(isinstance(self._model.current_player.cards[0],cards.Chancelier)):
                if(self._model.next_player.knows_card[0]==True):
                    probagarde=self._dicocarte[cards.Garde]/self._nbcarte*100
                    poids1=(100-probagarde)*(self._dicocarte[cards.Garde]/self._nbcarte)
                else:
                    poids1=self.evalchancelier(True, self._model)*(self._dicocarte[cards.Chancelier]/self._nbcarte)
        
            if(isinstance(self._model.current_player.cards[0],cards.Roi)):
                if(self._model.next_player.knows_card[0]==True):
                    probagarde=self._dicocarte[cards.Garde]/self._nbcarte*100
                    poids1=(100-probagarde)*(self._dicocarte[cards.Garde]/self._nbcarte)
                else:
                    if(self._opponent.immune==True):
                        poids1=10*(self._dicocarte[cards.Roi]/self._nbcarte)
                    else:
                        poids1=45*(self._dicocarte[cards.Roi]/self._nbcarte)
        
            if(isinstance(self._model.current_player.cards[0],cards.Comtesse)):
                if(self._model.next_player.knows_card[0]==True):
                    probagarde=self._dicocarte[cards.Garde]/self._nbcarte*100
                    poids1=(100-probagarde)*(self._dicocarte[cards.Garde]/self._nbcarte)
                else:
                    poids1=50*(self._dicocarte[cards.Comtesse]/self._nbcarte)
            
            if(isinstance(self._model.current_player.cards[0],cards.Princesse)):
                poids1=0 #Peut importe le contexte, le princesse est à 0. (Bon en vrai je pourrais faire une fonction qui nous permetterais de gagner la partie mais pour l'instant je laisse comme ça


            #print("Le poids 1 est :",poids1)


            if(isinstance(self._model.current_player.cards[1],cards.Espionne)):
                if(isinstance(self._model.current_player.cards[0],cards.Espionne)):
                    poids2=30*(self._dicocarte[cards.Espionne]/self._nbcarte) #Une main avec deux espionnes  n'est pas forcément la combinaison la plus avantageuse
                else:
                    poids2=100*(self._dicocarte[cards.Espionne]/self._nbcarte)

            if(isinstance(self._model.current_player.cards[1],cards.Garde)):
                poids2=self.evalgarde(True)*(self._dicocarte[cards.Garde]/self._nbcarte)

            if(isinstance(self._model.current_player.cards[1],cards.Pretre)):
                if(self._opponent.immune==True):
                    poids2=20*(self._dicocarte[cards.Pretre]/self._nbcarte)
                else:
                    poids2=70*(self._dicocarte[cards.Pretre]/self._nbcarte)

            if(isinstance(self._model.current_player.cards[1],cards.Baron)):
                probaespionne=self._dicocarte[cards.Espionne]/self._nbcarte*100
                probagarde=(self._dicocarte[cards.Espionne]+self._dicocarte[cards.Garde])/self._nbcarte*100
                probapretre=(self._dicocarte[cards.Espionne]+self._dicocarte[cards.Garde]+self._dicocarte[cards.Pretre])/self._nbcarte*100
                probabaron=(self._dicocarte[cards.Espionne]+self._dicocarte[cards.Garde]+self._dicocarte[cards.Pretre]+self._dicocarte[cards.Baron])/self._nbcarte*100
                probaservante=(self._dicocarte[cards.Espionne]+self._dicocarte[cards.Garde]+self._dicocarte[cards.Pretre]+self._dicocarte[cards.Baron]+self._dicocarte[cards.Servante])/self._nbcarte*100
                probaprince=(self._dicocarte[cards.Espionne]+self._dicocarte[cards.Garde]+self._dicocarte[cards.Pretre]+self._dicocarte[cards.Baron]+self._dicocarte[cards.Servante]+self._dicocarte[cards.Prince])/self._nbcarte*100
                probachancelier=(self._dicocarte[cards.Espionne]+self._dicocarte[cards.Garde]+self._dicocarte[cards.Pretre]+self._dicocarte[cards.Baron]+self._dicocarte[cards.Servante]+self._dicocarte[cards.Prince]+self._dicocarte[cards.Chancelier])/self._nbcarte*100
                probaroi=(self._dicocarte[cards.Espionne]+self._dicocarte[cards.Garde]+self._dicocarte[cards.Pretre]+self._dicocarte[cards.Baron]+self._dicocarte[cards.Servante]+self._dicocarte[cards.Prince]+self._dicocarte[cards.Chancelier]+self._dicocarte[cards.Roi])/self._nbcarte*100
                probacomtesse=(self._dicocarte[cards.Espionne]+self._dicocarte[cards.Garde]+self._dicocarte[cards.Pretre]+self._dicocarte[cards.Baron]+self._dicocarte[cards.Servante]+self._dicocarte[cards.Prince]+self._dicocarte[cards.Chancelier]+self._dicocarte[cards.Roi]+self._dicocarte[cards.Comtesse])/self._nbcarte*100
                #print("Les proba du Baron : Espionne :",probaespionne,"Garde :",probagarde,"Pretre :",probapretre,"Baron :",probabaron,"Servante :",probaservante,"Prince :",probaprince,"Chancelier :",probachancelier,"Roi :",probaroi,"Comtesse :",probacomtesse)
                if(self._opponent.immune==True):
                    poids2=35*(self._dicocarte[cards.Baron]/self._nbcarte)
                else:
                    if(isinstance(self._model.current_player.cards[0],cards.Espionne)):
                        poids2=probaespionne*(self._dicocarte[cards.Baron]/self._nbcarte)
                    if(isinstance(self._model.current_player.cards[0],cards.Garde)):
                        poids2=probagarde*(self._dicocarte[cards.Baron]/self._nbcarte)
                    if(isinstance(self._model.current_player.cards[0],cards.Pretre)):
                        poids2=probapretre*(self._dicocarte[cards.Baron]/self._nbcarte)
                    if(isinstance(self._model.current_player.cards[0],cards.Baron)):
                        poids2=probabaron*(self._dicocarte[cards.Baron]/self._nbcarte)
                    if(isinstance(self._model.current_player.cards[0],cards.Servante)):
                        poids2=probaservante*(self._dicocarte[cards.Baron]/self._nbcarte)
                    if(isinstance(self._model.current_player.cards[0],cards.Prince)):
                        poids2=probaprince*(self._dicocarte[cards.Baron]/self._nbcarte)
                    if(isinstance(self._model.current_player.cards[0],cards.Chancelier)):
                        poids2=probachancelier*(self._dicocarte[cards.Baron]/self._nbcarte)
                    if(isinstance(self._model.current_player.cards[0],cards.Roi)):
                        poids2=probaroi*(self._dicocarte[cards.Baron]/self._nbcarte)
                    if(isinstance(self._model.current_player.cards[0],cards.Comtesse)):
                        poids2=probacomtesse*(self._dicocarte[cards.Baron]/self._nbcarte)
                    if(isinstance(self._model.current_player.cards[0],cards.Princesse)):
                        poids2=100*(self._dicocarte[cards.Baron]/self._nbcarte)
                
            if(isinstance(self._model.current_player.cards[1],cards.Servante)):
                poids2=75*(self._dicocarte[cards.Servante]/self._nbcarte) #On viens de la piocher donc on a pas besoin de savoir si le joueur en face connait la carte et le fait que l'adversaire est joué une servante avant, balécouiles

            if(isinstance(self._model.current_player.cards[1],cards.Prince)):
                poids2=self.evalprince(True)*(self._dicocarte[cards.Prince]/self._nbcarte)

            if(isinstance(self._model.current_player.cards[1],cards.Chancelier)):
                poids2=self.evalchancelier(True, self._model)*(self._dicocarte[cards.Chancelier]/self._nbcarte)
        
            if(isinstance(self._model.current_player.cards[1],cards.Roi)):
                if(self._opponent.immune==True):
                    poids2=10*(self._dicocarte[cards.Roi]/self._nbcarte)
                else:
                    poids2=45*(self._dicocarte[cards.Roi]/self._nbcarte) #Poids haut car carte haute

            if(isinstance(self._model.current_player.cards[1],cards.Comtesse)):
                poids2=50*(self._dicocarte[cards.Comtesse]/self._nbcarte) #Le poids est quand même plus haut car le fait d'avoir une carte haute est toujours un avantage

            if(isinstance(self._model.current_player.cards[1],cards.Princesse)):
                poids2=0 #Peut importe le contexte, le princesse est à 0. (Bon en vrai je pourrais faire une fonction qui nous permetterais de gagner la partie mais pour l'instant je laisse comme ça
        
            #print("Le poids 2 est :",poids2)

            poidsfinal=poids1+poids2
            #print("Carte jouer par l'adversaire :",self._model.next_player.cards_played)
            #print("Le poids de l'état actuelle est :",poidsfinal,"/200\nLa main actuelle étant :",self._model.current_player.cards[0],self._model.current_player.cards[1])
            return poidsfinal
    
    def evalchancelier(self,choix, model):
        if(choix): #Si choix est vrai, on est dans le cas où il faut retourner un poids
            if(isinstance(model.current_player.cards[0],cards.Princesse) or isinstance(self._model.current_player.cards[1],cards.Princesse)):
                return 99 #C'est maximal parce que c'est quand même une princesse, même si le fait d'avoir une princesse n'est pas avantageux je pense qu'il faut qu'en même se diriger vers cet état pour s'en débarrasser
            else:
                return 40
        else: #La, c'est le choix des cartes
            for j in range(0,model.current_player.cards.__len__()):
                if(isinstance(model.current_player.cards[j],cards.Princesse)):
                    #print("Il faut défausser la princesse",model.current_player.cards[j],j)
                    return j
                else:
                    if(isinstance(model.current_player.cards[j],cards.Espionne)):
                        #print("Je rentre dans le cas de l'espionne pour le chancelier")
                        if(model.current_player.cards.__len__==2):
                            if(j==0):
                                return random.choice[1,2]
                            else:
                                if(j==1):
                                    return random.choice([0,2])
                                else:
                                    return random.choice[0,1]
                        else:
                            if(j==0):
                                return 1
                            else:
                                if(j==1):
                                    return 0
                                
            if(model.current_player.cards[0]==model.current_player.cards[1]):
                #print("Deux même cartes dans la main, on en défausse une au hasard")
                defausse=random.choice([0,1])
                #print("On se débarasse de",self._model.current_player.cards[defausse])
                return defausse
            else:
                if(model.current_player.cards.__len__==2):
                    if(model.current_player.cards[0]==model.current_player.cards[2]):
                        #print("Deux même cartes dans la main, on en défausse une au hasard")
                        defausse=random.choice([0,2])
                        #print("On se débarasse de",self._model.current_player.cards[defausse])
                        return defausse
                    else:
                        if(model.current_player.cards[1]==model.current_player.cards[2]):
                            #print("Deux même cartes dans la main, on en défausse une au hasard")
                            defausse=random.choice([1,2])
                            #print("On se débarasse de",self._model.current_player.cards[defausse])
                            return defausse
                        else:
                            defausse=random.choice([0,1,2])
                            #print("On se débarasse de",self._model.current_player.cards[defausse])
                            return defausse
                else:
                    defausse=random.choice([0,1])
                    #print("On se débarasse de",self._model.current_player.cards[defausse])
                    return defausse
                        
                        
    def evalprince(self,choix):
        probavictoire=self._dicocarte[cards.Princesse]/self._nbcarte*100
        probapourfairechier=(self._dicocarte[cards.Servante]+self._dicocarte[cards.Pretre])/self._nbcarte*100
        probatotal=probavictoire+probapourfairechier
        if(choix): #Case where we have to return a weight
            #print("Les probas pour le Prince : Victoire :",probavictoire,"Pour faire chier :",probapourfairechier)    
            if(self._opponent.immune==True):
                poids=30
            else:
                if(self._current_player.knows_card[0] and isinstance(self._model.next_player.cards[0],cards.Princesse)):
                    poids=99
                else:
                    if(probatotal>=0):
                        poids=probatotal
            return poids
        else: #Case where we have to return a side
            if(isinstance(self._model.next_player.cards[0],cards.Princesse)):
                #print("Camp adverse")
                return 1
            else:
                if(isinstance(self._model.next_player.cards[0],cards.Espionne)):
                    return 1
                else:
                    if(self._model.current_player.knows_card[0]):
                        #print("Camp IA")
                        return 0
                    if(probatotal>40):
                        #print("Camp IA")
                        return 0
                    else:
                        #print("Camp adversaire")
                        return 1

    def evalgarde(self,choix):
        probaespionne=(self._dicocarte[cards.Espionne]/self._nbcarte*100,0)
        probapretre=(self._dicocarte[cards.Pretre]/self._nbcarte*100,1)
        probabaron=(self._dicocarte[cards.Baron]/self._nbcarte*100,2)
        probaservante=(self._dicocarte[cards.Servante]/self._nbcarte*100,3)
        probaprince=(self._dicocarte[cards.Prince]/self._nbcarte*100,4)
        probachancelier=(self._dicocarte[cards.Chancelier]/self._nbcarte*100,5)
        probaroi=(self._dicocarte[cards.Roi]/self._nbcarte*100,6)
        probacomtesse=(self._dicocarte[cards.Comtesse]/self._nbcarte*100,7)
        probaprincesse=(self._dicocarte[cards.Princesse]/self._nbcarte*100,8)
        probalist=[probaespionne,probapretre,probabaron,probaservante,probaprince,probachancelier,probaroi,probacomtesse,probaprincesse]
        #print(probalist)

        carteajouer = max(probalist, key = lambda x:x[0])
        #print(carteajouer)
        
        if(choix): #Case where we have to return a weight
            if(self._opponent.immune==True):
                return 50
            else:
                if(self._current_player.knows_card[0]):
                    #print("Carte à faire deviner :",self._current_player.knows_card[1])
                    return 99
                else:
                    return carteajouer[0]+15 #luck factor
        else:
            if(self._current_player.knows_card[0]):
                #print("Carte à faire deviner :",self._current_player.knows_card[1])
                
                return self._current_player.knows_card[1].value()
            else:
                #print("Carte à faire deviner :",dicoproba[carteajouer])#Si il y a plusieurs cartes avec la même probabilité, il va prendre la dernière carte avec la même probabilité
                
               
                return carteajouer[1]
class Save():
    '''
    Class used to save the current state of the game during a simulation. This way of doing things is far from being the best, implementing a command pattern
    for the simulation would've been more beneficial, but would've made the files' architecture messier
    '''
    def __init__(self, model):
        #Create an environment linked to the current state in order not to manipulate the environnement outside the current state
        self._model = copy.deepcopy(model)
        
        self._current_player = self._model.current_player
        self._next_player = self._model.next_player
        
        #Save the elements of the environnment
        self._modelsave = self._model.save_attributes()
        self._current_player_save = self._model.current_player.save_attributes()
        self._next_player_save = self._model.next_player.save_attributes()
        
    def get_model(self):
        return self._model

    #reset the environnement
    def backup(self):
        
        self._current_player.set_attributes(self._current_player_save)
        self._next_player.set_attributes(self._next_player_save)
        self._model.set_attributes(self._modelsave)
        
        #Reset is only done on the cards' lists, we have to reset the current player manually
        self._model.players_list.next_turn()
        

    

# -*- coding: utf-8 -*-
'''
Created on 26 oct. 2020

@author: Antoine
'''

import src.model.model as model
import webbrowser
import sys

class Controller():
    #Don't call this variable from the view in order to keep model and view independants   
    
    _modelvar = None
    _game_scene = None
    
    @classmethod
    def addgamescene(cls, game_scene):
        cls._game_scene = game_scene
        
    @classmethod
    def consulter_regles(cls):
        webbrowser.open('https://fr.wikipedia.org/wiki/Love_Letter_(jeu)')
        
    @classmethod
    def quitter_jeu(cls):
        sys.exit(0)
    
    @classmethod
    #Function called by the user when the user start/finish a round or get back to the menu
    def display_scene(cls, view, scene_name):
        view.display_scene(scene_name)
    
    @classmethod
    #Function called when user chooses the game's difficulty
    def start_game(cls, view, difficulty): #difficulty = -1 : new round, difficulté != -1 : new game
        current_player = cls._modelvar.init_data(difficulty)
        if(difficulty == 1): #Hard difficulty chosen so we start a simulation to make the AI learn (reinforcement learning), to remove when the AI has already learnt
            return
        
        #Display the board
        cls.display_scene(view, "Game scene")
    
        #Display the 3 first cards and name of the player which starts, also reset the game scene
        view.scenes["Game scene"].init_round(cls._modelvar.get_three_cards(), str(cls._modelvar.current_player), cls._modelvar.ia.score, cls._modelvar.player.score)

        
        #Start of the first turn
        cls.start_turn(current_player, view.scenes["Game scene"])
        
        
    @classmethod
    #Function processing a turn
    def start_turn(cls, current_player, gamescene):
        if(not cls._modelvar.victory):
            
            #Update of the GUI (number of cards of AI)
            gamescene.update_iaUI(cls._modelvar.ia.cards.__len__())
            
            #Uodate the GUI of the real player (number of cards and pictures of the player's cards)
            gamescene.update_playerUI(cls._modelvar.player.cards_to_string)
            
            #If the current player is the AI, then the user can't play, and the actions won't be seen via the GUI , it'll be done in the model
            if(isinstance(current_player, model.player.IA)):
                gamescene.update_tour_label("C'est le tour de l'IA")
                #Verification of the first turn
                if(cls._modelvar.player.last_card_played is not None):
                    
                    gamescene.update_lastcardslabels(str(cls._modelvar.player), str(cls._modelvar.player.last_card_played)) #Display the card played by the last player
                cls.card_playedAI(gamescene)
            else:
               
                gamescene.update_tour_label("C'est votre tour")
                if(cls._modelvar.ia.last_card_played is not None):
                    gamescene.update_lastcardslabels(str(cls._modelvar.ia), str(cls._modelvar.ia.last_card_played)) #Display the card played by the last player
                gamescene.unlock_buttons()
                
                #Case where the player has to play the comtess
                must_play_comtesse = cls._modelvar.player.must_play_comtesse()
                if(must_play_comtesse != -1):
                    gamescene.lock_button((must_play_comtesse+1)%2)
                
       
    
    @classmethod
    #AI plays a card
    def card_playedAI(cls, gamescene):
        if(not cls._modelvar.islearning):
            #Wait 3 sec
            gamescene.freeze_screen()

        cls._modelvar.playAI()

        cls.start_turn(cls._modelvar.current_player, gamescene)
       
    @classmethod
    #Function called when a player choses a card
    def card_played(cls, gamescene, index):
        #Checks if the player isn't playing the counselor, in that case, the program must not interpret the click on the button as card played
        if(cls._modelvar.player.play_chancelier):
            cls.played_chancelier(gamescene, index)
        else:
            #Action of the card and change current player
            cls._modelvar.play(index)
            
            #New turn
            cls.start_turn(cls._modelvar.current_player, gamescene)
    

        
    @classmethod
    #Takes in the model the cards which have been played during the round and give them back of the view which will display them
    def display_played_cards(cls, special_frame, call_from_special = False):
        special_frame.display_allcards(cls._modelvar.ia.cards_played, cls._modelvar.player.cards_played, cls._modelvar.get_three_cards(), cls._modelvar.cartes_defaussees, call_from_special)
    
    #If the card is a guard and it's the user's turn, we'll display a screen showing which cards he can guess
    @classmethod
    def display_guard_choice(cls):
        cls._game_scene.display_guard_choice()

    
    #If the card played is a prince, then the user wil be able to chose which player has to throw its card
    @classmethod
    def display_prince_choice(cls, jeu_joueur, jeu_ia):
        cls._game_scene.display_prince_choice(jeu_joueur, jeu_ia)
    
    #Function which displays the label of information and adds some lisibility to the game
    @classmethod
    def display_guard_ialabel(cls, card_guessed):
        if(cls._modelvar.islearning):
            return
        
        cls._game_scene.display_details_label("L'IA a joué un garde\net deviné la carte : " + card_guessed)
        cls._game_scene.freeze_screen()
        cls._game_scene.update_lastcardslabels("IA ", model.cards.Garde.__name__)
        cls._game_scene.update_iaUI(1)
        cls._game_scene.undisplay_details_label()
    
    #Displays the label which recapitulates when a player played a prince
    @classmethod
    def display_prince_detailslabel(cls, current_player, side_chosen, card):
        if(cls._modelvar.islearning):
            return
        cls._game_scene.display_details_label(str(current_player) + " a joué un prince\net choisi ce camp : " + side_chosen + "\nDéfausse : " + str(card))
        if("IA" in side_chosen):
            cls.display_AI_card(cls._modelvar.ia.cards[0])
        cls._game_scene.freeze_screen()
        cls._game_scene.undisplay_details_label()
        cls._game_scene.update_iaUI(1)
        
    @classmethod
    #Function called when user tried to guess a card thanks to the guard card
    def card_chosen(cls, special_frame, card):
        #We remove the special frame and keep playing the guard's action
        special_frame.stop_display()
        model.cards.Garde.deuxieme_action(card)
        
    @classmethod
    #Function called when user played the prince and chose the player who has to throw its card
    def side_chosen(cls, special_frame, side):
        #We remove the special frame and resume the action of the prince
        special_frame.stop_display()
        model.cards.Prince.deuxieme_action(side)
        
    @classmethod
    def display_AI_card(cls,card):
        if(cls._modelvar.islearning):
            return
        #Displays the AI's card, locks the buttons, waits 3 sec, unlocks the buttons and displays the cards as hidden again
        cls._game_scene.display_AI_card(str(card))
        cls._game_scene.freeze_screen()
        cls._game_scene.update_iaUI(1)
        
    @classmethod
    def display_baron(cls, firstcard, secondcard):
        if(cls._modelvar.islearning):
            return
        cls._game_scene.update_lastcardslabels(str(cls._modelvar.current_player), model.cards.Baron.__name__)
        #Displays the cards of the player and the AI during 3 secs
        cls._game_scene.display_baron(firstcard, secondcard)

    #Update the GUI of the AI when it plays the counselor, in such a way that the user can follow up with its actions
    @classmethod
    def update_chancelier_IA(cls, current_player, nbcardsia):
        if(cls._modelvar.islearning):
            return
        cls._game_scene.update_lastcardslabels(str(current_player), model.cards.Chancelier.__name__)
        cls._game_scene.update_iaUI(nbcardsia)
        cls._game_scene.freeze_screen()
    
    #Update the GUI of the user when he plays a counselor, in such a way that he can then choose which cards he wants to keep
    @classmethod
    def update_chancelier_player(cls, current_player, playercards):
        cls._game_scene.display_details_label("Vous avez joué un chancelier\nChoisissez dans l'ordre\nles cartes que vous voulez avoir en fin de pioche") #Display the info label
        cls._game_scene.update_lastcardslabels(str(current_player), model.cards.Chancelier.__name__)
        cls._game_scene.update_playerUI(playercards) #Updates the GUI
        cls._game_scene.wait_chancelier() #Waits for the user's choice
    
    #Function called when the user clicked on one of the cards he wants to place at the bottom of the deck
    @classmethod
    def played_chancelier(cls, gamescene, index):
        gamescene.resume_game() #Resumes the game
        model.cards.Chancelier.deuxieme_action(cls._modelvar.player.cards[index]) #associated treatement starts
        cls._game_scene.undisplay_details_label()#Removes the label info
            
    @classmethod
    #Displays the end game screen, the way the round ended, and the score of each player
    def display_victory(cls, victory_condition, score):
        cls._game_scene.view.scenes["End game scene"].victory_screen(victory_condition, score)
        

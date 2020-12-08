# -*- coding: utf-8 -*-
'''
Created on 26 oct. 2020

@author: Antoine
'''

import src.model.model as model
import webbrowser
import sys
#from prompt_toolkit.application import current

class Controller():
    #Ne pas appeler cette variable depuis un module de view afin de garder l'indépendance entre modèle et view    
    
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
    #Fonction appelée lorsque l'utilisateur lance une partie/finit une partie/retourne au menu
    def display_scene(cls, view, scene_name):
        view.display_scene(scene_name)
    
    @classmethod
    #Fonction lancée lorsque l'utilisateur à choisi la difficulté de la partie
    def start_game(cls, view, difficulty): #difficulty = -1 : nouveau round, difficulté != -1 : nouvelle partie
        current_player = cls._modelvar.init_data(difficulty)
        
        #Affichage du plateau de jeu
        cls.display_scene(view, "Game scene")
    
        #Affichage des 3 premieres cartes et du nom de la personne qui commence et réinitialisation de la game scene
        view.scenes["Game scene"].init_round(cls._modelvar.get_three_cards(), str(cls._modelvar.current_player), cls._modelvar.ia.score, cls._modelvar.player.score)

        
        #Début du premier tour
        cls.start_turn(current_player, view.scenes["Game scene"])
        
        
    @classmethod
    #Fonction permettant le déroulement d'un tour
    def start_turn(cls, current_player, gamescene):
        if(not cls._modelvar.victory):
            
            #Actualisation de l'UI (nombre de cartes de l'IA)
            gamescene.update_iaUI(cls._modelvar.ia.cards.__len__())
            
            #Actualisation de l'UI du vrai joueur (nombre de cartes et images associées du joueur)
            gamescene.update_playerUI(cls._modelvar.player.cards_to_string)
            
            #Si le joueur actuel est l'IA, alors l'utilisateur ne peut pas jouer, et le process se fera sans UI, dans le modèle
            if(isinstance(current_player, model.player.IA)):
                gamescene.update_tour_label("C'est le tour de l'IA")
                #Vérification premier tour
                if(cls._modelvar.player.last_card_played is not None):
                    
                    gamescene.update_lastcardslabels(str(cls._modelvar.player), str(cls._modelvar.player.last_card_played)) #Affichage de la carte jouée par le joueur au dernier tour
                cls.card_playedAI(gamescene)
            else:
                gamescene.update_tour_label("C'est votre tour")
                if(cls._modelvar.ia.last_card_played is not None):
                    gamescene.update_lastcardslabels(str(cls._modelvar.ia), str(cls._modelvar.ia.last_card_played)) #Affichage de la carte jouée par l'IA au dernier tour
                gamescene.unlock_buttons()
                
                #Cas où le joueur est obligé de jouer la comtesse
                must_play_comtesse = cls._modelvar.player.must_play_comtesse()
                if(must_play_comtesse != -1):
                    gamescene.lock_button((must_play_comtesse+1)%2)
                
       
    
    @classmethod
    #L'IA joue une carte
    def card_playedAI(cls, gamescene):
        #Attente de 3 secondes
        gamescene.freeze_screen()

        current_player = cls._modelvar.playAI()
        cls.start_turn(current_player, gamescene)
       
    @classmethod
    #Fonction appelée lorsqu'un joueur a choisi une carte
    def card_played(cls, gamescene, index):
        #Vérifie si le joueur n'est pas entrain de jouer l'action du chancelier, auquel cas il ne faut pas que le programme interprète le click sur un bouton comme
        #le fait de jouer une carte
        if(cls._modelvar.player.play_chancelier):
            cls.played_chancelier(gamescene, index)
        else:
            #Action de la carte et changement de joueur courant
            current_player = cls._modelvar.play(index)
            
            #Nouveau tour
            cls.start_turn(current_player, gamescene)
    

        
    @classmethod
    #Prend dans le modèle les cartes ayant été jouées lors du round afin de les redonner à la view qui va les afficher
    def display_played_cards(cls, special_frame, call_from_special = False):
        special_frame.display_allcards(cls._modelvar.ia.cards_played, cls._modelvar.player.cards_played, cls._modelvar.get_three_cards(), cls._modelvar.cartes_defaussees, call_from_special)
    
    #Si la carte est un garde et que c'est le tour de l'utilisateur, on va afficher une écran lui montrant quelles cartes il peut 
    #deviner
    @classmethod
    def display_guard_choice(cls):
        cls._game_scene.display_guard_choice()

    
    #Si la carte est un prince, alors il pourra choisir le camp qui défausse sa carte    
    @classmethod
    def display_prince_choice(cls, jeu_joueur, jeu_ia):
        cls._game_scene.display_prince_choice(jeu_joueur, jeu_ia)
    
    #Fonction permettant d'afficher le label d'informations et d'ajouter de la lisibilité au jeu
    @classmethod
    def display_guard_ialabel(cls, card_guessed):
        cls._game_scene.display_details_label("L'IA a joué un garde\net deviné la carte : " + card_guessed)
        cls._game_scene.update_lastcardslabels("IA ", model.cards.Garde.__name__)
        cls._game_scene.update_iaUI(1)
        cls._game_scene.freeze_screen()
        cls._game_scene.undisplay_details_label()
    
    #Affichage du label récapitulatif lorsqu'un des joueurs a joué un prince
    @classmethod
    def display_prince_detailslabel(cls, current_player, side_chosen, card):
        cls._game_scene.display_details_label(str(current_player) + " a joué un prince\net choisi ce camp : " + side_chosen + "\nDéfausse : " + str(card))
        if("IA" in side_chosen):
           cls.display_AI_card(cls._modelvar.ia.cards[0])
        cls._game_scene.freeze_screen()
        cls._game_scene.undisplay_details_label()
        cls._game_scene.update_iaUI(1)
        
    @classmethod
    #Fonction appelée lorsque l'utilisateur a tenté de deviner une carte grâce au guarde
    def card_chosen(cls, special_frame, card):
        #On retire la special frame et on continue l'action du garde
        special_frame.stop_display()
        model.cards.Garde.deuxieme_action(card)
        
    @classmethod
    #Fonction appelée lorsque l'utilisateur a joué le prince et choisi le camp qui défausse sa carte
    def side_chosen(cls, special_frame, side):
        #On retir la special frame et on continue l'action du prince
        special_frame.stop_display()
        model.cards.Prince.deuxieme_action(side)
        
    @classmethod
    def display_AI_card(cls,card):
        #Affichage de la carte de l'ia, verouillage des boutons, attente de 3 secondes, déverouillage des boutons et ré affichage de la carte cachée
        cls._game_scene.display_AI_card(str(card))
        cls._game_scene.freeze_screen()
        cls._game_scene.update_iaUI(1)
        
    @classmethod
    def display_baron(cls, firstcard, secondcard):
        cls._game_scene.update_lastcardslabels(str(cls._modelvar.current_player), model.cards.Baron.__name__)
        #Affichage des cartes du joueur et de l'ia pendant 3 secondes
        cls._game_scene.display_baron(firstcard, secondcard)

    #Update l'UI de l'IA lorsqu'elle joue le chancelier, de manière à ce que le joueur puisse suivre son action
    @classmethod
    def update_chancelier_IA(cls, current_player, nbcardsia):
        cls._game_scene.update_lastcardslabels(str(current_player), model.cards.Chancelier.__name__)
        cls._game_scene.update_iaUI(nbcardsia)
        cls._game_scene.freeze_screen()
    
    #Update l'UI du joueur lorsqu'il joue un chancelier, de manière à ce qu'il puisse ensuite choisir la carte qu'il veut conserver
    @classmethod
    def update_chancelier_player(cls, current_player, playercards):
        cls._game_scene.display_details_label("Vous avez joué un chancelier\nChoisissez dans l'ordre\nles cartes que vous voulez avoir en fin de pioche") #Affichage du label d'info
        cls._game_scene.update_lastcardslabels(str(current_player), model.cards.Chancelier.__name__)
        cls._game_scene.update_playerUI(playercards) #Update de l'UI
        cls._game_scene.wait_chancelier() #Attente du choix du joueur
        
    #Fonction lancée lorsque le joueur a cliqué sur l'une des cartes qu'il souhaite mettre en bas de la pioche
    @classmethod
    def played_chancelier(cls, gamescene, index):
        gamescene.resume_game() #On reprend le jeu
        model.cards.Chancelier.deuxieme_action(cls._modelvar.player.cards[index]) #On effectue le traitement approprié
        cls._game_scene.undisplay_details_label()#On enlève le label d'info
            
    @classmethod
    #Affichage de l'écran de fin, de la manière dont s'est fini la partie, et du score de chaque joueur
    def display_victory(cls, victory_condition, score):
        cls._game_scene.view.scenes["End game scene"].victory_screen(victory_condition, score)
        

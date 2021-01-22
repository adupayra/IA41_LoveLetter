# -*- coding: utf-8 -*-
'''
Created on 26 oct. 2020

@author: Antoine
'''
import tkinter as tk
import tkinter.font
from src.controller.controller import Controller
from math import floor

    
class View(tk.Tk):
    '''
    Class which handles the creation of the window and the transition between the different scenes of the GUI (between the menu selection, the game, and  the
    victory menu
    '''
    
    def __init__(self):
        #Creates the window
        tk.Tk.__init__(self)
        
        #scales the window using the screen of the user
        ''''
        width_value = self.winfo_screenwidth()
        height_value = self.winfo_screenheight()
        self.geometry("%dx%d+0+0" % (width_value, height_value)) #Remplacer par les deux variables du dessus pour fullscreen
        '''
        #Fullscreen
        self.attributes('-fullscreen', True)
        
        #Title
        self.title("Love Letters")
        
        #Create a container for the different scenese
        container = tk.Frame(self)
        container.place(relwidth = 1, relheight = 1)
        
        #Creates the different scenes
        menu_scene = MenuScene(self, container)
        game_scene = GameScene(self, container)
        end_game_scene = EndGameScene(self, container)
        
        self._scenes = {"Menu scene":menu_scene, "Game scene":game_scene, 
                       "End game scene":end_game_scene}
        
        self.display_scene("Menu scene")
        
        #Once the gamescene is created, we notify the controller in order for it to keep an instance of it and gets it whenever it wants
        Controller.addgamescene(game_scene)
        
        self.mainloop()
            
    def display_scene(self, scene_name):
        self._scenes[scene_name].tkraise()
        
    @property
    def game_scene(self):
        return self._game_scene
    
    @property
    def scenes(self):
        return self._scenes


class MenuScene(tk.Frame):
    '''
    class responsible for the display of the menu
    '''

    def __init__(self, view, parent):
        '''
        Constructor
        '''
        
        theme1 = "orange2"
        theme2 = "orange2"
        theme3 = "#B00B1E"
        button_font = tk.font.Font(family = "Times", size = "20")
        
        #Window which will display when the player will start the application
        self._difficulty_window = None
        
        #Creates the scene      
        tk.Frame.__init__(self, parent, bg = theme1)
        self.place(relwidth = 1, relheight = 1)
        
        #Creates label title
        titre = tk.Label(self, text = "Love Letters", font = tk.font.Font(family = "Times", size = "35", weight = "bold", slant = "italic"),
                         bg = theme1, fg = theme3, pady = 25)
        titre.pack(side = tk.TOP, fill = tk.BOTH)
        
        #Creates transition button
        start_button = tk.Button(self, text = "Commencer partie", command = lambda:self.display_difficulty_choice(view), pady = 75, bg = theme3, fg = theme2,
                                 relief = tk.RIDGE, font = button_font)
        start_button.pack(side = tk.TOP, fill = tk.BOTH)
        
        #Button returning the URL which gives the rules
        rules_button = tk.Button(self, text = "Règles", command = lambda:Controller.consulter_regles(), pady = 75, bg = theme3, fg = theme2,
                                 relief = tk.RIDGE, font = button_font)
        rules_button.pack(side = tk.TOP, fill = tk.BOTH)
        
        #Button used to leave the game
        exit_button = tk.Button(self, text = "Quitter", command = lambda:Controller.quitter_jeu(), pady = 75, bg = theme3, fg = theme2,
                                relief = tk.RIDGE, font = button_font)
        exit_button.pack(side = tk.TOP, fill = tk.BOTH)
        
    #Displays the window allowing to chose the difficulty
    def display_difficulty_choice(self, view):
        
        #Creates the window if it hasn't been displayed yet
        if(self._difficulty_window is None):
            self._difficulty_window = tk.Toplevel()
            self._difficulty_window.title("Choix difficulté")
            self._difficulty_window.protocol("WM_DELETE_WINDOW", self.window_closed)
        
            #Creates the radio buttons
            var = tk.IntVar()
            radio1 = tk.Radiobutton(self._difficulty_window, text = "Intermédiaire", value = 0, 
                                    variable = var)
            radio2 = tk.Radiobutton(self._difficulty_window, text = "Difficile (pas implémenté)", value = 1, 
                                    variable = var)
            radio1.pack(anchor = tk.W)
            radio2.pack(anchor = tk.W)
            validate = tk.Button(self._difficulty_window, text = "OK", command =lambda:self.validate(view, var.get()))
            validate.pack(anchor = tk.SE)
    
    #If the window is closed without choice made, it's destroyed
    def window_closed(self):
        self._difficulty_window.destroy()
        self._difficulty_window = None
        
        
    def validate(self, view, difficulty):
        #Destruction of the second window
        self.window_closed()
        
        #Starting of the game
        Controller.start_game(view, difficulty)

    
        
class GameScene(tk.Frame):
    '''
    Cette classe contient les éléments UI du jeu
    '''

    def __init__(self, view, parent):
        '''
        Constructor
        '''
        
        #Color themes
        theme1 = 'red4'
        theme2 = 'brown4'
        
        #Font
        text_font = tk.font.Font(family = "Times", size = "14", weight = "bold")
        
        #Value used to wait for an action to resume the program
        self._var = None
        
        self._view = view

        #Creates the different pictures of the cards
        self._images = {"Espionne":tk.PhotoImage(file = "Espionne.png"), "Garde":tk.PhotoImage(file = "Garde.png"),
                        "Pretre":tk.PhotoImage(file = "Pretre.png"),"Baron":tk.PhotoImage(file = "Baron.png"), "Servante":tk.PhotoImage(file = "Servante.png"),
                        "Prince":tk.PhotoImage(file = "Prince.png"), "Chancelier":tk.PhotoImage(file = "Chancelier.png"), "Roi":tk.PhotoImage(file = "Roi.png"),
                        "Comtesse":tk.PhotoImage(file = "Comtesse.png"), "Princesse":tk.PhotoImage(file = "Princesse.png"), "Cache":tk.PhotoImage(file="Cache.png")} #Carte face cachée et princesse à ajouter
        
        
        #Creates the scene
        tk.Frame.__init__(self, parent, bg = theme1)
        self.place(relwidth = 1, relheight = 1)
        
        self.init_features(view, theme1, parent,text_font)
        
        self.init_playersUI(theme1)

        self.init_middleboard(theme2)
    
    
    '''_________________INSTANTIATION FUNCTIONS OF THE GUI ELEMENTS_____________'''
       
    #Initialize the GUI elements of features 
    def init_features(self, view, theme1, container, text_font):
        theme = 'goldenrod'
        
        #Container of quit button
        quit_frame = tk.Frame(self, bg = theme1, highlightthickness = 3, highlightbackground = theme)
        
        #Creates of the button used to leave the application
        button_quit = tk.Button(quit_frame, text="Quit game", command=lambda:Controller.quitter_jeu(), font = text_font, bg = theme1, fg = theme)
        quit_frame.place(relx = 0, rely = 1, y =-button_quit.winfo_reqheight() - 5)
        button_quit.pack()
        
        #Creates the label displaying the player whose turn it is
        self._tour_label = tk.Label(self, font = text_font, fg = theme, bg = theme1)
        self._tour_label.place(relx = 0.2, rely = 0.7)
        
        #Creates the label displaying the gamee's info
        self._info_label = tk.Label(self, text="Idle", font = text_font, fg = theme, bg = theme1)
        self._info_label.place(rely=0.325)
        
        #Creates the label displaying the last card played
        self._last_card_label = tk.Label(self, bg = theme1, image = self._images["Cache"])
        self._last_card_label.place(rely = 0.325, y = self._info_label.winfo_reqheight())
        
        #Creates the frame which is displayed on top of the game scene when the user wants to view the cards or when he has to chose between multiple options
        #(after playing the prince or the guard for instance)
        self._special_frame = SpecialFrame(container, theme1, self)
        
        #Container of the feature buttons
        container_features = tk.Frame(self, bg = theme1, highlightthickness = 3, highlightbackground = theme)
        container_features.pack(side = tk.RIGHT)
        
        #Button used to display the list of cards of the game
        boutton_reminder = tk.Button(container_features, command = lambda:self._special_frame.display_reminder(), text = "Rappel des cartes",
                                     bg = theme1, fg = theme, font = text_font)
        boutton_reminder.pack(fill = tk.BOTH)
        
        #Button used to display the cards played
        boutton_played_cards = tk.Button(container_features, text = "Consulter cartes jouées", command = lambda:Controller.display_played_cards(self._special_frame),
                                         bg = theme1, fg = theme, font = text_font)
        boutton_played_cards.pack()
        
        #Frames containing the player's tokens
        self._token_frames = (tk.Frame(self, bg = theme1, highlightbackground = theme, highlightthickness = 3),
                              tk.Frame(self, bg = theme1, highlightbackground = theme, highlightthickness = 3))
        
        #Picture of a token
        self._tokenimage = tk.PhotoImage(file = "Jeton.png")
        
        #Frames containing the labels (one for the player and one for the AI)
        self._token_frames[0].place(relx = 0.75, rely = 0.05)
        self._token_frames[1].place(relx = 0.75, rely = 0.7)
        #Labels "points"
        points_label = (tk.Label(self._token_frames[0], text = "points : ", bg = theme1, fg = theme, font = text_font),
                        tk.Label(self._token_frames[1], text = "points : ", bg = theme1, fg = theme, font = text_font))
        points_label[0].grid(row = 0, column = 0)
        points_label[1].grid(row = 0, column = 0)
        
        #Tokens labels
        self._token_labels = []
        
        #Creation of the list containing the list of all the labels of the player and a list for all the buttons of the AI
        for i in range (0,2):
            temp = []
            for _ in range(0,5):
                temp.append(tk.Label(self._token_frames[i], bg = theme1, fg = theme, image = self._tokenimage))
            self._token_labels.append(temp)
            
        self._details_label = tk.Label(self, bg = theme1, fg = theme, font = text_font)
        
        
    #Initialization off the GUI elements of the player and the AI
    def init_playersUI(self, theme1):
        #Buttons coresponding to the displaying of the hand of the AI (purely visual)
        self._ia_labels = (tk.Label(self, image=self._images["Cache"], borderwidth=0, highlightthickness=0), 
                           tk.Label(self, image="", borderwidth=0, highlightthickness=0, bg=theme1), 
                           tk.Label(self, image="", borderwidth=0, highlightthickness=0, bg=theme1))
        self._ia_labels[0].place(rely=0, relx=0.5, x=-self._ia_labels[0].winfo_reqwidth())
        
        #Buttons of the user, used to chose the card to play
        self._player_buttons = (tk.Button(self, command=lambda:Controller.card_played(self, 0), borderwidth=0, highlightthickness=0),
                                tk.Button(self, command=lambda:Controller.card_played(self, 1), borderwidth=0, highlightthickness=0),
                                tk.Button(self, command=lambda:Controller.card_played(self, 2), borderwidth=0, highlightthickness=0))
        #The 3d button is here to handle the counselor case
        
        self._player_buttons[0].place(rely=1, relx=0.5, x=-self._ia_labels[0].winfo_reqwidth(), y=-self._ia_labels[0].winfo_reqheight())



    def init_middleboard(self, theme2):
        """       
        
        Middle of the board : container used to display the widgets easily (the 3rd cards of the beginningof a round and the deck)
        
        """
        #Container creation
        container = tk.Frame(self, bg=theme2, highlightbackground='dark goldenrod1', highlightthickness=3)
        container.place(relx=0.2, rely=0.325, relwidth=0.6, relheight=0.35)
        
        #Creation of the labels on which we will display the pictures
        espace = tk.Label(container, text=" ", bg=theme2).pack(side=tk.LEFT) #Used for a prettier display
        self._label_milieux = (tk.Label(container, borderwidth=0, highlightthickness=0), 
                               tk.Label(container, borderwidth=0, highlightthickness=0), 
                               tk.Label(container, borderwidth=0, highlightthickness=0), 
                               tk.Label(container, image=self._images["Cache"], borderwidth=0, highlightthickness=0))
        self._label_milieux[0].pack(side=tk.LEFT)
        self._label_milieux[1].pack(side=tk.LEFT)
        self._label_milieux[2].pack(side=tk.LEFT)
        espace = tk.Label(container, text=" ", bg=theme2).pack(side=tk.RIGHT) #Used for a prettier display
        self._label_milieux[3].pack(side=tk.RIGHT)
        

    '''______________________END OF THE INSTANTIATION FUNCTIONS OF THE GUI ELEMENTS___________'''
        
    @property
    def images(self):
        return self._images
    
    @property
    def view(self):
        return self._view
        
    
    #Functions called in the beginning of a round : it displays the 3 cards shown at the beginning of the game, it resets the gamescene in case of new round
    def init_round(self, three_cards, string_joueur, score_ia, score_player):
        #Resets the gamescene
        self.update_tokens(score_ia, score_player)
        self.unlock_buttons()
        self._last_card_label['image'] = self._images["Cache"]
        
        #Displays the 3 cards et the label of the beginning of the round
        for i in range(0,3):
            self._label_milieux[i].config(image = self._images[three_cards[i]])
        
        self._info_label['text'] = "c'est à " + string_joueur + " de commencer !" #Displays the beginner player
             
    #Function used to update the GUI with the information regarding the hand of the user
    def update_playerUI(self, cards):
        
        #Ca ne marche pas avec la fonction winfo_ismapped, donc on met un identificateur pour différencier les boutons affichés à l'écran et ceux qui ne le sont pas
        number_cards_displayed = sum(button['text'] != "" for button in self._player_buttons) #Counts the number of buttons of the user
        number_cards_todisplay = cards.__len__() #Number of cards to display
        
        self._player_buttons[0].config(image = self.images[str(cards[0])])
        #Disjonction of the cases where there's more cards to display than available buttons and the cases where there are too much buttons available on the screen
        #for the number of cards to display
        if(number_cards_todisplay >= number_cards_displayed ):
            #In that case, we update the cards of the already available buttons
            for i in range(0,number_cards_displayed):
                self._player_buttons[i].config(image = self._images[cards[i]])
                self._player_buttons[i]['text'] = " "
            
            #We then display the number of buttons we need in order to display all the cards
            for i in range(number_cards_displayed, number_cards_todisplay):
                self._player_buttons[i].config(image = self._images[cards[i]])
                self._player_buttons[i]['text'] = " "
                self._player_buttons[i].place(rely = 1, relx = 0.5, x = (i-1) * self._ia_labels[0].winfo_reqwidth(), y = -self._ia_labels[0].winfo_reqheight())
                
                
        elif(number_cards_displayed > number_cards_todisplay):
            #Update the buttons we need
            for i in range(0, number_cards_todisplay):
                self._player_buttons[i]['text'] = " "
                self._player_buttons[i].config(image = self._images[cards[i]])
            #Remove the buttons we don't need anymore
            for i in range(number_cards_todisplay, number_cards_displayed):
                self._player_buttons[i]['text'] = ""
                self._player_buttons[i].place_forget()

    #Function used to update the GUI thanks to the number of cards of the AI (same principle as for the user's update)
    def update_iaUI(self, nbcards):
        number_cards_displayed = sum(label["image"] != "" for label in self._ia_labels)
        
        self._ia_labels[0]['image'] = self.images["Cache"] #Security since anyway the AI will only have one card in hand
        
        if(nbcards > number_cards_displayed):
            for i in range(number_cards_displayed, nbcards):
                self._ia_labels[i]['image'] = self._images["Cache"]
                self._ia_labels[i].place(relx = 0.5, x = (i-1) * self._ia_labels[0].winfo_reqwidth())
        elif(number_cards_displayed > nbcards):
            for i in range(nbcards, number_cards_displayed):
                self._ia_labels[i].config(image = "")
    
    #Updates the label displaying the last card played
    def update_lastcardslabels(self, joueur, card):
        self._info_label['text'] = joueur + " a joué la carte " + card
        self._last_card_label['image'] = self._images[card]
        
    #Updates the label indicating whose turn it is
    def update_tour_label(self, text):
        self._tour_label['text'] = text
        
    #Updates the labels and the pictures of the tokens
    def update_tokens(self, score_ia, score_player):
        #Checks the nubmer of tokens displayed for the AI and the user
        sum_ia = sum(button.winfo_ismapped() for button in self._token_labels[0])
        sum_player = sum(button.winfo_ismapped() for button in self._token_labels[1])
        
        #Displays the number of tokens needed for the AI
        for i in range(0, score_ia):
            self._token_labels[0][i].grid(row = floor(i/3), column = i%3 + 1)
        #Removes the tokens displayed we don't need (in case of new game)
        for i in range(score_ia, sum_ia):
            self._token_labels[0][i].grid_forget()
        
        #Same but for user
        for i in range(0, score_player):
            self._token_labels[1][i].grid(row = floor(i/3), column = i%3 + 1)
        for i in range(score_player, sum_player):
            self._token_labels[1][i].grid_forget()
    
    #Function used to lock the buttons when the AI plays
    def lock_buttons(self):
        for button in self._player_buttons:
            button.config(state = 'disabled')
            
    def lock_button(self, index):
        self._player_buttons[index].config(state = 'disabled')
    
    #Function used to unlock the buttons
    def unlock_buttons(self):
        for button in self._player_buttons:
            button.config(state = 'normal')
    
    #Function used to display the window allowing the user to chose which cards to guess (when he played a guard)
    def display_guard_choice(self):
        self._special_frame.display_guard_choice()
    
    #Same but for prince
    def display_prince_choice(self, jeu_joueur, jeu_ia):
        self._special_frame.display_prince_choice(jeu_joueur, jeu_ia)
        
    def display_AI_card(self, card):
        self._ia_labels[0]['image'] = self._images[card]

    #Function used to replace the first button when it is place_forget
    def replace_button(self):
        self._player_buttons[0].tkraise()
        self._player_buttons[0].place(rely=1, relx=0.5, x=-self._ia_labels[0].winfo_reqwidth(), y=-self._ia_labels[0].winfo_reqheight())
    
    #Starts the display function of the Baron
    def display_baron(self, player, ia):
        self._special_frame.display_baron_screen(player, ia)
        
    #Displays the info label
    def display_details_label(self, text_to_display):
        self._details_label['text'] = text_to_display
        self._details_label.place(relx = 0.1, rely = 0.8)
    
    #Removes the info label of the counselor
    def undisplay_details_label(self):
        self._details_label.place_forget()
        
    #Stops the program while waiting for the player to chose the card he wants to keep when he played the counselor
    def wait_chancelier(self):
        self._var = tk.IntVar()
        self.wait_variable(self._var)
        
    #Resumes the program when it is interrupted by a particular event (doesn't include all events)
    #(exceptions : displays the special frames and wait for 3 sec before resuming the program)
    def resume_game(self):
        self._var.set(1)
        self._var = None
        
    #Stops program for 3 seconds
    def freeze_screen(self):
        self.lock_buttons() #Restrains the user to do any action during the freeze
        self._var = tk.IntVar()
        self.after(3000, self._var.set, 1)
        self.wait_variable(self._var)
        self._var = None
        self.unlock_buttons() #unlock the buttons
        
    
class SpecialFrame(tk.Frame):
    '''
    Ugly class, but it works. Have to do it again if we have time
    
    class used to display a new frame on top of the game scene. Used to display the info such as the cards played during the round
    or to allow the user to make some choice when he played some cards (guard and prince)
    '''
    
    def __init__(self, parent, color, gamescene):
        #Creation of the window
        tk.Frame.__init__(self, parent, bg = color)
        
        #Configuration of the window and declaration of the differnt colors and fonts used to have a prettier interface
        self.grid_columnconfigure(0, weight = 1)
        self.grid_columnconfigure(1, weight = 1)
        self.grid_columnconfigure(2, weight = 1)
        theme2 = 'goldenrod'
        
        cards_played_font = tk.font.Font(family = "Times", size = "14")
        
        prince_buttons_color = 'brown4'
        prince_buttons_font = tk.font.Font(family = "Times", size = '30', weight = "bold")
        
        #Instance of the gamescene
        self._gamescene = gamescene
        
        #Frame containing the button leave feature
        self._leave_feature_frame = tk.Frame(self, bg = color, highlightbackground = theme2, highlightthickness = 3)
        
        #Button used to get back to the game
        _leave_feature = tk.Button(self._leave_feature_frame, text = "Retourner au jeu", command = lambda:self.stop_display(), font = cards_played_font,
                                        bg = color, fg = theme2)
        _leave_feature.pack()
        
        #Labels used to display the cards played and the cards recall (21 for 21 cards in total)
        self._displayerslabels = []
        
        #Buttons used to guess the AI's card when the user played a guard
        self._actionbuttons = []
        
        #Instantiates the buttons and part of the labels
        for i in range(0,9):
            self._actionbuttons.append(tk.Button(self))

            self._displayerslabels.append(tk.Label(self, bg = color))

        #Instantiates the rest of the labels
        for i in range(9, 21):
            self._displayerslabels.append(tk.Label(self, bg = color))
        
        #Frame only used as a container of the buttons (used to put a border in color)
        self._prince_frames = (tk.Frame(self, bg = color, highlightbackground = theme2, highlightthickness = 3),
                               tk.Frame( self, bg = color, highlightbackground = theme2, highlightthickness = 3))
        
        #Instantiates the buttons used by the user to chose the player who has to throw its card
        prince_buttons = (tk.Button(self._prince_frames[0], text = "Votre jeu", command = lambda:Controller.side_chosen(self, prince_buttons[0]['text']), 
                                          bg = prince_buttons_color, highlightbackground = theme2, highlightthickness = 3,font = prince_buttons_font, fg = theme2),
                                tk.Button(self._prince_frames[1], text = "Le jeu adverse", command = lambda:Controller.side_chosen(self, prince_buttons[1]['text']),
                                          highlightbackground = theme2, highlightthickness = 3, bg = prince_buttons_color, font = prince_buttons_font, fg = theme2))
        prince_buttons[0].pack(expand = True, fill = tk.BOTH)
        prince_buttons[1].pack(expand = True, fill = tk.BOTH)
        
        #Labels of text used when displaying the played cards
        self._side_labels = (tk.Label(self, text = "Cartes jouées par l'IA", bg = color, fg = theme2, font = cards_played_font),
                             tk.Label(self, text = "Cartes jouées par vous", bg = color,fg = theme2, font = cards_played_font),
                             tk.Label(self, text = "3 premières cartes", bg = color, fg = theme2, font = cards_played_font),
                             tk.Label(self, text = "Choisissez une carte", bg = color, fg = theme2, font = cards_played_font))
        
        #Copy used to keep in memory the widgets in case where we want to display another window while being able to coming back to the previous one
        self._copie = []
        
        #Container of the button
        self._see_played_cards_frame_prince = tk.Frame(self, bg = color, highlightthickness = 3, highlightbackground = theme2)
        
        #Button used to see the played cards from another window than the gamescene window
        see_played_cards_prince = tk.Button(self._see_played_cards_frame_prince, text = "Voir cartes jouées", command = lambda:self.make_copy(), bg = prince_buttons_color, fg = theme2,
                                     font = prince_buttons_font)
        see_played_cards_prince.pack(expand = True, fill = tk.BOTH)
        
        #Container of the button
        self._see_played_cards_frame_garde = tk.Frame(self, bg = color, highlightthickness = 3, highlightbackground = theme2)
        
        #button
        see_played_cards_garde = tk.Button(self._see_played_cards_frame_garde,  text = "Voir cartes jouées", command = lambda:self.make_copy(), bg = prince_buttons_color,
                                           fg = theme2, font = cards_played_font)
        
        see_played_cards_garde.pack(expand = True, fill = tk.BOTH)
        
        #Display label of the baron's screen
        self._baron_label = tk.Label(self, text = "Un baron a été joué, comparaison de vos cartes : ", bg = color, font = cards_played_font, fg = theme2)
        
        #Container of the back to the last frame button
        self._return_last_frame_frame = tk.Frame(self, bg = color, highlightbackground = theme2, highlightthickness = 3)
        
        #Button used to go back to the last frame
        return_last_frame = tk.Button(self._return_last_frame_frame, text = "Retour à la séléction", command = lambda:self.retour(), font = cards_played_font, bg = color,
                                            fg = theme2)
        return_last_frame.pack()
        
        #Attributes the picture to the buttons used to guess a card (when a guard is played)
        self._actionbuttons[0]['image'] = self._gamescene.images['Espionne']
        self._actionbuttons[1]['image'] = self._gamescene.images['Pretre']
        self._actionbuttons[2]['image'] = self._gamescene.images['Baron']
        self._actionbuttons[3]['image'] = self._gamescene.images['Servante']
        self._actionbuttons[4]['image'] = self._gamescene.images['Prince']
        self._actionbuttons[5]['image'] = self._gamescene.images['Chancelier']
        self._actionbuttons[6]['image'] = self._gamescene.images['Roi']
        self._actionbuttons[7]['image'] = self._gamescene.images['Comtesse']
        self._actionbuttons[8]['image'] = self._gamescene.images['Princesse']
        
        #Events to trigger in case of a click on those buttons
        self._actionbuttons[0].configure(command = lambda:Controller.card_chosen(self, self.search_card(0)))
        self._actionbuttons[1].configure(command = lambda:Controller.card_chosen(self, self.search_card(1)))
        self._actionbuttons[2].configure(command = lambda:Controller.card_chosen(self, self.search_card(2)))
        self._actionbuttons[3].configure(command = lambda:Controller.card_chosen(self, self.search_card(3)))
        self._actionbuttons[4].configure(command = lambda:Controller.card_chosen(self, self.search_card(4)))
        self._actionbuttons[5].configure(command = lambda:Controller.card_chosen(self, self.search_card(5)))
        self._actionbuttons[6].configure(command = lambda:Controller.card_chosen(self, self.search_card(6)))
        self._actionbuttons[7].configure(command = lambda:Controller.card_chosen(self, self.search_card(7)))
        self._actionbuttons[8].configure(command = lambda:Controller.card_chosen(self, self.search_card(8)))
        
        #Thrown cards label
        self._defausse_label = tk.Label(self, text = "Cartes défaussées : ", bg = color, fg = theme2, font = cards_played_font)
    
    #Used to return a string corresponding to the button chosen by the user
    def search_card(self, index):
        if(index == 0):
            return "Espionne"
        elif index == 1:
            return "Pretre"
        elif index == 2:
            return "Baron"
        elif index == 3:
            return "Servante"
        elif index == 4:
            return "Prince"
        elif index == 5:
            return "Chancelier"
        elif index == 6:
            return "Roi"
        elif index == 7:
            return "Comtesse"
        elif index == 8:
            return "Princesse"
    
    
    #Displays all the cards of the game, it's a recall of the different cards for the user
    def display_reminder(self):
        self.place(relwidth = 1, relheight = 1)
        self.tkraise()
        self._gamescene.place_forget()
        
        #Attribution of the pictures to the labels
        self._displayerslabels[0]['image'] = self._gamescene.images['Espionne']
        self._displayerslabels[1]['image'] = self._gamescene.images['Garde']
        self._displayerslabels[2]['image'] = self._gamescene.images['Pretre']
        self._displayerslabels[3]['image'] = self._gamescene.images['Baron']
        self._displayerslabels[4]['image'] = self._gamescene.images['Servante']
        self._displayerslabels[5]['image'] = self._gamescene.images['Prince']
        self._displayerslabels[6]['image'] = self._gamescene.images['Chancelier']
        self._displayerslabels[7]['image'] = self._gamescene.images['Roi']
        self._displayerslabels[8]['image'] = self._gamescene.images['Comtesse']
        self._displayerslabels[9]['image'] = self._gamescene.images['Princesse']
        
        j= 0
        last_column = self.compute_last_column(0, self._displayerslabels[0].winfo_reqwidth())
        #Loop through the dictionary of images (-1 because of the hidden card picture)
        for i in range(0, self._gamescene.images.__len__() - 1):
            #Condition used to get to the next line when there's no more space on the screen of the user
            if(i != 0 and i%last_column == 0):
                j+=1
            
            #Displays the label
            self._displayerslabels[i].grid(row = j, column = i%last_column)
        #Displays the button to go back to game
        self._leave_feature_frame.grid(row = j+1, column = i%last_column)
    
        self._gamescene.wait_visibility()
        
    #Displays all the cards which were played during the round
    def display_allcards(self, ia_cards, player_cards, middle_cards, cartes_defausse, call_from_special = False):
        self.place(relwidth = 1, relheight = 1)
        self.tkraise()
        self._gamescene.place_forget()
        
        #Configuration of the grid (purely visual)
        self.grid_columnconfigure(0, weight = 0)
        self.grid_columnconfigure(1, weight = 0)
        self.grid_columnconfigure(2, weight = 0)
        
        #Displays the cards used by the AI while taking the screen's width into account
        i = self.display_cards_side(ia_cards, 0, self._side_labels[0], 0, self._displayerslabels)
        j = 1
        
        #Displays the cards of the middle on the next line
        self._side_labels[2].grid(row = i, column=0)
        for p in range(ia_cards.__len__(), ia_cards.__len__() + 3):
            self._displayerslabels[p]['image'] = self._gamescene.images[str(middle_cards[j-1])]
            self._displayerslabels[p].grid(row = i, column = j)
            j+=1
        
        #Checks if the function is called via the gamescene or the specialframe
        if(call_from_special):
            self._return_last_frame_frame.grid(row = i, column = j) #If the function is called from the special frame, the button is displayed, allowing to come back to the previous
                                                                    #specialframe
        else:
            self._leave_feature_frame.grid(row = i, column = j) #Button used to come back to the gamescene
        
        #Displays the thrown cards
        j += 1
        p+=1
        self._defausse_label.grid(row = i, column = j)
        j+=1
        for k in range(0, cartes_defausse.__len__()):
            self._displayerslabels[p]['image'] = self._gamescene.images[str(cartes_defausse[k])]
            self._displayerslabels[p].grid(row = i, column = j+k)
            p+=1
        
        i+=1
        
        #Display the cards used by the player
        self.display_cards_side(player_cards, i, self._side_labels[1], ia_cards.__len__() + 5 + cartes_defausse.__len__(), self._displayerslabels)
        
        self._gamescene.wait_visibility()
     
    #Used to display the GUI elements of the special frame
    #Considering the screen's size, it is possible to have display problems on the height of the screen
    def display_cards_side(self, side, row, label, labelindex, widgets):
        #Displays the descriptive label
        j=1
        label.grid(row = row, column = 0)
        
        label_index = labelindex
        
        #Determines the number of cards that we can place in width before being out of the screen
        last_column = self.compute_last_column(widgets[0].winfo_reqwidth(), self._gamescene.images['Espionne'].width())
        
        #Displays the cards
        for p in range(0, side.__len__()):
            widgets[label_index].configure(image = self._gamescene.images[str(side[p])])
            widgets[label_index].grid(row = floor(j/(last_column+1)) + row, column = j%(last_column+1))
            label_index += 1
            j+=1
        
        return row + 1
    

    #Displays the buttons used by the user when he choses who has to throw its card
    def display_prince_choice(self, jeu_joueur, jeu_ia):
        self.place(relwidth = 1, relheight = 1)
        self.tkraise()
        self._gamescene.place_forget()
        
        #Visual configuration of the grid
        self.grid_columnconfigure(0, weight = 1)
        self.grid_columnconfigure(1, weight = 1)
        self.grid_columnconfigure(2, weight = 1)
        
        self._prince_frames[0].winfo_children()[0]['text'] = jeu_joueur
        self._prince_frames[1].winfo_children()[0]['text'] = jeu_ia
        
        self._prince_frames[0].grid(sticky = 'nesw', columnspan = 10, ipady = 50)
        self._prince_frames[1].grid(sticky = 'nesw', columnspan = 10, ipady = 50)
        
        self._see_played_cards_frame_prince.grid(sticky = 'nesw', columnspan = 10, ipady = 50)
        
        self._gamescene.wait_visibility()
    
    #Displays the possibilities of guess the user can do
    def display_guard_choice(self):
        self.place(relwidth = 1, relheight = 1)
        self.tkraise()
        self._gamescene.place_forget()
        
        self.display_cards_side(["Espionne", "Pretre", "Baron", "Servante", "Prince", "Chancelier", "Roi", "Comtesse", 
                                 "Princesse"], 0, self._side_labels[3], 0, self._actionbuttons)
        
        self._see_played_cards_frame_garde.grid()
        
        self._gamescene.wait_visibility()
    
    #Displays the screen when a baron is played
    def display_baron_screen(self, currentplayercard, othercard):
        self._gamescene.freeze_screen()
        self.place(relwidth = 1, relheight = 1)
        self.tkraise()
        self._gamescene.place_forget()
        
        self._baron_label.grid()
        self._displayerslabels[0]['image'] = self._gamescene.images[str(currentplayercard)]
        self._displayerslabels[1]['image'] = self._gamescene.images[str(othercard)]
        self._displayerslabels[1].grid(row = 0, column = 1)
        self._displayerslabels[0].grid(row = 0, column = 2)
        
        #Waits 3sec before removing the display
        self._gamescene.freeze_screen()
        self.stop_display()
        
    #Remove the frame, to do this, it removes the display of all the elements being on the frame, and then removes the frame
    def stop_display(self):

        for widget in self.winfo_children():
                widget.grid_forget() #"forgets" all the elements
        self.place_forget() #"forgets" the frame
        
        self._gamescene.place(relwidth = 1, relheight = 1)
        
        #When we place_forget the gamescene, its buttons are place_forget with it, we therefore have to replace the first button of the player
        self._gamescene.replace_button()
    
    #Used to determine the maximum column that can fit in the screen
    def compute_last_column(self, first_width, unite):
        sum_width = first_width
        last_column = 0
        while(sum_width + unite < self.winfo_screenwidth()):
            sum_width += unite
            last_column +=1
        return last_column
    
    #Used to do a copy of the displayed elements of the screen whe nwe want to display them back later
    def make_copy(self):
        for x in self.winfo_children():
            if(x.winfo_ismapped()):
                self._copie.append(x)
                
        self.stop_display() #In order to display the elements again, we refresh the frame
        Controller.display_played_cards(self, True) #Display the cards played
        
    #Used to come back to the configuration of the last special frame
    def retour(self):
        self.stop_display() #Updates
        if(self._copie[0] is self._prince_frames[0]): #Search which info were displayed
            Controller.display_prince_choice(self._copie[0].winfo_children()[0]['text'], self._copie[1].winfo_children()[0]['text'])
        else:
            Controller.display_guard_choice()
        self._copie = [] #Clear the buffer
        
class EndGameScene(tk.Frame):
    '''
    Class which handles the display of the end game scene (end of round and end of game)
    '''

    def __init__(self, view, parent):
        '''
        Constructor
        '''
        theme1 = "peach puff"
        theme2 = "white"
        text_font = tk.font.Font(family = "Courier", size = "30")
        #Creates the scene
        tk.Frame.__init__(self, parent, bg = theme1)
        self.place(relwidth = 1, relheight = 1)
        
        #Victory text
        self._label_victory = tk.Label(self, text = "", bg = theme1, fg = theme2, font = text_font)
        self._label_victory.pack()
        
        #Token picture
        self._image = tk.PhotoImage(file = "Jeton.png")
        
        #Container of the tokens of the user and the AI
        player_container = (tk.Frame(self, bg = theme1), tk.Frame(self, bg = theme1))
        player_container[0].pack()
        player_container[1].pack()
        
        #Labels of the player and the AI
        player_labels = (tk.Label(player_container[0], text = "Vos points : ", bg = theme1, font = text_font), 
                         tk.Label(player_container[1], text = "Points de l'IA : ", bg = theme1, font = text_font))
        player_labels[0].pack(side = tk.LEFT)
        player_labels[1].pack(side = tk.LEFT)
        
        #Tokens' labels
        #Labels des jetons
        self._tokenlabels = []
        for i in range(0,2):
            temp = []
            for _ in range(0,6):
                temp.append(tk.Label(player_container[i], bg = theme1, image = self._image))
            self._tokenlabels.append(temp)
        
        
        #Buttons to come back to the menu/get to the next round
        retour_menu_button = tk.Button(self, text = "Retour au menu", 
                                      command = lambda:Controller.display_scene(view, "Menu scene"))
        self._next_round_button = tk.Button(self, text = "Prochain round", 
                                      command = lambda:Controller.start_game(view, -1))
        retour_menu_button.pack()
        self._next_round_button.pack()
    
    #Function used to display the winner
    def victory_screen(self, text, score):

        self.tkraise()
        self._label_victory['text'] = text
        
        #If more than a game has been played, the button will be unpack, we therefore need to display it again
        self._next_round_button.pack()
        
        #Clear the tokens (in case there's too much of them)
        #Clear les tokens (au cas où il y en ait en trop)
        for i in range(0, self._tokenlabels.__len__()):
            for j in range(0, self._tokenlabels[i].__len__()):
                self._tokenlabels[i][j].pack_forget()
        
        #Displays the score
        for i in range(0, score[0]):
            self._tokenlabels[0][i].pack(side = tk.LEFT)
            
        for i in range(0, score[1]):
            self._tokenlabels[1][i].pack(side = tk.LEFT)
            
        #Dissociates the cases where it's the end of a round and the end of a game
        if score[0] >= 6 or score[1] >= 6:
            self._next_round_button.pack_forget() #Deactivates the next round buttons if it is the end of the game


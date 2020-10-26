# -*- coding: utf-8 -*-
'''
Created on 26 oct. 2020

@author: Antoine
'''

import tkinter as tk

class GameScene(tk.Frame):
    '''
    Cette classe contient les éléments UI du jeu
    Elle est composée 
    '''


    def __init__(self, parent):
        '''
        Constructor
        '''
        tk.Frame.__init__(self, parent, bg = 'blue')
        self.place(relwidth = 1, relheight = 1)
        
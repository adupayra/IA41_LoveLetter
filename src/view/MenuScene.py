# -*- coding: utf-8 -*-
'''
Created on 26 oct. 2020

@author: Antoine
'''

import tkinter as tk

class MenuScene(tk.Frame):
    '''
    Classe responsable de l'affichage du menu
    '''


    def __init__(self):
        '''
        Constructor
        '''
        tk.Frame.__init__(self, bg = 'green')
        self.place(relwidth = 1, relheight = 1)
        
        
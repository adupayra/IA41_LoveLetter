# -*- coding: utf-8 -*-
'''
Created on 26 oct. 2020

@author: Antoine
'''

from abc import ABC
import tkinter as tk

class SceneTemplate(ABC, tk.Frame):
    '''
    Classe permettant de définir les attributs et méthodes qu'implémenteront toutes les scènes utilisées
    '''


    def __init__(self):
        '''
        Constructor
        '''
        #abc.__init__()
        #tk.Frame.__init__(self, View.getInstance())
        self.place(relwidth = 1, relheight = 1)
        
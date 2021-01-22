# -*- coding: utf-8 -*-
'''                 
Created on 30 oct. 2020

@author: Antoine
'''

import src.controller.controller as controller
import src.model.model as model
import src.view.view as view
import os   

def main():
    #We change the current directory in order to place inside the resource directory
    path_ressources = os.path.dirname(os.path.abspath(__file__))
    os.chdir(path_ressources)
    os.chdir(os.pardir)
    os.chdir("resources")
    controller.Controller._modelvar = model.Model(controller.Controller)
    controller.Controller._viewvar = view.View()

        
if __name__ == '__main__':
    main()
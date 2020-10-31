'''
Created on 30 oct. 2020

@author: Antoine
'''

import src.controller.controller as controller
import src.model.model as model
import src.view.view as view
import os

def main():
    view.View()
    controller.modelvar = model.Model()

    
if __name__ == '__main__':
    main()
    

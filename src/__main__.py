'''             
Created on 30 oct. 2020

@author: Antoine
'''

import src.controller.controller as controller
import src.model.model as model
import src.view.view as view

def main():
    controller.Controller._modelvar = model.Model(controller.Controller)
    controller.Controller._viewvar = view.View()
    
    
    

    
if __name__ == '__main__':
    main()
    

import random
import re

class Board:
    def __init__(self, dim_size, num_bombs):
        
        self.dim_size = dim_size
        self.num_bombs = num_bombs

        
        self.board = self.make_new_board()
        self.assign_values_to_board()

        
        self.dug = set()

    def make_new_board(self): 
        return []  

    def assign_values_to_board(self): 
        pass

    def get_num_neighboring_bombs(self, row, col): 
        pass

    def dig(self, row, col): 
        pass

    def __str__(self): 
        return ''

def play(dim_size=10, num_bombs=10): 
    pass

if __name__=='__main__':
    play()
    
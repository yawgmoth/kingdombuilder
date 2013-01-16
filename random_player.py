import random

class RandomPlayer:
    def __init__(self, name):
        self.name = name
        
    def inform_board(self, board):
        pass
        
    def inform_addpiece(self, where, color):
        pass
        
    def inform_removepiece(self, where):
        pass
        
    def inform_endgame(self, scores):
        pass
        
    def inform_actions(self, actions, rotate=False):
        self.actions = actions        
        
    def ask_target(self, options, source):
        return random.choice(options)
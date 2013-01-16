class PlayerInterface:
    def __init__(self, name):
        pass
        
    def inform_board(self, board):
        pass
        
    def inform_addpiece(self, where, color):
        pass
        
    def inform_removepiece(self, where):
        pass
        
    def inform_endgame(self, scores):
        pass
        
    def inform_actions(self, actions, rotate=False):
        pass
        
    def ask_target(self, options, source):
        pass

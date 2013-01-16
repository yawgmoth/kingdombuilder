class ConsolePlayer:
    def __init__(self, name):
        self.name = name
        self.actions = []
        self.board = None
        
    def inform_board(self, board):
        self.board = board
        
    def inform_addpiece(self, where, color):
        pass
        
    def inform_removepiece(self, where):
        pass
        
    def inform_endgame(self, scores):
        pass
        
    def inform_actions(self, actions, rotate=False):
        self.actions = actions
        if rotate:
            print "new action:", actions[-1]
        else:
            for a in actions:
                print "action:", a
        
        
    def ask_target(self, options, source):
        try:
            w, h = self.board.dimension
            print self.name
            print "  action:", source
            for y in xrange(h):
                print "  ",
                for x in xrange(w):
                    print self.board.pieces[y*h+x],
                print
            print "  possible choices:",
            for o in options:
                print o,
            print
            return int(raw_input("your choice %s> "%self.name))
        except Exception:
            return self.ask_target(options, source)
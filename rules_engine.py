import random

from constants import *

class TerrainAction:
    def __init__(self, type):
        self.type = type
        self.action_type = PUT_ACTION
        
    def perform(self, player, board):
        options = []
        for i, b in enumerate(board.pieces):
            if b[0] == self.type and b[1] == -1:
                options.append(i)
        real_options = []
        for o in options:
            neigh = board.get_neighbours(o)
            keep = False
            for n in neigh:
                if n[1] == player.id:
                    keep = True
            if keep:
                real_options.append(o)
        if not real_options:
            real_options = options
        if not real_options: return
        target = player.interface.ask_target(real_options, self)
        if target not in real_options:
            return self.perform(player, board)
        board.pieces[target][1] = player.id
        player.rules_engine.inform_all_addpiece(target, player.id)
    
    def __str__(self):
        return "TerrainAction(%d)"%self.type
        
class RemoveAction:
    def __init__(self):
        self.action_type = REMOVE_ACTION
        
    def perform(self, player, board):
        options = []
        for i, b in enumerate(board.pieces):
            if b[1] != -1:
                options.append(i)
        if not options:
            return
        target = player.interface.ask_target(options, self)
        if target not in options:
            return self.perform(player, board)
        board.pieces[target][1] = -1
        player.rules_engine.inform_all_removepiece(target)
    
    def __str__(self):
        return "RemoveAction"
        
class SwitchAction:
    def __init__(self):
        self.action_type = SWITCH_ACTION
        
    def perform(self, player, board):
        options = []
        for i, b in enumerate(board.pieces):
            if b[1] != -1:
                options.append(i)
        if len(options) < 2:
            return
        target = player.interface.ask_target(options, self)
        if target not in options:
            return self.perform(player, board)
        options.remove(target)
        
        target1 = player.interface.ask_target(options, self)
        if target1 not in options:
            return self.perform(player, board)
        tmp = board.pieces[target1][1]
        board.pieces[target1][1] = board.pieces[target][1]
        board.pieces[target][1] = tmp
        player.rules_engine.inform_all_removepiece(target)
        player.rules_engine.inform_all_addpiece(target, tmp)
        player.rules_engine.inform_all_removepiece(target1)
        player.rules_engine.inform_all_addpiece(target1, board.pieces[target1][1])

    def __str__(self):
        return "SwitchAction"


def generate_action():
    odds = [2,2,2,0.5, 0.5]
    sumodds = sum(odds)
    r = random.random()*sumodds
    i = 0
    o = odds[i]
    while o < r:
        i += 1
        o += odds[i]
    actions = [TerrainAction(GRASS), TerrainAction(FOREST), TerrainAction(HILLS), 
                          RemoveAction(), SwitchAction()]
    return actions[i]

class Player:
    def __init__(self, interface, id=0):
        self.interface = interface
        self.action_queue = [generate_action() for i in xrange(ACTION_QUEUE_SIZE)]
        self.interface.inform_actions(self.action_queue)
        self.id = id
        
    def perform_action(self, board):
        self.action_queue[0].perform(self, board)
        del self.action_queue[0]
        self.action_queue.append(generate_action())
        self.interface.inform_actions(self.action_queue, rotate=True)

class Board:
    def __init__(self, pieces, dimension):
        self.pieces = pieces
        self.dimension = dimension
        
    def get_neighbours(self, where):
        w, h = self.dimension
        result = []
        if where >= w:
            result.append(self.pieces[where-w])
        if where > 0 and where%w != 0:
            result.append(self.pieces[where-1])
        if where < len(self.pieces)-1 and where%w != (w-1):
            result.append(self.pieces[where+1])
        if where < len(self.pieces) - w:
            result.append(self.pieces[where+w])
        return result
        
    def get_neighbour_indices(self, where):
        w, h = self.dimension
        result = []
        if where >= w:
            result.append(where-w)
        if where > 0 and where%w != 0:
            result.append(where-1)
        if where < len(self.pieces)-1 and where%w != (w-1):
            result.append(where+1)
        if where < len(self.pieces) - w:
            result.append(where+w)
        return result
        
    def floodfill(self, where, what):
        if self.pieces[where][1] < 0 or self.pieces[where][1] != what:
            return
        
        self.pieces[where][1] += 1
        self.pieces[where][1] *= -1
        neigh = self.get_neighbour_indices(where)
        for n in neigh:
            self.floodfill(n, what)

def generate_piece():
    return [random.choice([GRASS, FOREST, HILLS, ROCKS]), -1]
        
def generate_board():
    pieces = [generate_piece() for i in xrange(BOARD_WIDTH*BOARD_HEIGHT)]
    dimension = (BOARD_WIDTH,BOARD_HEIGHT)
    return Board(pieces, dimension)
    
class RulesEngine:
    def __init__(self, players):
        self.board = generate_board()
        self.players = []
        for i, p in enumerate(players):
            self.players.append(Player(p, i))
            self.players[-1].rules_engine = self
        self.current_player = 0
        
    def game_ended(self):
        for p in self.board.pieces:
            if p[1] == -1 and p[0] != ROCKS:
                return False
        return True
        
    def calculate_points(self):
        scores = {}
        for p in self.players:
            count = 0
            for i,pc in enumerate(self.board.pieces):
                what, who = pc
                if who == p.id:
                    count += 1
                    self.board.floodfill(i, p.id)
            scores[p.interface.name] = count
        return scores

    def run(self):
        for p in self.players:
            p.interface.inform_board(self.board)
        while not self.game_ended():
            p = self.players[self.current_player]
            p.perform_action(self.board)
            self.current_player += 1
            self.current_player %= len(self.players)
        scores = self.calculate_points()
        for p in self.players:
            p.interface.inform_endgame(scores)
            
    def inform_all_addpiece(self, where, color):
        for p in self.players:
            p.interface.inform_addpiece(where, color)
            
    def inform_all_removepiece(self, where):
        for p in self.players:
            p.interface.inform_removepiece(where)
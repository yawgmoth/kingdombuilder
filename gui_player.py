import pygame
from pygame.locals import *
import os
import sys
from constants import *

DATADIR = "data"
IMAGEDIR = "img"

GRID_SIZE = 64

def load_image(name, colorkey=None):
    fullname = os.path.join(DATADIR, IMAGEDIR, name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print "Cannot load image:", name
        raise SystemExit, message
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image

class GUIPlayer:
    def __init__(self, name):
        self.name = name
        self.actions = []
        self.board = None
        pygame.init()
        self.screen = pygame.display.set_mode((600, 320))
        pygame.display.set_caption('Kingdom Builder')
        self.clock = pygame.time.Clock()
        self.tile_image = load_image('terrain1.gif')
        self.tile_map = {GRASS: Rect(0, GRID_SIZE, GRID_SIZE, GRID_SIZE),  
                         FOREST: Rect(6*GRID_SIZE, 6*GRID_SIZE, GRID_SIZE, GRID_SIZE),
                         HILLS: Rect(3*GRID_SIZE, 10*GRID_SIZE, GRID_SIZE, GRID_SIZE),
                         ROCKS: Rect(6*GRID_SIZE, 18*GRID_SIZE, GRID_SIZE, GRID_SIZE)}
                         
        self.action_map = {REMOVE_ACTION: Rect(6*GRID_SIZE, 8*GRID_SIZE, GRID_SIZE, GRID_SIZE),
                           SWITCH_ACTION: Rect(8*GRID_SIZE, 5*GRID_SIZE, GRID_SIZE, GRID_SIZE)}
        self.player_colors = {0: (255,0,0), 1: (0,0,255), 2: (0,255,255), 3: (255,0,255)}

    def draw_board(self, options=[]):
        if not self.board: 
            return
        self.clock.tick(4)
        w,h = self.board.dimension
        for y in xrange(h):
            for x in xrange(w):
                i = y*w+x
                type, id = self.board.pieces[i]
                self.screen.blit(self.tile_image, (x*GRID_SIZE,y*GRID_SIZE), self.tile_map[type])
                if id >= 0:
                    cx = x*GRID_SIZE + GRID_SIZE/2
                    cy = y*GRID_SIZE + GRID_SIZE/2
                    pygame.draw.circle(self.screen, self.player_colors[id], (cx,cy), GRID_SIZE/4)
                if i in options:
                    pygame.draw.rect(self.screen, (0,200,0), Rect(x*GRID_SIZE, y*GRID_SIZE, GRID_SIZE, GRID_SIZE), 3)
        if self.actions:
            for i, a in enumerate(self.actions):
                if a.action_type == PUT_ACTION:
                    self.screen.blit(self.tile_image, ((w+1)*GRID_SIZE, (2-i)*GRID_SIZE + (2-i)*10 + 10), self.tile_map[a.type])
                else:
                    self.screen.blit(self.tile_image, ((w+1)*GRID_SIZE, (2-i)*GRID_SIZE + (2-i)*10 + 10), self.action_map[a.action_type])
        pygame.display.flip()

    def process_events(self, options=[]):
        self.clock.tick(60)
        result = None
        w,h = self.board.dimension
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit(0)
            elif event.type == MOUSEBUTTONDOWN:
                x,y = event.pos
                if x < w*GRID_SIZE and y < h*GRID_SIZE:
                    i = (x/GRID_SIZE) + (y/GRID_SIZE)*w
                    if i in options:
                        result = i
        return result
        
    def inform_board(self, board):
        self.board = board
        self.draw_board()
        self.process_events()
        
    def inform_addpiece(self, where, color):
        self.draw_board()
        
    def inform_removepiece(self, where):
        self.draw_board()
        
    def inform_endgame(self, scores):
        sc = []
        for s in scores:
            sc.append((s, scores[s]))
        sc.sort(key=lambda x: x[1])
        for s in sc:
            print s[0], ":", s[1]
        while True:
            self.process_events()
        
    def inform_actions(self, actions, rotate=False):
        self.actions = actions
        self.draw_board()
        
    def ask_target(self, options, source):
        self.process_events()
        self.draw_board(options)
        result = None
        while result is None:
            result = self.process_events(options)
        self.draw_board()
        return result
        
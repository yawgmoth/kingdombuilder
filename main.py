import rules_engine

import console_player
import gui_player
import random_player

def main():
    players = [random_player.RandomPlayer("Player 1"), gui_player.GUIPlayer("player 2"), random_player.RandomPlayer("Player 3")]
    re = rules_engine.RulesEngine(players)
    re.run()

if __name__ == '__main__':
    main()
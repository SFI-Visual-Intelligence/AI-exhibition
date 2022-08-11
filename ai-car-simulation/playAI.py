#!/usr/bin/env python3

import os
from argparse import ArgumentParser, ArgumentTypeError

import neat

from db_handler import DataBaseHandler
from simulation import Simulation
from trainer import RacingTrainer

path = os.path.dirname(__file__)
map_path = os.path.join(path, "assets", 'maps')
maps = os.listdir(map_path)


class NeatPlayer:
    def __init__(self, players, map):
        self.players = players
        self.map = map
        self.sim = Simulation(map=map)

        self.configs = []
        self.players_ai = []

        for player in self.players:
            
            # Get configs for each player
            self.configs.append(
                neat.config.Config(
                    neat.DefaultGenome,
                    neat.DefaultReproduction,
                    neat.DefaultSpeciesSet,
                    neat.DefaultStagnation,
                    os.path.join(player.db_path, "config.txt")
                )
            )

            # Get ai for each player
            self.players_ai.append((1, player.model))

    def play_ai(self):
        """
        Method which launches the game.
        """

        # add players to game
        self.sim.add_players(self.players)

        # Set the game mode
        self.sim.set_gamemode("playing")

        # Play the game
        self.sim.run(self.players_ai, self.configs)

def name_exist(*names):
    """
    Function that checks if a name exists in the database.

    Args
    ----
    *names: str | list of str
        The name(s) to check.
    
    Returns
    -------
    str | list of str
        The name(s) if they all exist in the database.
    """

    # Get database users.
    users = db.get_users()

    # Check if user exists.
    for name in names:

        # If not, raise a ArgumentTypeError.
        if not name in users:
            raise ArgumentTypeError(f"{name} is not a registered user! Please train {name} first.")
    
    if len(names) == 1:
        return names[0]
    return names

def argparser():

    parser = ArgumentParser(
        description='Play with your trained neural network.',
        prog="playAI.py"
    )
    parser.add_argument("player", type=name_exist, help="The name of the player, must exist a database record of this player.")
    parser.add_argument("map", type=int, choices=range(1, len(maps) + 1), help="The name of the map to play on.")
    parser.add_argument("opponent", type=name_exist, nargs="+", help="Opponents to play against.")

    return parser

def show_players():
    """
    Method that shows all players in the database.
    """

    # Get database users.
    users = db.get_users()

    # Print users.
    print("\n".join(users))

if __name__ == "__main__":

    # register a database handler
    db = DataBaseHandler()

    # parse arguments
    parser = argparser()
    args = parser.parse_args()

    # Create RacingTrainer object for each player
    players = []

    for player in [args.player] + args.opponent:

        # Get texture of player
        texture = db.get_texture(player)

        # Create a RacingTrainer object
        trainer = RacingTrainer(player, texture)

        # Get path to users directory
        trainer.db_path = db.get_user_dir(player)

        # Get users model
        trainer.model = db.get_model(player)

        # Add player to list
        players.append(trainer)

    # Create a NeatPlayer object
    neat_player = NeatPlayer(players, args.map)

    # Play the ai
    neat_player.play_ai()
#!/usr/bin/env python3

"""
Train and race agains Neat AI!

This code has inspiration from YouTuber: NeuralNine which in turn was inspired by YouTuber: Cheesy AI.

This code is modified to suit quickly learning a model, then when model training is satisfied, you can play it.
"""

import math
import os
import random
import sys
from argparse import ArgumentParser

import neat
import pygame as pg

from car import Car
from db_handler import DataBaseHandler
from settings import *
from simulation import Simulation


class NeatPlayer:
    def __init__(self, config_path, map_ind):

        # set config path
        self.config_path = config_path

        self.checkpoint_dir = os.path.join(os.path.dirname(__file__), "checkpoints")

        # make config
        self.config = neat.config.Config(
            neat.DefaultGenome,
            neat.DefaultReproduction,
            neat.DefaultSpeciesSet,
            neat.DefaultStagnation,
            config_path
        )
        
        # Initialize simulation
        self.sim = Simulation(map=map_ind)

    def train_ai(self, trainer, play_until_generation:int=10) -> None:
        """
        Method to start the training of the AI. The training will last until play_until_generation.

        Args
        ----
        play_until_generation: int
            Number of generations before training is complete.
        """

        # Add trainer to simulation
        self.sim.add_trainer(trainer)
        
        # set game mode to simulation
        self.sim.set_gamemode("training")

        # set trainer attribute: is_trained = True
        trainer.train()

        # Create Population and add Reporters
        population = neat.Population(self.config)
        population.add_reporter(neat.StdOutReporter(True))
        stats = neat.StatisticsReporter()
        population.add_reporter(stats)

        # runs the population
        best_genome = population.run(self.sim.run, play_until_generation)

        return best_genome

    def play(self, players):
        """
        Method that also call Simulation.run, but only runs one for competing agains other players.

        Args
        ----
        players: List(neat.DefaultGenome)
            Pretrained genomes that compete against each other.
        """

        # make a list of all players models (NB: genomes must be stored in a list as: [(1, model1), (1, model2)])
        ai = [(1, player.model) for player in players]

        # Add players to simulation
        self.sim.add_players(players)

        self.sim.set_gamemode("playing")

        # Run the simulation
        self.sim.run(ai, self.config)

class RacingTrainer:
    
    path = os.path.join(os.path.dirname(__file__), "assets", "car-textures")

    def __init__(self, name, car_texture, model=None):
        self.__is_trained = False
        self.name = name

        self.__model = model

        if car_texture.endswith(".png"):
            car_texture = car_texture.split(".")[0]

        self.__texture = self.get_car_textures(self.path)[car_texture]

        self.__score = 0

    @property
    def score(self):
        return self.__score
    
    @score.setter
    def score(self, points):
        self.__score = points

    @property
    def model(self):
        return self.__model

    @model.setter
    def model(self, model):
        self.__model = model

    @property
    def texture(self):
        return self.__texture

    @property
    def is_trained(self):
        return self.__is_trained

    def train(self):
        self.__is_trained = True

    def get_car_textures(self, path):
        textures = dict()

        for items in os.listdir(path):

            # Set dict key = color and value = absolute path
            textures[items.split(".")[0]] = os.path.join(path, items)

        return textures

if __name__ == "__main__":

    vec = pg.math.Vector2

    # # Load Config
    path = os.path.dirname(__file__)
    config_path = os.path.join(path, "config.txt")

    colors = list(map(lambda x: x.split(".")[0], os.listdir(os.path.join(path, "assets", "car-textures"))))

    # Argument parser for cli usage (recommended).
    parser = ArgumentParser(prog="AI-NEAT-racing", description="Train an AI to race around maps")
    parser.add_argument("name", type=str, help="Name of the trainer.")
    parser.add_argument("-m", "--map", type=int, choices=[1, 2, 3, 4, 5], help="Select which map by integer (1 - 5) what map to use.")
    parser.add_argument("-t", "--train", action="store_true", help="Starts training a model to the user with specified number of generations using flag: --generations.")
    parser.add_argument("-c", "--color", type=str, choices=colors, help="Choose color for car (can only be set in training).")
    parser.add_argument("--generations", type=int, nargs="?", default=10, help="Number of generations model will train to.")
    parser.add_argument("-p", "--play", nargs="+", help="Who to play against")
    parser.add_argument("--show_opponents", action="store_true", help="Shows other possible opponents to play agains.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose mode")
    args = parser.parse_args()

    # Read inputs if verbose flag set (exits).
    if args.verbose:
        print(f"[debug] name: {args.name}, map choice: {args.map}, train: {args.train}, opponent: {args.play}")
        exit()

    # Initialize database
    db = DataBaseHandler()

    # Read other players if flag set (exits).
    if args.show_opponents:
        
        # Show opponents
        users = db.get_users()
        
        if len(users) == 0:
            print("[info]\tNo registered users.")
        else:
            print("[info]\tShowing registered users:")
            for user in users: print(f"\t{user}")

        exit()
    
    # Initialize game
    game = NeatPlayer(config_path, args.map)
    
    if args.train:
        # SET COLOR TOO HERE

        trainer = RacingTrainer(args.name, args.color)

        # Train ai
        ai = game.train_ai(trainer, args.generations)

        trainer.model = ai

        # Add model to user database folder.
        db.entry(trainer)

    elif args.play:
        
        # initialize competition by construction a RacingTrainer object for each player, 
        # starting_player = RacingTrainer(args.name)
        # starting_player.texture = db.get_texture(starting_player.name)
        # starting_player.model = db.get_model(starting_player.name)

        # Generate list of all players names starting with the main player.
        players_names = [args.name] + args.play

        players = []
        for name in players_names:
            car_texture = db.get_texture(name)
            driver = RacingTrainer(name, car_texture)
            driver.model = db.get_model(name)
            players.append(driver)
        
        # start game with players
        game.play(players)

"""
https://stackoverflow.com/questions/61365668/applying-saved-neat-python-genome-to-test-environment-after-training
"""

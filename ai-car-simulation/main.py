#!/usr/bin/env python3

"""
Train and race agains Neat AI!

This code has inspiration from YouTuber: NeuralNine which in turn was inspired by YouTuber: Cheesy AI.

This code is modified to suit quickly learning a model, then when model training is satisfied, you can play it.

THIS FILE IS DEPRECATED AS OF NOW!

"""

import math
import os
import random
import sys
from argparse import ArgumentParser

import neat
import pygame as pg

from db_handler import DataBaseHandler
from settings import *
from simulation import Simulation
from trainer import RacingTrainer



if __name__ == "__main__":

    vec = pg.math.Vector2

    # # Load Config
    path = os.path.dirname(__file__)
    config_path = os.path.join(path, "config2.txt")

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
        
        # Generate list of all players names starting with the main player.
        players_names = [args.name] + args.play

        # Make every player a racingtrainer and load their models and textures
        players = []
        for name in players_names:
            car_texture = db.get_texture(name)
            driver = RacingTrainer(name, car_texture)
            driver.model = db.get_model(name)
            players.append(driver)
        
        # start game with players
        game.play(players)
        
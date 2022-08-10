#!/usr/bin/env python3

import os
from argparse import ArgumentParser, ArgumentTypeError

import neat

from db_handler import DataBaseHandler
from simulation import Simulation
from trainer import RacingTrainer

path = os.path.dirname(__file__)
map_path = os.path.join(path, "assets", "maps")
maps = os.listdir(map_path)

def percentage_float(x):
    """
    Casts type to float and limits to 0.0 < x < 1.0.
    """
    try:
        x = float(x)
    except ValueError:
        raise ArgumentTypeError(f"{x} not a floating point literal.")

    if x < 0.0 and x > 1.0:
        raise ArgumentTypeError(f"{x} not within bounds (0.0 < x < 1.0).")
    
    return x

def limit_generations(x):
    """
    Sets the amount of generations to be a value between 0 and 20.
    """
    try:
        x = int(x)
    except ValueError:
        raise ArgumentTypeError(f"{x} not an integer.")

    if x < 0 or x > 20:
        raise ArgumentTypeError(f"{x} not within bounds (0 < x < 20).")
    return x

def censor_names(name):
    """
    Censor names that are not allowed.
    """
     
    NOT_ALLOWED_NAMES = ["admin"] # Feel free to add more names that should not be allowed.

    # Can also modify to look for parts of the name not allowed.
    if name in NOT_ALLOWED_NAMES:
        raise ValueError(f"{name} is not allowed.")

    return name

def argparser():
    valuenote = "Value must be 0.0 < x < 1.0."
    
    # Get saved colors from ./assets/car-textures
    colors = list(map(lambda x: x.split(".")[0], os.listdir(os.path.join(path, "assets", "car-textures"))))

    parser = ArgumentParser(prog="AI-NEAT-trainig", description="Train a neural network to drive a racing car.")
    parser.add_argument("trainer", type=censor_names, help="Select your trainer name")
    parser.add_argument("color", type=str, choices=colors, help="Select your car color")
    parser.add_argument("map", type=int, choices=range(1, len(maps) + 1), help=f"Select which map by integer (1 - {len(maps)}) to train on.")
    parser.add_argument("generations", type=limit_generations, nargs="?", default=10, help="Number of generations model will train to.")
    parser.add_argument("weight_mutate_power", type=percentage_float, nargs="?", default=0.5, help=f"Set the weight_mutate_power parameter in neat config. {valuenote}")
    parser.add_argument("weight_mutate_rate", type=percentage_float, nargs="?", default=0.8, help=f"Set the weight_mutate_rate parameter in neat config. {valuenote}")
    parser.add_argument("weight_replace_rate", type=percentage_float, nargs="?", default=0.1, help=f"Set the weight_replace_rate parameter in neat config. {valuenote}")

    return parser

class NeatTrainer:
    def __init__(self, config_path, map):
        
        # Set config path
        self.config_path = config_path

        # Make config
        self.config = neat.config.Config(
            neat.DefaultGenome, 
            neat.DefaultReproduction, 
            neat.DefaultSpeciesSet, 
            neat.DefaultStagnation, 
            self.config_path
        )

        # Initialize simulation

        self.sim = Simulation(map=map)

    def train_ai(self, trainer, train_until_generation):
        """
        Method for training the ai, the training will last until train_until_generation.

        Args
        ----
        trainer: trainer.RacingTrainer | obj
            The trainer object to be used.
        train_until_generation: int
            The generation to train until.
        """

        # Set trainer
        self.sim.add_trainer(trainer)
        self.sim.set_gamemode("training")
        trainer.train()

        # Make neat Population and add Reporters
        population = neat.Population(self.config)
        population.add_reporter(neat.StdOutReporter(True))
        stats = neat.StatisticsReporter()
        population.add_reporter(stats)
        
        # Run simulation
        best_genome = population.run(self.sim.run, train_until_generation)

        return best_genome

if __name__ == "__main__":
    parser = argparser()

    args = parser.parse_args()
    
    # Setup a database for the trainer
    db = DataBaseHandler(prefix="DEBUG2_")
    
    # Create a RacingTrainer object
    trainer = RacingTrainer(
        name=args.trainer,
        car_texture=args.color,
        weight_mutate_power=args.weight_mutate_power,
        weight_mutate_rate=args.weight_mutate_rate,
        weight_replace_rate=args.weight_replace_rate,
    )

    # Save a config and color for the trainer in the database.
    db.entry(trainer)

    # Initialize training process object
    game = NeatTrainer(config_path=os.path.join(trainer.db_path, "config.txt"), map=args.map)

    # Train the ai
    ai = game.train_ai(trainer, args.generations)

    # Assign ai to trainer
    trainer.model = ai

    # Save the ai to the database
    db.add_user_model(trainer.name, trainer.model)
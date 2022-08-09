#!/usr/bin/env python3

from argparse import ArgumentParser, ArgumentTypeError
import os
from main import RacingTrainer
import shutil
from db_handler import DataBaseHandler

path = os.path.dirname(__file__)
map_path = os.path.join(path, "assets/maps")
maps = os.listdir(map_path)

def restricted_float(x):
    try:
        x = float(x)
    except ValueError:
        raise ArgumentTypeError(f"{x} not a floating point literal.")

    if x < 0.0 and x > 1.0:
        raise ArgumentTypeError(f"{x} not within bounds (0.0 < x < 1.0).")
    
    return x

def argparser():
    valuenote = "Value must be 0.0 < x < 1.0."

    parser = ArgumentParser(prog="AI-NEAT-trainig", description="Train a neural network to drive a racing car.")
    parser.add_argument("trainer", type=str, help="Select your trainer name")
    parser.add_argument("map", type=int, choices=range(1, len(maps) + 1), help=f"Select which map by integer (1 - {len(maps)}) to train on.")
    parser.add_argument("generations", type=int, nargs="?", default=10, help="Number of generations model will train to.")
    parser.add_argument("weight_mutate_power", type=restricted_float, nargs="?", default=0.5, help=f"Set the weight_mutate_power parameter in neat config. {valuenote}")
    parser.add_argument("weight_mutate_rate", type=restricted_float, nargs="?", default=0.8, help=f"Set the weight_mutate_rate parameter in neat config. {valuenote}")
    parser.add_argument("weight_replace_rate", type=restricted_float, nargs="?", default=0.1, help=f"Set the weight_replace_rate parameter in neat config. {valuenote}")

    return parser

def create_trainer(
        name, 
        map, 
        generations, 
        weight_mutate_power, 
        weight_mutate_rate, 
        weight_replace_rate
    ):

    # Create the users folder in the databse
    db.add_user(name)

    # Construct a custom config to the user.
    db.add_config(
        name, 
        weight_mutate_power=weight_mutate_power, 
        weight_mutate_rate=weight_mutate_rate, 
        weight_replace_rate=weight_replace_rate
    )


if __name__ == "__main__":
    parser = argparser()

    args = parser.parse_args()
    
    db = DataBaseHandler()
    
    create_trainer(
        args.trainer, 
        args.map, 
        args.generations, 
        args.weight_mutate_power,
        args.weight_mutate_rate,
        args.weight_replace_rate
    )

    # Now need to implement a call to main.py to start training. or ignore main.py and start training from here...
#!/usr/bin/env python3

"""
Train and race agains Neat AI!

This code has inspiration from YouTuber: NeuralNine which in turn was inspired by YouTuber: Cheesy AI.

This code is modified to suit quickly learning a model, then when model training is satisfied, you can play it.
"""

import math
import random
import sys
import os

import neat
import pygame as pg
from argparse import ArgumentParser

from settings import *
from db_handler import DataBaseHandler

class Car:

    def __init__(self, owner):
        # Load Car Sprite and Rotate
        self.owner = owner
        self.sprite = pg.image.load(self.owner.texture).convert_alpha() # Convert Speeds Up A Lot
        self.sprite = pg.transform.scale(self.sprite, (CAR_SIZE_X, CAR_SIZE_Y))
        self.rotated_sprite = self.sprite 

        self.position = [830, 920] # Starting Position
        self.angle = 0
        self.speed = 0

        self.speed_set = False # Flag For Default Speed Later on

        self.center = [self.position[0] + CAR_SIZE_X / 2, self.position[1] + CAR_SIZE_Y / 2] # Calculate Center

        self.radars = [] # List For Sensors / Radars
        self.drawing_radars = [] # Radars To Be Drawn

        self.alive = True # Boolean To Check If Car is Crashed

        self.distance = 0 # Distance Driven
        self.time = 0 # Time Passed

    def draw(self, screen):
        screen.blit(self.rotated_sprite, self.position) # Draw Sprite
        self.draw_radar(screen) #OPTIONAL FOR SENSORS
        self.draw_owner_name(screen)

    def draw_radar(self, screen):
        # Optionally Draw All Sensors / Radars
        for radar in self.radars:
            position = radar[0]
            pg.draw.line(screen, (0, 255, 0), self.center, position, 1)
            pg.draw.circle(screen, (0, 255, 0), position, 5)

    def draw_owner_name(self, screen):
        font = pg.font.SysFont("Arial", 36)
        text = font.render(self.owner.name, True, (0,255,0))
        screen.blit(text, self.center + [100, -20])

    def check_collision(self, game_map):
        self.alive = True
        for point in self.corners:
            # If Any Corner Touches Border Color -> Crash
            # Assumes Rectangle
            if game_map.get_at((int(point[0]), int(point[1]))) == BORDER_COLOR:
                self.alive = False
                break

    def check_radar(self, degree, game_map):
        length = 0
        x = int(self.center[0] + math.cos(math.radians(360 - (self.angle + degree))) * length)
        y = int(self.center[1] + math.sin(math.radians(360 - (self.angle + degree))) * length)

        # While We Don't Hit BORDER_COLOR AND length < 300 (just a max) -> go further and further
        while not game_map.get_at((x, y)) == BORDER_COLOR and length < 300:
            length = length + 1
            x = int(self.center[0] + math.cos(math.radians(360 - (self.angle + degree))) * length)
            y = int(self.center[1] + math.sin(math.radians(360 - (self.angle + degree))) * length)

        # Calculate Distance To Border And Append To Radars List
        dist = int(math.sqrt(math.pow(x - self.center[0], 2) + math.pow(y - self.center[1], 2)))
        self.radars.append([(x, y), dist])
    
    def update(self, game_map):
        # Set The Speed To 20 For The First Time
        # Only When Having 4 Output Nodes With Speed Up and Down
        if not self.speed_set:
            self.speed = 20
            self.speed_set = True

        # Get Rotated Sprite And Move Into The Right X-Direction
        # Don't Let The Car Go Closer Than 20px To The Edge
        self.rotated_sprite = self.rotate_center(self.sprite, self.angle)
        self.position[0] += math.cos(math.radians(360 - self.angle)) * self.speed
        self.position[0] = max(self.position[0], 20)
        self.position[0] = min(self.position[0], WIDTH - 120)

        # Increase Distance and Time
        self.distance += self.speed
        self.time += 1
        
        # Same For Y-Position
        self.position[1] += math.sin(math.radians(360 - self.angle)) * self.speed
        self.position[1] = max(self.position[1], 20)
        self.position[1] = min(self.position[1], WIDTH - 120)

        # Calculate New Center
        self.center = [int(self.position[0]) + CAR_SIZE_X / 2, int(self.position[1]) + CAR_SIZE_Y / 2]

        # Calculate Four Corners
        # Length Is Half The Side
        length = 0.5 * CAR_SIZE_X
        left_top = [self.center[0] + math.cos(math.radians(360 - (self.angle + 30))) * length, self.center[1] + math.sin(math.radians(360 - (self.angle + 30))) * length]
        right_top = [self.center[0] + math.cos(math.radians(360 - (self.angle + 150))) * length, self.center[1] + math.sin(math.radians(360 - (self.angle + 150))) * length]
        left_bottom = [self.center[0] + math.cos(math.radians(360 - (self.angle + 210))) * length, self.center[1] + math.sin(math.radians(360 - (self.angle + 210))) * length]
        right_bottom = [self.center[0] + math.cos(math.radians(360 - (self.angle + 330))) * length, self.center[1] + math.sin(math.radians(360 - (self.angle + 330))) * length]
        self.corners = [left_top, right_top, left_bottom, right_bottom]

        # Check Collisions And Clear Radars
        self.check_collision(game_map)
        self.radars.clear()

        # From -90 To 120 With Step-Size 45 Check Radar
        for d in range(-90, 120, 45):
            self.check_radar(d, game_map)

    def get_data(self):
        # Get Distances To Border
        radars = self.radars
        return_values = [0, 0, 0, 0, 0]
        for i, radar in enumerate(radars):
            return_values[i] = int(radar[1] / 30)

        return return_values

    def is_alive(self):
        # Basic Alive Function
        return self.alive

    def get_reward(self):
        # Calculate Reward (Maybe Change?)
        # return self.distance / 50.0
        return self.distance / (CAR_SIZE_X / 2)

    def rotate_center(self, image, angle):
        # Rotate The Rectangle
        rectangle = image.get_rect()
        rotated_image = pg.transform.rotate(image, angle)
        rotated_rectangle = rectangle.copy()
        rotated_rectangle.center = rotated_image.get_rect().center
        rotated_image = rotated_image.subsurface(rotated_rectangle).copy()
        return rotated_image

class Simulation:
    def __init__(self, train_map):

        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT), pg.FULLSCREEN)

        self.current_generation = 0

        path = os.path.dirname(__file__)
        assets_path = os.path.join(path, "assets")
        map_path = os.path.join(assets_path, "maps")

        # Get maps paths
        self.maps = [os.path.join(map_path, map_file) for map_file in sorted(os.listdir(map_path))]

        self.map = self.maps[train_map - 1]

        self.trainer = None

        self.players = None

    def add_trainer(self, trainer):
        self.trainer = trainer

    def add_players(self, players):
        self.players = players

    def load(self, map):
        self.generation_font = pg.font.SysFont("Arial", 30)
        self.alive_font = pg.font.SysFont("Arial", 20)
        game_map = pg.image.load(map).convert_alpha()
        return game_map

    def init_model(self, genomes, config):
        nets = []
        cars = []

        # If players is specified, cars are made as this and will not train up new models.
        if not self.players is None:
            cars = [Car(player) for player in self.players]

        for i, g in genomes:
            net = neat.nn.FeedForwardNetwork.create(g, config)
            nets.append(net)
            g.fitness = 0

            # if a trainer is specified cars are generated and trained.
            if not self.trainer is None:
                if self.trainer.is_trained and self.players is None:
                    cars.append(Car(self.trainer))
                
        return nets, cars

    def run(self, genomes, config):
        """ Make the game able to play in same window """
        

        nets, cars = self.init_model(genomes, config)

        clock = pg.time.Clock()
        self.t = 0
        game_map = self.load(self.map)

        while True:

            # Handle events
            self.events()

            self.still_alive = self.update(nets, cars, genomes, game_map)

            if self.still_alive == 0 or self.t > 15:
                break
            
            self.draw(game_map, cars)
            self.display_text()

            pg.display.flip()
            self.t += clock.tick(60) / 1000

        self.current_generation += 1

    def draw(self, map, cars):
        self.screen.blit(map, (0,0))

        for car in cars:
            if car.is_alive():
                car.draw(self.screen)


    def display_text(self):
        text = self.generation_font.render(f"Generation: {self.current_generation}", True, (0,0,0))
        text_rect = text.get_rect(center = vec(900, 450))
        self.screen.blit(text, text_rect)

        text = self.alive_font.render(f"Still Alive: {self.still_alive}", True, (0,0,0))
        text_rect = text.get_rect(center = vec(900, 490))
        self.screen.blit(text, text_rect)


    def update(self, nets, cars, genomes, game_map):
        
        # For each car get its action
        for i, car in enumerate(cars):
            output = nets[i].activate(car.get_data())
            choice = output.index(max(output))

            # Left
            if choice == 0:
                car.angle += 10

            # Right
            elif choice == 1:
                car.angle -= 10

            # Slow Down
            elif choice == 2:
                if car.speed - 2 >= 12:
                    car.speed -= 2

            # Speed up
            else:
                car.speed += 2

        # Check if car is still alive
        # if yes, increase fitness, break loop if not

        still_alive = 0
        for i, car in enumerate(cars):
            if car.is_alive():
                still_alive += 1
                car.update(game_map)
                genomes[i][1].fitness += car.get_reward()

        return still_alive
        
    def events(self):
        # Exit on Quit Event
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit(0)

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    sys.exit(0)

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
        self.sim = Simulation(train_map=map_ind)

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
        Method that
        """

        # make a list of all players models (NB: genomes must be stored in a list as: [(1, model1), (1, model2)])
        ai = [(1, player.model) for player in players]

        # Add players to simulation
        self.sim.add_players(players)

        # Run the simulation
        self.sim.run(ai, self.config)

class RacingTrainer:
    
    path = os.path.join(os.path.dirname(__file__), "assets", "car-textures")

    def __init__(self, name, car_texture=None, model=None):
        self.__is_trained = False
        self.name = name

        self.__model = model

        if car_texture is None:
            self.texture = car_texture   
            return
        
        self.texture = self.get_car_textures(self.path)[car_texture]


    @property
    def model(self):
        return self.__model

    @model.setter
    def model(self, model):
        self.__model = model

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

    # Argument parser for cli usage (recommended).
    parser = ArgumentParser(prog="AI-NEAT-racing", description="Train an AI to race around maps")
    parser.add_argument("name", type=str, help="Name of the trainer.")
    parser.add_argument("-m", "--map", type=int, choices=[1, 2, 3, 4, 5], help="Select which map by integer (1 - 5) what map to use.")
    parser.add_argument("-t", "--train", action="store_true", help="Starts training a model to the user with specified number of generations using flag: --generations.")
    parser.add_argument("-c", "--color", type=str, choices=["blue", "red"], help="Choose color for car (can only be set in training).")
    parser.add_argument("--generations", type=int, nargs="?", const=10, help="Number of generations model will train to.")
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

        # Create dict with players name as key and model as value

        starting_player = RacingTrainer(args.name)
        starting_player.texture = db.get_texture(starting_player.name)
        starting_player.model = db.get_model(starting_player.name)

        # Generate list of all players names starting with the main player.
        players_names = [args.name] + args.play

        players = []
        for name in players_names:
            driver = RacingTrainer(name)
            driver.texture = db.get_texture(name)
            driver.model = db.get_model(name)
            players.append(driver)
        

        # players = {args.name: db.get_model(args.name)}

        # # Do the same for the specified opponents.
        # for opponent in args.play:
        #     players[opponent] = [db.get_model(opponent), random.choice(["red", "blue"])]

        # start game with players
        game.play(players)

"""
https://stackoverflow.com/questions/61365668/applying-saved-neat-python-genome-to-test-environment-after-training
"""
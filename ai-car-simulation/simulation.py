import os
import sys

import neat
import pygame as pg

from car import Car
from settings import *

vec = pg.math.Vector2

class Simulation:
    def __init__(self, train_map):

        # init pygame and screen
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT), pg.FULLSCREEN)

        # keep track of current generation
        self.current_generation = 0

        # set path
        path = os.path.dirname(__file__)
        assets_path = os.path.join(path, "assets")
        map_path = os.path.join(assets_path, "maps")

        # Get maps paths
        self.maps = [os.path.join(map_path, map_file) for map_file in sorted(os.listdir(map_path))]

        # select which map to use.
        self.map = self.maps[train_map - 1]

        # sets trainer if game-mode is training (1 object)
        self.trainer = None

        # sets players if game-mode is playing (multiple objects)
        self.players = None

    def add_trainer(self, trainer):
        self.trainer = trainer

    def add_players(self, players):
        self.players = players

    def load(self, map):
        """
        Load fonts and map.

        Args
        ----
        map: str | path-like
            The path to the map to be used.
        
        Returns
        ------
        game_map: pygame.image
            Loaded image from given path.
        """

        # Load fonts
        self.generation_font = pg.font.SysFont("Arial", 30)
        self.alive_font = pg.font.SysFont("Arial", 20)

        # Load game map, use convert_alpha as it speeds up computations and displaying of the image.
        game_map = pg.image.load(map).convert_alpha()
        return game_map

    def init_model(self, genomes, config):
        """
        Initializes the Neat-model.

        Note that when neat.Population.run is called, it provides theese arguments.

        Args
        ----
        genomes: List(neat.DefaultGenome)
            Genomes to be trained or used to play.
        config: neat.DefaultGenomeConfig
            Config that specifies neural networks parameters.
        """
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
        """ Runs the simulation and contains the main loop of the game.
        
        Note that when neat.Population.run is called, it provides theese arguments.

        Args
        ----
        genomes: List(neat.DefaultGenome)
            Genomes to be trained or used to play.
        config: neat.DefaultGenomeConfig
            Config that specifies neural networks parameters.
        """
        
        # Initialize model
        nets, cars = self.init_model(genomes, config)

        # make a clock object for time-keeping
        clock = pg.time.Clock()
        self.t = 0

        # Load map and fonts.
        game_map = self.load(self.map)

        # Start game-loop
        while True:

            # Handle events
            self.events()

            # update networks, cars and genomes
            self.still_alive = self.update(nets, cars, genomes, game_map)

            # check if either no genomes still alive or maximum allowed play-time is exceeded.
            if self.still_alive == 0 or self.t > MAX_GENERATION_TIME:
                break
            
            # draw map, cars and show text.
            self.draw(game_map, cars)
            self.display_text_training()
            
            # flip display and tick clock
            pg.display.flip()
            self.t += clock.tick(60) / 1000

        # iter generation
        self.current_generation += 1

    def draw(self, map, cars):
        """
        Draw map and cars

        Args
        ----
        map: pygame.image
            Map image to be displayed
        cars: list
            list of car.Car to display
        """

        self.screen.blit(map, (0,0))

        for car in cars:
            if car.is_alive():
                car.draw(self.screen)


    def display_text_training(self):
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

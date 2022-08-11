import csv
import os
import sys

import neat
import pygame as pg

from car import Car
from settings import *
from leaderboard import LeaderboardHandler

vec = pg.math.Vector2

class Simulation:
    def __init__(self, map):

        # init pygame and screen
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT), pg.FULLSCREEN)

        # keep track of current generation
        self.current_generation = 0

        # set path
        path = os.path.dirname(__file__)
        self.assets_path = os.path.join(path, "assets")
        map_path = os.path.join(self.assets_path, "maps")

        # Get maps paths
        self.maps = [os.path.join(map_path, map_file) for map_file in sorted(os.listdir(map_path))]

        # select which map to use.
        self.map = self.maps[map - 1]

        # Make a leaderboard object.
        self.leaderboard = LeaderboardHandler(map)

        # sets trainer if game-mode is training (1 object)
        self.trainer = None

        # sets players if game-mode is playing (multiple objects)
        self.players = None

    def set_gamemode(self, mode):

        # sets gamemode
        self.mode = mode

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
        self.header_font = pg.font.SysFont("Arial", 30)
        self.subheader_font = pg.font.SysFont("Arial", 20)

        self.additional_fonts = []
        if self.mode == "playing":
            for i, _ in enumerate(self.players):
                self.additional_fonts.append(pg.font.SysFont("Arial", 25))


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

        if self.mode is "playing":
            cars = [Car(self, player) for player in self.players]

            for (i, genome), config in zip(genomes, config):
            # for genome in genomes:
                net = neat.nn.FeedForwardNetwork.create(genome, config)
                nets.append(net)
                genome.fitness = 0

            self.time_left = MAX_PLAYTIME
            self.maxtime = MAX_PLAYTIME

            return nets, cars

        # If however the mode is training, cars are created for the trainer, one per genome and then trained.
        for i, g in genomes:
            net = neat.nn.FeedForwardNetwork.create(g, config)
            nets.append(net)
            g.fitness = 0

            cars.append(Car(self, self.trainer))

        self.time_left = MAX_GENERATION_TIME
        self.maxtime = MAX_GENERATION_TIME
        

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
            if self.still_alive == 0 or self.t > self.maxtime:
                if self.mode == "training":
                    break
                self.game_over()
            
            # draw map, cars and show text.
            self.draw(game_map, cars)

            if self.mode == "training":
                self.display_text_training()
            else:
                self.display_text_playing()
            
            # flip display and tick clock
            pg.display.flip()
            self.t += clock.tick(60) / 1000

            # Calculate time left
            self.time_left = self.maxtime - self.t

        # iter generation
        self.current_generation += 1

    def game_over(self):
        """
        Should trigger when game mode is playing and either time runs out or all cars crashes.

        This function stores the score of each player to a global leaderboards text file.
        """
        
        # Create leaderboard handler object.
        self.leaderboard.add_score(self.players)

        sys.exit(0)

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
        text = self.header_font.render(f"Generation: {self.current_generation}", True, (0,0,0))
        text_rect = text.get_rect(center = vec(900, 450))
        self.screen.blit(text, text_rect)

        text = self.subheader_font.render(f"Still Alive: {self.still_alive}", True, (0,0,0))
        text_rect = text.get_rect(center = vec(900, 490))
        self.screen.blit(text, text_rect)

    def display_text_playing(self):
        # text = self.header_font.render(f"Players: {[player.name for player in self.players]}", True, (0,0,0))
        texty = 450
        text = self.header_font.render(f"Time left: {int(self.time_left)}", True, (0,0,0))
        text_rect = text.get_rect(center = vec(920, texty))
        self.screen.blit(text, text_rect)
        
        texty += 40

        text = self.subheader_font.render("Scores:", True, (0,0,0))
        text_rect = text.get_rect(center=vec(920, texty))
        self.screen.blit(text, text_rect)

        texty += 40

        # For each player display their score.
        for i, font in enumerate(self.additional_fonts):
            text = font.render(f"{self.players[i].name} - {self.players[i].score}", True, (0,0,0))
            text_rect = text.get_rect(center=vec(920, texty))
            self.screen.blit(text, text_rect)
            texty += 40

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
            
            if not car.is_alive():
                continue 

            still_alive += 1
            car.update(game_map)

            reward = car.get_reward()

            genomes[i][1].fitness += reward

            if self.mode == "playing":
                self.players[i].score += reward // 100
            

        return still_alive
        
    def events(self):
        # Exit on Quit Event
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit(0)

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    sys.exit(0)

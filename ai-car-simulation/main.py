"""
Train and race agains Neat AI!

This code has inspiration from YouTuber: NeuralNine which in turn was inspired by YouTuber: Cheesy AI.

This code is modified to suit quickly learning a model, then when model training is satisfied, you can play it.
"""

import math
import random
import sys
import os
import pickle

import neat
import pygame as pg

from settings import *

vec = pg.math.Vector2

class Car:

    def __init__(self):
        # Load Car Sprite and Rotate
        self.sprite = pg.image.load('car.png').convert_alpha() # Convert Speeds Up A Lot
        self.sprite = pg.transform.scale(self.sprite, (CAR_SIZE_X, CAR_SIZE_Y))
        self.rotated_sprite = self.sprite 

        # self.position = [690, 740] # Starting Position
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

    def draw_radar(self, screen):
        # Optionally Draw All Sensors / Radars
        for radar in self.radars:
            position = radar[0]
            pg.draw.line(screen, (0, 255, 0), self.center, position, 1)
            pg.draw.circle(screen, (0, 255, 0), position, 5)

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
    def __init__(self):

        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT), pg.FULLSCREEN)

        self.current_generation = 0

    def load(self, map):
        self.generation_font = pg.font.SysFont("Arial", 30)
        self.alive_font = pg.font.SysFont("Arial", 20)
        game_map = pg.image.load(map).convert_alpha()
        return game_map


    def init_model(self, genomes, config):
        nets = []
        cars = []

        if isinstance(genomes, list):
            for i, g in genomes:
                net = neat.nn.FeedForwardNetwork.create(g, config)
                nets.append(net)
                g.fitness = 0

                cars.append(Car())
        else:
            net = neat.nn.FeedForwardNetwork.create(genomes, config)
            nets.append(net)
            genomes.fitness = 0

            cars.append(Car())

        return nets, cars

    def run(self, genomes, config):
        """ Make the game able to play in same window """
        
        nets, cars = self.init_model(genomes, config)

        clock = pg.time.Clock()
        self.t = 0
        game_map = self.load("map2.png")

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
    def __init__(self, config_path):

        # set config path
        self.config_path = config_path

        # make config
        self.config = neat.config.Config(
            neat.DefaultGenome,
            neat.DefaultReproduction,
            neat.DefaultSpeciesSet,
            neat.DefaultStagnation,
            config_path
        )
        
        # Initialize simulation
        self.sim = Simulation()

    def train_ai(self, play_until_generation:int=10) -> None:
        """
        Method to start the training of the AI. The training will last until play_until_generation.

        Args
        ----
        play_until_generation: int
            Number of generations before training is complete.
        """

        # Create Population and add Reporters
        population = neat.Population(self.config)
        population.add_reporter(neat.StdOutReporter(True))
        stats = neat.StatisticsReporter()
        population.add_reporter(stats)


        best_genome = population.run(self.sim.run, play_until_generation)

        return best_genome

    def play(self, ai):
        """
        Method that
        """

        self.sim.run(ai, self.config)

    @staticmethod
    def save_genome(genome, filepath):
        with open(filepath, "wb") as f:
            pickle.dump(genome, f)

    @staticmethod
    def load_genome(filepath):
        """
        Load a locally saved genome.

        Args
        ----
        filepath : path-like | str
            path to file containing genome bytes.
        
        Returns
        -------
        genome : 
        """
        with open(filepath, "rb") as f:
            genome = pickle.load(filepath)
        
        genome = [(1, genome)]
        return genome


if __name__ == "__main__":

    # Load Config
    path = os.path.dirname(__file__)
    config_path = os.path.join(path, "config.txt")

    game = NeatPlayer(config_path)
    ai = game.train_ai(7)

    modelname = "neat-trained-model.pkl"

    game.save_genome(ai, modelname)

    ai = game.load_genome(modelname)

    game.play(ai)

"""
https://stackoverflow.com/questions/61365668/applying-saved-neat-python-genome-to-test-environment-after-training
"""
import os


class RacingTrainer:
    
    path = os.path.join(os.path.dirname(__file__), "assets", "car-textures")

    def __init__(self, name, car_texture, **config_params):
        self.__is_trained = False
        self.name = name
        self.config_params = config_params

        self.model = None
        self.db_path = None

        if car_texture.endswith(".png"):
            car_texture = car_texture.split(".")[0]

        self.__texture = self.get_car_textures(self.path)[car_texture]

        self.score = 0

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
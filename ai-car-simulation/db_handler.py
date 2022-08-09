import pickle
from os import listdir, getcwd, chdir, makedirs, rmdir, remove
from os.path import join, isdir, abspath
from changedir import Changedir

class DataBaseHandler:
    """
    Handle databases.

    Attributes
    ----------
    path: str
        path to database. Optional, default "database"
    
    Methods
    -------
    get_model(user) -> model:
        Get the model of a user
    get_users() -> list:
        List of users stored.
    entry(user, model):
        Add a new database entry to store the model to a user.
    """
    def __init__(self, path: str = "database", prefix: str = None):
        """
        Args
        ----
        path: str
            Path to database. Optional, default "database"
        prefix: str
            prefix for database name. Optional, default None
        """

        self.path = str(path)
        
        # If optional prefix specified, add it.
        if not prefix is None:
            self.path = str(prefix) + str(path)

        if not isdir(self.path):
            makedirs(self.path)

        self.default_config_dir = abspath(join(self.path, "..", "assets"))

    def DEBUG_remove_database(self):
        """
        Remove the whole database.
        """
        # Ask user if this is what they want
        sel = input("\n[interactive]\tAre you sure you want to delete the whole database? (y/n)\t")

        # Exit on no
        if sel == "n":
            return
        
        users = listdir(self.path)

        for user in users:
            self.DEBUG_remove_user(join(self.path, user))

    def DEBUG_remove_user(self, user:str):
        """
        Remove user from database.

        Args
        ----
        user_path: str | path_like
            Path to user directory
        """

        user_path = join(self.path, user)

        # find all files in directory
        files = listdir(user_path)

        if len(files) != 0:
            for file in files:
                remove(join(user_path, file))

        # Remove empty directory
        rmdir(user_path)
        print(f"[debug]\t{user_path} removed.")

    def add_user(self, name:str):
        """
        Add a directory for a user.

        Args
        ----
        name: str
            Name of user to be added.
        """
        userpath = join(self.path, str(name))
        try:
            makedirs(userpath)
            print(f"[info]\t{userpath} created.")
        except FileExistsError as e:
            print(f"[warning]\t{userpath} already exist.")

    def _add_user_model(self, user):
        """
        Add a model entry to a user directory.

        Args
        ----
        user: str
            Name of user
        model: obj
            Object to be stored in database.
        """
        user_model = join(self.path, user.name, "model.pkl")

        try:
            with open(user_model, "wb") as f:
                pickle.dump(user.model, f)
                print(f"[info]\t{user_model} created.")

        except FileExistsError as e:
            raise e

    def _add_user_texture(self, owner):
        """
        Store owners color

        Args
        ----
        owner: RacingTrainer obj
            Object with name and texture attribute.
        """

        user_dir = join(self.path, owner.name, "texture.txt")
        
        # get only the color, not the full path
        texture_to_save = owner.texture.split("/")[-1]

        # Remove .png
        texture_to_save = texture_to_save.split(".")[0]
        try:
            with open(user_dir, "w") as f:
                f.write(texture_to_save)
        except FileExistsError as e:
            raise e

    def add_config(self, user, **configparams):
        """
        Store user modified config in database.

        Args
        ----
        user: str
            User to store new config to.
        configparams: kwargs (dict)
            Parameters from config file to modify. In principle any parameter can be changed, althoug only some have been tested:
                weight_mutate_power,
                weight_mutate_rate,
                weight_replace_rate.
        """
        
        # Use a context manager to keep track of source and dist.
        with Changedir(self.default_config_dir, self.path) as changer:

            defaultconfig = join(changer.newdir, "defaultconfig.txt")
            userconfig = join(changer.olddir, user, "config.txt")
            
            # open the default config and temporarily store its content
            with open(defaultconfig, "r") as rf:
                data = rf.readlines()
            
            # iterate over content
            for i, line in enumerate(data):

                # See if parameter has a match in the configuration parameters
                for parameter in configparams:

                    if parameter in line:
                        
                        # split wanted line at equals mark
                        new_line = data[i].split("= ")

                        # Change line to new value
                        changed_line = f"{configparams[parameter]}\n"

                        # Concatenate with rest of line
                        set_line = new_line[0] + "= " + changed_line

                        # set the whole line to the modified line
                        data[i] = set_line
            
            # Write modified config to user
            with open(userconfig, "w+") as wf:
                wf.writelines(data)

    def get_model(self, user):
        """
        Get the model of a user.

        Args
        ----
        user: str
            Name of user.
        
        Returns
        -------
        model: obj
            Stored model object from users file.
        """
        
        # path to users model
        user_model = join(self.path, user, "model.pkl")

        # Try and catch error if user does not exist.
        try:
            with open(user_model, "rb") as f:
                model = pickle.load(f)
            
            return model
        
        except FileNotFoundError as e:
            print(f"[Error]\t{e}")

    def get_texture(self, user):
        """
        Get the texture of a user.

        Args
        ----
        user: str
            Name of user.

        Returns
        -------
        texture: str
            Name of texture.
        """

        user_texture = join(self.path, user, "texture.txt")

        try:
            with open(user_texture, "r") as f:
                texture = f.read()
        except FileNotFoundError as e:
            print(f"[Error]\t{e}")

        return texture

    def get_users(self):
        """
        Get all users registered in the database.

        Returns
        -------
        users: list
            List of registered users.
        """

        return listdir(self.path)

    def entry(self, owner):
        """
        Add a new entry to the database.

        Args
        ----
        user: str
            Name of user.
        model: obj
            Object to be stored in database.
        """

        self.add_user(owner.name)
        self._add_user_texture(owner)
        self._add_user_model(owner)

if __name__ == "__main__":
    class TestClass:
        def __init__(self, name, texture, model):
            self.name = name
            self.texture = texture
            self.model = model

    a, b = "1", "2"
    p1 = TestClass("user1", "blue", a)
    p2 = TestClass("user2", "red", b)


    db = DataBaseHandler(prefix="DEBUG_")

    db.entry(p1)
    db.entry(p2)

    db.add_config("user1", weight_mutate_power=0.2, weight_mutate_rate=0.5, weight_replace_rate=0.8)

    try:
        for username in db.get_users(): assert username in [p1.name, p2.name]
        assert db.get_model(p1.name) == "1"
        assert db.get_texture(p1.name) == "blue"
    except AssertionError as e:
        print(f"A test failed: {e}")
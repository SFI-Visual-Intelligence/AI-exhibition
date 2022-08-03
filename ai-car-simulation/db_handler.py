import pickle
from os import listdir, getcwd, chdir, makedirs, rmdir, remove
from os.path import join, isdir

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

    def _add_user(self, name:str):
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

    def _add_model_to_user(self, user, model):
        """
        Add a model entry to a user directory.

        Args
        ----
        user: str
            Name of user
        model: obj
            Object to be stored in database.
        """
        user_model = join(self.path, user, "model.pkl")

        try:
            with open(user_model, "wb") as f:
                pickle.dump(model, f)
                print(f"[info]\t{user_model} created.")

        except FileExistsError as e:
            raise e

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


    def get_users(self):
        """
        Get all users registered in the database.

        Returns
        -------
        users: list
            List of registered users.
        """

        return listdir(self.path)

    def entry(self, user, model):
        """
        Add a new entry to the database.

        Args
        ----
        user: str
            Name of user.
        model: obj
            Object to be stored in database.
        """

        self._add_user(user)
        self._add_model_to_user(user, model)

if __name__ == "__main__":
    a, b = "1", "2"
    h1 = DataBaseHandler(prefix="DEBUG_")
    h1.entry("DEBUG_user1", a)
    h1.entry("DEBUG_user2", b)
    assert h1.get_model("DEBUG_user1") == "1"
    assert h1.get_users() == ["DEBUG_user1", "DEBUG_user2"]
    h1.get_model("DEBUG_user3") # Does not exist entry for user3 will therefore crash
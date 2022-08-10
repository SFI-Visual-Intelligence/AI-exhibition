import os
import pandas

class LeaderboardHandler:
    """
    Object for keeping track of a running leaderboard.

    Stores scores for each person on a per map basis in a csv file for each map.

    The file is named leaderboard-map<map>.csv and is stored in the assets folder.
    """

    # Class attribute
    base_path = os.path.join(os.path.dirname(__file__), "assets", "leaderboards")
    
    def __init__(self, map):
        """
        Args
        ----
        map: int
            The map to use by index.
        """
        self.map = map
        self.leaderboard_path = os.path.join(self.base_path, f"leaderboard-map{map}.csv")
        
        if os.path.exists(self.leaderboard_path):
            self.leaderboard = pandas.read_csv(self.leaderboard_path)
        else:
            self.leaderboard = pandas.DataFrame(columns=["name", "score"])
            self.leaderboard.to_csv(self.leaderboard_path, index=False)
    
    def _sort_leaderboard(self):
        self.leaderboard.sort_values(by="score", ascending=False, inplace=True)

        # Remove duplicate entries
        self.leaderboard.drop_duplicates(subset=["name"], keep="first", inplace=True)

    def add_score(self, players):
        """
        Save the RacingTrainers score to the leaderboard.
        """
        for player in players:
            self.leaderboard = self.leaderboard.append({"name": player.name, "score": player.score}, ignore_index=True)
            self._sort_leaderboard()
            self.leaderboard.to_csv(self.leaderboard_path, index=False)


if __name__ == "__main__":
    ldb = LeaderboardHandler(1)
    print(ldb.leaderboard)

    class TestTrainer:
        def __init__(self, name, score):
            self.name, self.score = name, score

    players = [TestTrainer("test1", 5), TestTrainer("test2", 2), TestTrainer("test3", 3)]

    ldb.add_score(players)

    print(ldb.leaderboard)
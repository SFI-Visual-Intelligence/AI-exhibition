#!/usr/bin/env python3

import os
import pandas as pd
from argparse import ArgumentParser

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

        # Set path to leaderboard
        self.leaderboard_path = os.path.join(self.base_path, f"leaderboard-map{map}.csv")
        
        # Load leaderboard if it exists
        if os.path.exists(self.leaderboard_path):
            self.leaderboard = pd.read_csv(self.leaderboard_path)

        # If not, create leaderboard
        else:
            self.leaderboard = pd.DataFrame(columns=["name", "score"])
            self.leaderboard.to_csv(self.leaderboard_path, index=False)
    
    def _sort_leaderboard(self):
        """
        Private method to sort the leaderboard. Will also ensure only one score is stored per player.

        This however can lead to some problems if different people have the same name and the first to register a player on the name gets a high score, then the leaderboard wont update the new players score as training a new model only will replace the old one.
        """

        self.leaderboard.sort_values(by="score", ascending=False, inplace=True)

        # Remove duplicate entries
        self.leaderboard.drop_duplicates(subset=["name"], keep="first", inplace=True)

    def add_score(self, players):
        """
        Save the RacingTrainers score to the leaderboard.

        Args
        ----
        players: list of RacingTrainer
            The players to add to the leaderboard.
        """

        player_scores = {"name":[], "score":[]}

        for player in players:
            player_scores["name"].append(player.name)
            player_scores["score"].append(player.score)

        player_scores = pd.DataFrame(player_scores)
        
        self.leaderboard = pd.concat((self.leaderboard, player_scores), ignore_index=True)
        self._sort_leaderboard()
        self.leaderboard.to_csv(self.leaderboard_path, index=False)

def test_leaderboard(test_map):
    """
    Test the leaderboard by making some artificial entries.
    """

    ldb = LeaderboardHandler(test_map)
    print(ldb.leaderboard)

    class TestTrainer:
        def __init__(self, name, score):
            self.name, self.score = name, score

    players = [TestTrainer("test1", 5), TestTrainer("test2", 9), TestTrainer("test3", 16)]

    ldb.add_score(players)

    print(ldb.leaderboard)

if __name__ == "__main__":
    parser = ArgumentParser(description="See the leaderboard")
    parser.add_argument(
        "map",
        type=int,
        choices=range(1, 6),
        help="The map to show the leaderboard for."
    )
    parser.add_argument(
        "-t",
        "--test",
        action="store_true",
        help="Test the leaderboard."
    )

    args = parser.parse_args()

    if args.test:
        test_leaderboard(args.map)
    
    leaderboard = LeaderboardHandler(args.map)
    print(leaderboard.leaderboard)


class GameStats:

    """This class tracks the statistics of the game. """

    def __init__(self, ai_game):
        """Initialize the statistics."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.reset_stats()


        #Start the Alien invasion in an active state.
        self.game_active = False

        #High scores should never be reset.
        self.high_score = 0


    def reset_stats(self):
        """Initialize the statistics that can change during the game. """
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1







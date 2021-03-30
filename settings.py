import  pygame

class Settings:
    """this is a class to store all settings for Alien Invasion"""

    def __init__(self):
        """Initialize the game's settings"""
        #Screen Settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230,230,230)

        #Ship Settings

        self.ship_limit = 3

        ##Bullet settings

        self.bullet_width = 15
        self.bullet_height = 4
        self.bullet_color = (60,60,60)
        self.bullets_allowed = 4


        #Alien speed settings

        self.fleet_drop_speed = 10


        #How quickly the game speeds up
        self.speed_scale = 1.1

        #How quickly the alien point values increases
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize the game settings that change throughout the year. """
        self.ship_speed = 1.5
        self.bullet_speed = 3.0
        self.alien_speed = 1.0

        # Fleet direction of 1 represents right and -1 represents left.
        self.fleet_direction = 1

        #Scoring
        self.alien_points = 50

    def increase_speed(self):
        """Increase speed settings."""
        self.ship_speed *= self.speed_scale
        self.bullet_speed *= self.speed_scale
        self.alien_speed *= self.speed_scale

        self.alien_points = int(self.alien_points * self.score_scale)









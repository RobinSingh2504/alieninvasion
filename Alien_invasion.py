import sys       ## Exit the game when the player quits

from time import sleep

import pygame    ##Functionality to create the game

from settings import Settings

from game_stats import GameStats

from ship import Ship

from bullet import Bullet

from alien import Alien

from button import Button

from scoreboard import Scoreboard

class AlienInvasion:
    """This is the class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game and create game resources. """
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)  ##inherent display function in package 'pygame'
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height

        pygame.display.set_caption("Alien Invasion")    ##within display, multiple functions including set.mode and set.caption.

        self.stats = GameStats(self) # Create an instance to store game statistics.
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group() # A sprite group is a collection of sprites that can act all at the same time.
        self._create_fleet()


        #Make the play button
        self.play_button = Button(self, "Click to Play")


    def _ship_hit(self):
        """Respond to the ship being hit by an alien. """
        if self.stats.ships_left > 0:

            #Decrenebt Ships left.
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            #Get rid of any remaining aliens and bullets.
            self.aliens.empty()
            self.bullets.empty()

            #Create a new fleet and recenter the ship.
            self._create_fleet()
            self.ship.center_ship()

            #pause before recreating and regrouping the alien.
            sleep(0.5) #pausing the program for half a second.

        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _create_fleet(self):
        """Create a fleet of aliens. """
        #Make an alien.
        #Spacing between each alien is equal to one alien width.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_of_aliens =  available_space_x // (2 * alien_width)

        #Determine the number of rows of aliens that fit on the screen.
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_of_rows = available_space_y // (2*alien_height)


        for row_number in range(number_of_rows):
            # Create the first row of aliens.
            for alien_number in range(number_of_aliens):
                #Create an alien and place it in the row.
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """Create an alien and place it in the row."""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien._check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction. """
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def run_game(self):
        """Start the main loop of the game."""
        while True:
            # Watch out for keyboard and mouse events.
            self._check_events()  #Redraw the screen during each pass through the loop
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            self._update_screen()

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():   # an event is an action that the user performs while playing the game, such as pressing a key.
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()   ## this function gets the position (tuple) containing the x,y coordinates when the mouse button is  clicked.
                self._check_play_button(mouse_pos)   # Send these values to the new function _check_play_button.


    def _check_play_button(self, mouse_pos):
        #Start a new game when the player clicks Play.
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:  ##Check if the method collidepoint : point of the mouse click overlaps the region defined by the Play button's rectangle.
            #Reset the game statistics.
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()

            #Get rid of the remaining aliens and bullets
            self.aliens.empty()
            self.bullets.empty()

            #Create a new fleet of aliens and center the ship.
            self._create_fleet()
            self.ship.center_ship

            #Hide the mouse cursor.
            pygame.mouse.set_visible(False)

    """def _start_game(self):
        # Reset the game statistics.
        self.stats.reset_stats()
        self.stats.game_active = True

        # Get rid of the remaining aliens and bullets
        self.aliens.empty()
        self.bullets.empty()

        # Create a new fleet of aliens and center the ship.
        self._create_fleet()
        self.ship.center_ship"""


    def _check_keydown_events(self, event):
        """Respond to keypresses"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        """elif event.key == pygame.K_p:
            self._check_play_button()
            self._start_game()"""


    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right=False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet=Bullet(self)
            self.bullets.add(new_bullet)   ## add is similar to append method

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        #Update bullet positions.
        self.bullets.update()

        # Get rid of the bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
    # print(len(self.bullets)) - Tells whether the number of bullets have decreased. This will slow as it tells keeps the processor running on the count of the bullets deleted.

            self._check_bullet_alien_collisions()
    def _check_bullet_alien_collisions(self):
        """ Check for any bullets that have hit the aliens. """
        """If so, het rid of the bullets and the alien. """
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()


        if not self.aliens:
            # Destroy the existing bullets and create a new fleet.
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            #Increase Level
            self.stats.level +=1
            self.sb.prep_level()

    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen. """
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
            #treat this as if the ship got hit
                self._ship_hit()
                break

    def _update_aliens(self):
        """Check if the fleet is at an edge.
        then update the position of all aliens in the fleet. """
        self._check_fleet_edges()
        """Update the position of aliens in the fleet."""
        self.aliens.update()

        #Look for alien-ship collisions.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        #look for aliens to hit the bottom of the screen.
        self._check_aliens_bottom()

    def _update_screen(self):  ##updating the images on the screen and flip to the new screen.
        self.screen.fill(self.settings.bg_color)    ##fill method in the object self.screen which acts on a surface and takes only one argument color

        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        # Draw the score information.
        self.sb.show_score()

        #Draw the play button if the game is inactive.
        if not self.stats.game_active:
            self.play_button.draw_button()

            #Make the most recently drawn screen visible.
        pygame.display.flip()     ## This tells Pygame to make the most recently drawn screen visible.
# It simply draws the an empty screen on each pass through the while loop, erasing the old screen so only new screen is visible.

if __name__ == '__main__':
    #Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()
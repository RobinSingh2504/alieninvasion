import pygame.font  ##Pygame render a text on the screen.

class Button:

    def __init__(self, ai_game, msg):
        """Initialize the button assets. """
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        #set the dimensions and properties of the button.

        self.width, self.height = 200, 50
        self.button_color = (0,255,0)
        self.text_color = (255,255,255)
        self.font = pygame.font.SysFont(None, 48)  ##font attribute for rendering the text. None means use - default font. 48 - size of the text.

        #Build the button's rect object and center it.
        self.rect = pygame.Rect(0,0,self.width,self.height)
        self.rect.center = self.screen_rect.center

        #The button message needs to be prepped only once.
        self._prep_msg(msg)   #Pygame works with text by rendering the string you want to display as an image.

    def _prep_msg(self, msg):
        """Turn the message into a rendered image and center the text on the button"""
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)   ##boolean value to turn the antialiasing on or off. Anti-aliasing means the edges of the text smoother.
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):

        #Draw a blank button and then draw the message.
        self.screen.fill(self.button_color, self.rect)   #screen.fill to draw the rectangle portion of the button.
        self.screen.blit(self.msg_image, self.msg_image_rect)   #screen.blit to draw the text image to the screen., passing it an image and the rect object associated with an image.
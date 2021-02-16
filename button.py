import pygame


class Button:
    def __init__(self, screen, x, y, width, height, text, font,
                 main_col="#FFFFFF", font_col="#111111"):
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.font = font
        self.font_col = font_col
        self.main_col = main_col

        self.button = pygame.Rect(self.x, self.y, self.width, self.height)

    def update(self):
        pygame.draw.rect(self.screen, pygame.Color(self.main_col), self.button)

        self.render_text()

    def collide(self, *pos):
        if self.button.collidepoint(pos):
            return True

    def render_text(self):
        text = self.font.render(self.text, 1, pygame.Color(self.font_col))
        text_rect = text.get_rect()
        text_rect.center = (self.x + self.width * 0.5,
                            self.y + self.height * 0.5)
        self.screen.blit(text, text_rect)

    def set_text(self, text):
        self.text = text

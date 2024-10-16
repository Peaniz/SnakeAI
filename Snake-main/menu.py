import pygame
import sys
from scoreboard import show_scoreboard  # Import the show_scoreboard function

pygame.init()

# Set the resolution to match main.py's resolution
SCREEN = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Menu")

# Load and scale the background image to cover the entire screen
BG = pygame.image.load('assets/Background.png')
BG = pygame.transform.scale(BG, (800, 800))

class Menu_Button():
    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False

    def changeColor(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)

def get_font(size):
    return pygame.font.Font("assets/font.ttf", size)

def play():
    return 'playing'

def options():
    global selected_algorithm  # Biến toàn cục để lưu thuật toán đã chọn

    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.fill("white")

        # Tiêu đề
        OPTIONS_TEXT = get_font(45).render("Select "
                                           "Search Algorithm", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(400, 100))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        # Radio Button - BFS
        BFS_BUTTON = Menu_Button(image=None, pos=(400, 300),
                                 text_input="BFS MODE", font=get_font(40),
                                 base_color="Black", hovering_color="Green")
        BFS_BUTTON.changeColor(OPTIONS_MOUSE_POS)
        BFS_BUTTON.update(SCREEN)

        # Radio Button - A* Search
        A_STAR_BUTTON = Menu_Button(image=None, pos=(400, 400),
                                    text_input="A* SEARCH MODE", font=get_font(40),
                                    base_color="Black", hovering_color="Green")
        A_STAR_BUTTON.changeColor(OPTIONS_MOUSE_POS)
        A_STAR_BUTTON.update(SCREEN)

        # Nút Back
        OPTIONS_BACK = Menu_Button(image=None, pos=(400, 500),
                                   text_input="BACK", font=get_font(75),
                                   base_color="Black", hovering_color="Green")
        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if BFS_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                    selected_algorithm = 'bfs'
                    print("Thuật toán đã chọn: BFS")  # Debug

                if A_STAR_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                    selected_algorithm = 'a_star'
                    print("Thuật toán đã chọn: A*")  # Debug

                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    return  # Quay về menu chính

        pygame.display.update()



def main_menu(db, game_state):
    while game_state == 'menu':
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(75).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(400, 100))

        PLAY_BUTTON = Menu_Button(image=pygame.image.load("assets/Play Rect.png"), pos=(400, 250), 
                        text_input="PLAY", font=get_font(40), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Menu_Button(image=pygame.image.load("assets/Options Rect.png"), pos=(400, 400), 
                            text_input="OPTIONS", font=get_font(40), base_color="#d7fcd4", hovering_color="White")
        SCOREBOARD_BUTTON = Menu_Button(image=pygame.image.load("assets/Options Rect.png"), pos=(400, 550), 
                            text_input="SCOREBOARD", font=get_font(40), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Menu_Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(400, 700), 
                            text_input="QUIT", font=get_font(40), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, SCOREBOARD_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    return play()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if SCOREBOARD_BUTTON.checkForInput(MENU_MOUSE_POS):
                    show_scoreboard(db, SCREEN, 20, 40)  # Show the scoreboard
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
    return game_state

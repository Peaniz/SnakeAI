import pygame,sys,random
from pygame.math import Vector2
from collections import deque
from pleier import PLAYER
from freeit import FRUIT
from sinake import SNAKE




class MAIN:
	def __init__(self):
		self.snake = SNAKE()
		self.player = PLAYER()
		self.fruit = FRUIT()

	def update(self):
		self.snake.move_snake(self.fruit.pos, self.player.body, cell_number)
		self.player.move_snake()
		self.check_collision()
		self.check_fail()

	def draw_elements(self):
		self.draw_grass()
		self.fruit.draw_fruit(screen, apple, cell_size)
		self.snake.draw_snake(screen, cell_size)
		self.player.draw_snake(screen, cell_size)
		self.draw_score()

	def check_collision(self):
		if self.fruit.pos == self.snake.body[0]:
			self.fruit.randomize(cell_number)
			self.snake.add_block()
			self.snake.play_crunch_sound()

		for block in self.snake.body[1:]:
			if block == self.fruit.pos:
				self.fruit.randomize(cell_number)

		if self.fruit.pos == self.player.body[0]:
			self.fruit.randomize(cell_number)
			self.player.add_block()
			self.player.play_crunch_sound()

		for block in self.player.body[1:]:
			if block == self.fruit.pos:
				self.fruit.randomize(cell_number)

	def check_fail(self):
		if not 0 <= self.player.body[0].x < cell_number or not 0 <= self.player.body[0].y < cell_number:
			print("AI thang")
			self.game_over()
		
		if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
			print("Player thang")
			self.game_over()

		for block in self.player.body[1:]:
			if block == self.snake.body[0]:
				print("Player thang")
				self.game_over()
		
		for block in self.snake.body[1:]:
			if block == self.player.body[0]:
				print("AI thang")
				self.game_over()
		
	def game_over(self):
		self.snake.reset()
		self.player.reset()

	def draw_grass(self):
		grass_color = (167,209,61)
		for row in range(cell_number):
			if row % 2 == 0: 
				for col in range(cell_number):
					if col % 2 == 0:
						grass_rect = pygame.Rect(col * cell_size,row * cell_size,cell_size,cell_size)
						pygame.draw.rect(screen,grass_color,grass_rect)
			else:
				for col in range(cell_number):
					if col % 2 != 0:
						grass_rect = pygame.Rect(col * cell_size,row * cell_size,cell_size,cell_size)
						pygame.draw.rect(screen,grass_color,grass_rect)			

	def draw_score(self):
		score_text = str(len(self.player.body) - 3)
		score_surface = game_font.render(score_text,True,(56,74,12))
		score_x = int(cell_size * cell_number - 60)
		score_y = int(cell_size * cell_number - 40)
		score_rect = score_surface.get_rect(center = (score_x,score_y))
		apple_rect = apple.get_rect(midright = (score_rect.left,score_rect.centery))
		bg_rect = pygame.Rect(apple_rect.left,apple_rect.top,apple_rect.width + score_rect.width + 6,apple_rect.height)

		pygame.draw.rect(screen,(167,209,61),bg_rect)
		screen.blit(score_surface,score_rect)
		screen.blit(apple,apple_rect)
		pygame.draw.rect(screen,(56,74,12),bg_rect,2)

pygame.mixer.pre_init(44100,-16,2,512)
pygame.init()
cell_size = 40
cell_number = 20
screen = pygame.display.set_mode((cell_number * cell_size,cell_number * cell_size))
clock = pygame.time.Clock()
apple = pygame.image.load('Graphics/apple.png').convert_alpha()
game_font = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 25)

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE,100)

main_game = MAIN()

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == SCREEN_UPDATE:
			main_game.update()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP:
				if main_game.player.direction.y != 1:
					main_game.player.direction = Vector2(0,-1)
			if event.key == pygame.K_RIGHT:
				if main_game.player.direction.x != -1:
					main_game.player.direction = Vector2(1,0)
			if event.key == pygame.K_DOWN:
				if main_game.player.direction.y != -1:
					main_game.player.direction = Vector2(0,1)
			if event.key == pygame.K_LEFT:
				if main_game.player.direction.x != 1:
					main_game.player.direction = Vector2(-1,0)

	screen.fill((175,215,70))
	main_game.draw_elements()
	pygame.display.update()
	clock.tick(60)
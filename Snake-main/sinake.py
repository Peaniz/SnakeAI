import pygame
from pygame.math import Vector2
from collections import deque
import heapq

def heuristic(a, b):
    # Hàm heuristic sử dụng khoảng cách Manhattan
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star_search(snake_body, player_body, start, goal, grid_size):
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    open_list = []
    heapq.heappush(open_list, (0, start))
    came_from = {start: None}
    cost_so_far = {start: 0}

    while open_list:
        _, current = heapq.heappop(open_list)

        if current == goal:
            break

        for direction in directions:
            neighbor = (current[0] + direction[0], current[1] + direction[1])
            if (0 <= neighbor[0] < grid_size and 0 <= neighbor[1] < grid_size and
                neighbor not in snake_body and neighbor not in player_body):
                new_cost = cost_so_far[current] + 1  # Mỗi bước có chi phí bằng 1
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    priority = new_cost + heuristic(neighbor, goal)
                    heapq.heappush(open_list, (priority, neighbor))
                    came_from[neighbor] = current

    path = []
    if goal in came_from:
        current = goal
        while current != start:
            path.append(current)
            current = came_from[current]
        path.reverse()
    return path


def bfs(snake_body,player_body, start, goal, grid_size):
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  
    queue = deque([start])
    came_from = {start: None}
    visited = {start}

    while queue:
        current = queue.popleft()

        if current == goal:
            break

        for direction in directions:
            neighbor = (current[0] + direction[0], current[1] + direction[1])
            if (0 <= neighbor[0] < grid_size and 0 <= neighbor[1] < grid_size and 
                neighbor not in visited and neighbor not in snake_body and neighbor not in player_body):
                queue.append(neighbor)
                visited.add(neighbor)
                came_from[neighbor] = current

  
    path = []
    if goal in came_from:
        current = goal
        while current != start:
            path.append(current)
            current = came_from[current]
        path.reverse()  
    return path

class SNAKE:
    def __init__(self):
        self.body = [Vector2(15, 10), Vector2(14, 10), Vector2(13, 10)]
        self.direction = Vector2(0, 0)
        self.new_block = False

        # Load graphics for AI snake
        self.head_up = pygame.image.load('Graphics/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('Graphics/head_down.png').convert_alpha()
        self.head_right = pygame.image.load('Graphics/head_right.png').convert_alpha()
        self.head_left = pygame.image.load('Graphics/head_left.png').convert_alpha()

        self.tail_up = pygame.image.load('Graphics/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('Graphics/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load('Graphics/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load('Graphics/tail_left.png').convert_alpha()

        self.body_vertical = pygame.image.load('Graphics/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('Graphics/body_horizontal.png').convert_alpha()

        self.body_tr = pygame.image.load('Graphics/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load('Graphics/body_tl.png').convert_alpha()
        self.body_br = pygame.image.load('Graphics/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load('Graphics/body_bl.png').convert_alpha()

        self.crunch_sound = pygame.mixer.Sound('Sound/crunch.wav')

    def move_snake(self, fruit_pos, player_body, cell_number, selected_algorithm):

        snake_head = self.body[0]
        snake_body_set = set((block.x, block.y) for block in self.body[1:])
        player_body_set = set((block.x, block.y) for block in player_body)

        # Chọn thuật toán dựa trên lựa chọn của người dùng
        if selected_algorithm == 'a_star':
            path = a_star_search(snake_body_set, player_body_set,
                                 (snake_head.x, snake_head.y),
                                 (fruit_pos.x, fruit_pos.y),
                                 cell_number)
        else:  # BFS
            path = bfs(snake_body_set, player_body_set,
                       (snake_head.x, snake_head.y),
                       (fruit_pos.x, fruit_pos.y),
                       cell_number)

        if path:
            next_move = Vector2(path[0][0], path[0][1]) - snake_head
            if abs(next_move.x) <= 1 and abs(next_move.y) <= 1:
                self.direction = next_move

        if self.new_block:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]

    # def move_snake(self, fruit_pos, player_body, cell_number):
    #     snake_head = self.body[0]
    #     snake_body_set = set((block.x, block.y) for block in self.body[1:])
    #     player_body_set = set((block.x, block.y) for block in player_body)
    #     path = bfs(snake_body_set, player_body_set, (snake_head.x, snake_head.y), (fruit_pos.x, fruit_pos.y), cell_number)
    #
    #     if path:
    #         next_move = Vector2(path[0][0], path[0][1]) - snake_head
    #         if abs(next_move.x) <= 1 and abs(next_move.y) <= 1:
    #             self.direction = next_move
    #
    #     if self.new_block:
    #         body_copy = self.body[:]
    #         body_copy.insert(0, body_copy[0] + self.direction)
    #         self.body = body_copy[:]
    #         self.new_block = False
    #     else:
    #         body_copy = self.body[:-1]
    #         body_copy.insert(0, body_copy[0] + self.direction)
    #         self.body = body_copy[:]

    def draw_snake(self, screen, cell_size):
        self.update_head_graphics()
        self.update_tail_graphics()
        for index, block in enumerate(self.body):
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)

            if index == 0:
                screen.blit(self.head, block_rect)
            elif index == len(self.body) - 1:
                screen.blit(self.tail, block_rect)
            else:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical, block_rect)
                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal, block_rect)
                else:
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        screen.blit(self.body_tl, block_rect)
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        screen.blit(self.body_bl, block_rect)
                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        screen.blit(self.body_tr, block_rect)
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        screen.blit(self.body_br, block_rect)

    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1, 0): self.head = self.head_left
        elif head_relation == Vector2(-1, 0): self.head = self.head_right
        elif head_relation == Vector2(0, 1): self.head = self.head_up
        elif head_relation == Vector2(0, -1): self.head = self.head_down

    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1, 0): self.tail = self.tail_left
        elif tail_relation == Vector2(-1, 0): self.tail = self.tail_right
        elif tail_relation == Vector2(0, 1): self.tail = self.tail_up
        elif tail_relation == Vector2(0, -1): self.tail = self.tail_down

    def add_block(self):
        self.new_block = True

    def play_crunch_sound(self):
        self.crunch_sound.play()

    def reset(self):
        self.body = [Vector2(15, 10), Vector2(14, 10), Vector2(13, 10)]
        self.direction = Vector2(0, 0)

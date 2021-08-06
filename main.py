import pygame
import sys
from pygame.math import Vector2
from random import randint


class SNAKE:
    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(1, 0)

        self.head_img = pygame.image.load('graphics/snake_head.png')
        self.body_img = pygame.image.load('graphics/snake_body.png')
        self.tail_img = pygame.image.load('graphics/snake_tail.png')
        self.turn_img = pygame.image.load('graphics/snake_turn.png')

        self.head_up = pygame.transform.rotate(self.head_img, 180)
        self.head_down = pygame.transform.rotate(self.head_img, 0)
        self.head_left = pygame.transform.rotate(self.head_img, 270)
        self.head_right = pygame.transform.rotate(self.head_img, 90)

        self.body_vertical = pygame.transform.rotate(self.body_img, 0)
        self.body_horizontal = pygame.transform.rotate(self.body_img, 90)

        self.tail_up = pygame.transform.rotate(self.tail_img, 0)
        self.tail_down = pygame.transform.rotate(self.tail_img, 180)
        self.tail_right = pygame.transform.rotate(self.tail_img, 270)
        self.tail_left = pygame.transform.rotate(self.tail_img, 90)

        self.turn_vl = pygame.transform.rotate(self.turn_img, 270)
        self.turn_vr = pygame.transform.rotate(self.turn_img, 0)
        self.turn_hl = pygame.transform.rotate(self.turn_img, 90)
        self.turn_hr = pygame.transform.rotate(self.turn_img, 180)

        self.head = None
        self.tail = None
        self.turn = None

        self.crunch_sound = pygame.mixer.Sound('Sound/crunch.mp3')

    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()

        for index, block in enumerate(self.body):
            x_pos = block.x * cell_size
            y_pos = block.y * cell_size
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)

            if index == 0:
                screen.blit(self.head, block_rect)
            elif index == len(self.body) - 1:
                screen.blit(self.tail, block_rect)
            elif self.body[index - 1].x == self.body[index + 1].x:
                screen.blit(self.body_vertical, block_rect)
            elif self.body[index - 1].y == self.body[index + 1].y:
                screen.blit(self.body_horizontal, block_rect)
            else:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                if previous_block.x != next_block.x:
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        screen.blit(self.turn_vl, block_rect)
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        screen.blit(self.turn_vr, block_rect)
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        screen.blit(self.turn_hl, block_rect)
                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        screen.blit(self.turn_hr, block_rect)

    def move_snake(self):
        body_copy = self.body[:-1]
        body_copy.insert(0, body_copy[0] + self.direction)
        self.body = body_copy

    def add_block(self):
        if self.body[len(self.body) - 1].y == self.body[len(self.body) - 2].y and self.body[len(self.body) - 1].x < \
                self.body[len(self.body) - 2].x:
            self.body.append(self.body[len(self.body) - 1] + Vector2(-1, 0))
        if self.body[len(self.body) - 1].y == self.body[len(self.body) - 2].y and self.body[len(self.body) - 1].x > \
                self.body[len(self.body) - 2].x:
            self.body.append(self.body[len(self.body) - 1] + Vector2(1, 0))
        if self.body[len(self.body) - 1].x == self.body[len(self.body) - 2].x and self.body[len(self.body) - 1].y > \
                self.body[len(self.body) - 2].y:
            self.body.append(self.body[len(self.body) - 1] + Vector2(0, 1))
        if self.body[len(self.body) - 1].x == self.body[len(self.body) - 2].x and self.body[len(self.body) - 1].y < \
                self.body[len(self.body) - 2].y:
            self.body.append(self.body[len(self.body) - 1] + Vector2(0, -1))

    def update_head_graphics(self):
        if self.body[0].y < self.body[1].y:
            self.head = self.head_up
            self.tail = self.tail_up
        elif self.body[0].y > self.body[1].y:
            self.head = self.head_down
            self.tail = self.tail_down
        elif self.body[0].x > self.body[1].x:
            self.head = self.head_right
            self.tail = self.tail_right
        else:
            self.head = self.head_left
            self.tail = self.tail_left

    def update_tail_graphics(self):
        if self.body[len(self.body) - 2].y < self.body[len(self.body) - 1].y:
            self.tail = self.tail_up
        elif self.body[len(self.body) - 2].y > self.body[len(self.body) - 1].y:
            self.tail = self.tail_down
        elif self.body[len(self.body) - 2].x > self.body[len(self.body) - 1].x:
            self.tail = self.tail_right
        else:
            self.tail = self.tail_left

    def play_crunch_sound(self):
        self.crunch_sound.play()

    def reset(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(1, 0)


class FRUIT:
    def __init__(self):
        self.x = randint(0, cell_number - 1)
        self.y = randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)

    def draw_fruit(self):
        fruit_rect = pygame.Rect(self.pos.x * cell_size, self.pos.y * cell_size, cell_size, cell_size)
        screen.blit(apple, fruit_rect)

    def randomize(self):
        self.x = randint(0, cell_number - 1)
        self.y = randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)


class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()

    def draw_elements(self):
        self.draw_grass()
        self.snake.draw_snake()
        self.fruit.draw_fruit()
        self.draw_score()

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()
            self.snake.play_crunch_sound()

        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomize()

    def check_fail(self):
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.game_over()

        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

    def draw_grass(self):
        grass_color = (167, 209, 61)

        for col in range(cell_number):
            for row in range(cell_number):
                if row % 2 == 0:
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)
                else:
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)

    def draw_score(self):
        score_text = str(len(self.snake.body) - 3)
        score_surface = game_score_font.render(score_text, True, (56, 75, 12))
        score_x = cell_size * cell_number - 60
        score_y = cell_size * cell_number - 40
        score_rect = score_surface.get_rect(center=(score_x, score_y))
        apple_rect = apple.get_rect(midright=(score_rect.left, score_rect.centery))
        bg_rect = pygame.Rect(apple_rect.left, apple_rect.top, apple_rect.width + score_rect.width + 5,
                              apple_rect.height)

        pygame.draw.rect(screen, (255, 167, 9), bg_rect)
        screen.blit(score_surface, score_rect)
        screen.blit(apple, apple_rect)
        pygame.draw.rect(screen, (64, 64, 64), bg_rect, 3)

    def game_over(self):
        global game_over

        game_over = True

    def game_restart(self):
        game_over_surface = game_over_font.render('Game Over', True, (56, 75, 12))
        game_over_x = cell_size * (cell_number // 2)
        game_over_y = cell_size * (cell_number // 4)
        game_over_rect = game_over_surface.get_rect(center=(game_over_x, game_over_y))

        game_restart_surface = game_restart_font.render('Press R to restart', True, (56, 75, 12))
        game_restart_x = cell_size * (cell_number // 2)
        game_restart_y = cell_size * (cell_number // 1.5)
        game_restart_rect = game_restart_surface.get_rect(center=(game_restart_x, game_restart_y))

        screen.blit(game_over_surface, game_over_rect)
        screen.blit(game_restart_surface, game_restart_rect)


# pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
cell_size = 40
cell_number = 20
clock = pygame.time.Clock()
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
apple = pygame.image.load('Graphics/apple.png').convert_alpha()
game_score_font = pygame.font.Font('Font/Bubblegum.ttf', 35)
game_over_font = pygame.font.Font('Font/Bubblegum.ttf', 100)
game_restart_font = pygame.font.Font('Font/Pacho DEMO.ttf', 75)

icon = pygame.image.load('Images/icon_snake.png')
pygame.display.set_icon(icon)
pygame.display.set_caption('Snake Game')

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

main_game = MAIN()

delay_flag = False
start_time = pygame.time.get_ticks()

game_over = False

while True:
    if not game_over:
        if not delay_flag:
            start_time = pygame.time.get_ticks()
            delay_flag = True
        # !!!
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == SCREEN_UPDATE:
                main_game.update()
            if event.type == pygame.KEYDOWN:
                if delay_flag and pygame.time.get_ticks() - start_time >= 100:  # !!!
                    delay_flag = False
                if event.key == pygame.K_UP and not delay_flag:  # !!!
                    if main_game.snake.direction.y != 1:
                        main_game.snake.direction = Vector2(0, -1)
                if event.key == pygame.K_DOWN and not delay_flag:  # !!!
                    if main_game.snake.direction.y != -1:
                        main_game.snake.direction = Vector2(0, 1)
                if event.key == pygame.K_LEFT and not delay_flag:  # !!!
                    if main_game.snake.direction.x != 1:
                        main_game.snake.direction = Vector2(-1, 0)
                if event.key == pygame.K_RIGHT and not delay_flag:  # !!!
                    if main_game.snake.direction.x != -1:
                        main_game.snake.direction = Vector2(1, 0)

        screen.fill((160, 201, 61))
        main_game.draw_elements()
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    main_game.snake.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
                    main_game.snake.direction = Vector2(1, 0)
                    game_over = False

        screen.fill((160, 201, 61))
        main_game.draw_grass()
        main_game.draw_score()
        main_game.game_restart()
    pygame.display.update()
    clock.tick(60)

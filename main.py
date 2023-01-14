import pygame
from random import randint

pygame.init()

WIDTH = 300
HEIGHT = 300

screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Pong Reboot')

timer = pygame.time.Clock()
framerate = 60
black = (0, 0, 0)
white = (255, 255, 255)
game_over = False
font = pygame.font.SysFont('arial', 22)

player_y = 130
computer_y = 130
ball_x = 145
ball_y = 145
player_direction = 0
player_speed = 5
ball_x_direction = 1
ball_y_direction = 1
ball_speed = 2
ball_y_speed = 2
score = 0
ball_color = white


def update_ai(ball_y, computer_y):
    computer_speed = 3
    if computer_y + 15 > ball_y + 5:
        computer_y -= computer_speed
    elif computer_y + 15 < ball_y + 5:
        computer_y += computer_speed
    return computer_y


def check_collisions(ball, player, computer, ball_x_direction, score):
    global ball_color
    if ball.colliderect(player) and ball_x_direction == -1:
        ball_x_direction = 1
        score += 1
        ball_color = (randint(1, 255), randint(0, 255), randint(0, 255))
    elif ball.colliderect(computer) and ball_x_direction == 1:
        ball_x_direction = -1
        score += 1
    return ball_x_direction, score, ball_color


def update_ball(ball_x_direction, ball_y_direction, ball_x, ball_y, ball_speed, ball_y_speed):
    if ball_x_direction == 1 and ball_x < 290:
        ball_x += ball_speed
    elif ball_x_direction == 1 and ball_x >= 290:
        ball_x_direction *= -1
    if ball_x_direction == -1 and ball_x > 0:
        ball_x -= ball_speed
    elif ball_x_direction == -1 and ball_x <= 0:
        ball_x_direction *= -1

    if ball_y_direction == 1 and ball_y < 290:
        ball_y += ball_y_speed
    elif ball_y_direction == 1 and ball_y >= 290:
        ball_y_direction *= -1
    if ball_y_direction == -1 and ball_y > 0:
        ball_y -= ball_y_speed
    elif ball_y_direction == -1 and ball_y <= 0:
        ball_y_direction *= -1

    return ball_x_direction, ball_y_direction, ball_x, ball_y


def check_game_over(ball_x, game_over):
    if (ball_x <= 0 or ball_x >= 290) and game_over == False:
        game_over = True

    return game_over


running = True
while running:
    timer.tick(framerate)
    screen.fill(black)
    game_over = check_game_over(ball_x, game_over)
    player = pygame.draw.rect(screen, white, [5, player_y, 10, 40])
    computer = pygame.draw.rect(screen, white, [285, computer_y, 10, 40])
    ball = pygame.draw.rect(screen, ball_color, [ball_x, ball_y, 10, 10])
    score_text = font.render(f'Score: {score}', True, white, black)
    screen.blit(score_text, (99, 10))

    if not game_over:
        computer_y = update_ai(ball_y, computer_y)
        ball_x_direction, ball_y_direction, ball_x, ball_y = update_ball(ball_x_direction, ball_y_direction,
                                                                         ball_x, ball_y, ball_speed, ball_y_speed)
    ball_x_direction, score, ball_color = check_collisions(ball, player, computer, ball_x_direction, score)

    if game_over:
        game_over_text = font.render('Game Over!', True, white, black)
        screen.blit(game_over_text, (83, 120))

        restart_button = pygame.draw.rect(screen, black, [62, 200, 100, 20])
        restart_text = font.render('Press to restart', True, white, black)
        screen.blit(restart_text, (68, 200))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                player_direction = -1
            if event.key == pygame.K_x:
                player_direction = 1
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                player_direction = 0
            if event.key == pygame.K_x:
                player_direction = 0
        if event.type == pygame.MOUSEBUTTONDOWN and game_over:
            if restart_button.collidepoint(event.pos):
                game_over = False
                player_y = 130
                computer_y = 130
                ball_x = 145
                ball_y = 145
                player_direction = 0
                player_speed = 5
                ball_x_direction = 1
                ball_y_direction = 1
                ball_speed = 2
                ball_y_speed = 2
                score = 0

    if 10 <= player_y <= HEIGHT - 40:
        player_y += player_speed * player_direction
    elif player_y > HEIGHT - 40:
        player_y = HEIGHT - 40
    elif player_y < 10:
        player_y = 10

    player_y += player_speed * player_direction
    ball_speed = 2 + (score//10)
    ball_y_speed = 2 + (score//15)

    pygame.display.flip()

pygame.quit()

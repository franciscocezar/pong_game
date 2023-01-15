import pygame
from random import randint


class Pong:
    def __init__(self):
        pygame.init()
        self.WIDTH = 300
        self.HEIGHT = 300
        self.screen = pygame.display.set_mode([self.WIDTH, self.HEIGHT])
        pygame.display.set_caption('Pong Reboot')
        self.font = pygame.font.SysFont('arial', 22)

        self.timer = pygame.time.Clock()
        self.framerate = 60
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.ball_color = self.white

        self.player_y = 130
        self.computer_y = 130
        self.ball_x = 145
        self.ball_y = 145
        self.player_direction = 0
        self.player_speed = 5
        self.ball_x_direction = 1
        self.ball_y_direction = 1
        self.ball_speed = 2
        self.ball_y_speed = 2
        self.score = 0
        self.game_over = False

        self.run()

    def update_ai(self, ball_y, computer_y):
        computer_speed = 3
        if computer_y + 15 > ball_y + 5:
            computer_y -= computer_speed
        elif computer_y + 15 < ball_y + 5:
            computer_y += computer_speed
        return computer_y

    def check_collisions(self, ball, player, computer, ball_x_direction, score):
        if ball.colliderect(player) and ball_x_direction == -1:
            ball_x_direction = 1
            score += 1
            self.ball_color = (randint(1, 255), randint(0, 255), randint(0, 255))
        elif ball.colliderect(computer) and ball_x_direction == 1:
            ball_x_direction = -1
            score += 1
        return ball_x_direction, score, self.ball_color

    def update_ball(self, ball_x_direction, ball_y_direction, ball_x, ball_y, ball_speed, ball_y_speed):
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

    def check_game_over(self, ball_x, game_over):
        if (ball_x <= 0 or ball_x >= 290) and not self.game_over:
            game_over = True
        return game_over

    def run(self):
        running = True
        while running:
            self.timer.tick(self.framerate)
            self.screen.fill(self.black)
            game_over = self.check_game_over(self.ball_x, self.game_over)
            player = pygame.draw.rect(self.screen, self.white, [5, self.player_y, 10, 40])
            computer = pygame.draw.rect(self.screen, self.white, [285, self.computer_y, 10, 40])
            ball = pygame.draw.rect(self.screen, self.ball_color, [self.ball_x, self.ball_y, 10, 10])
            score_text = self.font.render(f'Score: {self.score}', True, self.white, self.black)
            self.screen.blit(score_text, (99, 10))

            if not game_over:
                self.computer_y = self.update_ai(self.ball_y, self.computer_y)
                self.ball_x_direction, self.ball_y_direction, self.ball_x, \
                    self.ball_y = self.update_ball(self.ball_x_direction, self.ball_y_direction, self.ball_x,
                                                   self.ball_y, self.ball_speed, self.ball_y_speed)
                self.ball_x_direction, self.score, self.ball_color = \
                    self.check_collisions(ball, player, computer, self.ball_x_direction, self.score)

            if game_over:
                game_over_text = self.font.render('Game Over!', True, self.white, self.black)
                self.screen.blit(game_over_text, (83, 120))

                self.restart_button = pygame.draw.rect(self.screen, self.black, [62, 200, 100, 20])
                self.restart_text = self.font.render('Press to restart', True, self.white, self.black)
                self.screen.blit(self.restart_text, (68, 200))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        self.player_direction = -1
                    if event.key == pygame.K_x:
                        self.player_direction = 1
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_w:
                        self.player_direction = 0
                    if event.key == pygame.K_x:
                        self.player_direction = 0
                if event.type == pygame.MOUSEBUTTONDOWN and game_over:
                    if self.restart_button.collidepoint(event.pos):
                        self.game_over = False
                        self.player_y = 130
                        self.computer_y = 130
                        self.ball_x = 145
                        self.ball_y = 145
                        self.player_direction = 0
                        self.player_speed = 5
                        self.ball_x_direction = 1
                        self.ball_y_direction = 1
                        self.ball_speed = 2
                        self.ball_y_speed = 2
                        self.score = 0

            if 10 <= self.player_y <= self.HEIGHT - 40:
                self.player_y += self.player_speed * self.player_direction
            elif self.player_y > self.HEIGHT - 40:
                self.player_y = self.HEIGHT - 40
            elif self.player_y < 10:
                self.player_y = 10

            self.player_y += self.player_speed * self.player_direction
            self.ball_speed = 2 + (self.score // 10)
            self.ball_y_speed = 2 + (self.score // 15)

            pygame.display.flip()


if __name__ == '__main__':
    game = Pong()


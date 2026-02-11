import pygame, random

from .powerup import PowerUp
from game import ball, paddle, brick
from game.settings import *


class BreakoutGame:
    """
    Main game controller class.
    Handles object creation, score, rendering, and game loop utilities.
    """

    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Breakout")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)
        self.hit_sound = pygame.mixer.Sound(hit_path)
        self.break_sound = pygame.mixer.Sound(break_path)
        self.state = "waiting"
        self.score = 0
        self.ball_in_motion = False
        self.paddle_powerup_active = False
        self.powerups = []
        self.extra_balls = []
    
    def create_paddle(self):
        # Calculate paddle position (centered horizontally, near bottom)
        px = (SCREEN_WIDTH // 2 - PADDLE_WIDTH // 2)
        py = (SCREEN_HEIGHT - 15)
    
        self.paddle = paddle.Paddle(px, py, PADDLE_WIDTH, PADDLE_HEIGHT, PADDLE_SPEED)
    
    def create_ball(self):
        # Spawn ball directly above the paddle before launch
        bx = (SCREEN_WIDTH // 2 - BALL_RADIUS // 2)
        by = (SCREEN_HEIGHT - 20 - PADDLE_HEIGHT)

        self.ball = ball.Ball(bx, by, BALL_RADIUS, BALL_RADIUS, BALL_SPEED, BALL_ACCELERATION)

    def create_bricks(self, rows, cols):

        """
        Create a grid of bricks based on given rows and columns.
        Each brick type is chosen randomly from BRICK_RULES.
        """

        self.bricks = []
        start_x = BREAK_WIDTH
        start_y = BREAK_WIDTH
        gap = 5

        # create a grid of bricks
        for row in range(rows):
            for col in range(cols):
                x = start_x + col * (BREAK_WIDTH + gap)
                y = start_y + row * (BREAK_HEIGHT + gap)

                brick_type = random.choice(list(BRICK_RULES.keys()))
                new_brick = brick.Brick(x, y, BREAK_WIDTH, BREAK_HEIGHT, BRICK_RULES[brick_type])

                self.bricks.append(new_brick)
    
    def spawn_powerup(self, x, y, type_):
        powerup = PowerUp(x, y, ITEM_WIDTH, ITEM_HEIGHT, type_, ITEM_SPEED, ITEM_COLOR)
        self.powerups.append(powerup)

    def active_powerup(self, type_):
        if type_ == 'triple':
            self.spawn_extra_balls(3)

        elif type_ == 'double':
            self.spawn_extra_balls(2)

        elif type_ == 'big_paddle':
            self.big_paddle()

    def big_paddle(self):
        self.paddle.rect.width = int(PADDLE_WIDTH * 1.5)
        if not self.paddle_powerup_active:
            self.paddle_powerup_active = True
            self.paddle_powerup_end_time = pygame.time.get_ticks() + 10000
        else:
            self.paddle_powerup_end_time += 10000

    def spawn_extra_balls(self, count):
        for _ in range(count):
            new_ball = ball.Ball(
                self.ball.rect.x,
                self.ball.rect.y,
                BALL_RADIUS,
                BALL_RADIUS,
                BALL_SPEED,
                acceleration=0,
                simulated=True
            )
            
            new_ball.dx = random.choice([-1, 1])
            new_ball.dy = -1
            self.extra_balls.append(new_ball)

    def checking_powerup_time(self):
        current_time = pygame.time.get_ticks()
        if self.paddle_powerup_active and current_time >= self.paddle_powerup_end_time:
            self.paddle.rect.width = PADDLE_WIDTH
            self.paddle_powerup_active = False

    def show_start_message(self):
        """Display start-game message and wait for start"""
        text = self.font.render('Press SPACE To Start', True, WAITING_TEXT_COLOR)
        px = (SCREEN_WIDTH // 2 - text.get_width() // 2)
        py = (SCREEN_HEIGHT // 2 - text.get_height() // 2)
        self.screen.blit(text, (px, py))

    def show_end_message(self):
        """Display end-game message and wait for restart/quit."""
        if self.state == "win":
            text = self.font.render("YOU WIN(R to Restart or Q for Quit)", True, WIN_TEXT_COLOR)
        elif self.state == "game_over":
            text = self.font.render("GAME OVER(R to Restart or Q for Quit)", True, GAME_OVER_TEXT_COLOR)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

        self.screen.blit(text, text_rect)
        pygame.display.flip()

    def add_score(self, score):
        # Increase total score after destroying a brick
        self.score += score

    def show_score(self):
        # Render score text in top-left corner
        score_text = self.font.render(f'Score: {self.score}', True, FONT_COLOR)
        self.screen.blit(score_text, (10, 10))

    def is_game_over(self):
        # Ball has fallen below the screen → game over
        if self.ball.rect.top >= SCREEN_HEIGHT:
            self.state = "game_over"
            return True
        return False

    def is_win(self):
        if not self.bricks:
            self.state = "win"
            return True
        return False

    def wait_for_restart(self):
        """Wait for player to press R to restart or Q to quit."""
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        return "restart"
                    if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                        return "quit"

    def run(self):
        """
        Main game loop.
        Handles input, updates game objects, checks win/lose conditions,
        renders everything, and returns 'restart' or 'quit'.
        """

        self.create_ball()
        self.create_paddle()
        self.create_bricks(3, 8)

        running = True

        while running:

            # --- Input handling ---
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.ball_in_motion = True
                        self.state = "playing"

            # --- Update paddle ---
            self.paddle.handle_input()
            self.paddle.update(SCREEN_WIDTH)

            if self.ball_in_motion:
                # --- Update item ---
                for p in self.powerups:
                    p.move()
                    if p.check_collision(self.paddle):
                        self.active_powerup(p.type)
                        self.powerups.remove(p)

                self.powerups = [p for p in self.powerups if p.rect.y <= SCREEN_HEIGHT]

                # --- Update ball ---
                self.ball.move()
                self.ball.update(SCREEN_WIDTH, self.paddle)
            
                # -- Brick collisions --
                for br in self.bricks:
                    if br.alive and self.ball.rect.colliderect(br.rect):
                        self.ball.handle_brick_collision(br)
                        br.take_damage()
                        item = br.drop_item()

                        if item:
                            self.break_sound.play()
                            self.add_score(br.score)
                            if item is not True:
                                self.spawn_powerup(br.rect.centerx, br.rect.centery, item)
                        else:
                            self.hit_sound.play()
                        break

                # --- Update extra balls ---
                for b in self.extra_balls:
                    b.move()
                    b.update(SCREEN_WIDTH, self.paddle)

                self.extra_balls = [b for b in self.extra_balls if b.rect.top < SCREEN_HEIGHT]

                # -- extra balls collision with brick --
                for extra in self.extra_balls:
                    for br in self.bricks:
                        if br.alive and extra.rect.colliderect(br.rect):
                            extra.handle_brick_collision(br)
                            br.take_damage()
                            item = br.drop_item()

                            if item:
                                self.break_sound.play()
                                self.add_score(br.score)
                                if item is not True:
                                    self.spawn_powerup(br.rect.centerx, br.rect.centery, item)
                            else:
                                self.hit_sound.play()
                            break

                # delete destroyed bricks
                self.bricks = [b for b in self.bricks if b.alive]

            # --- Rendering ---
            
            self.screen.fill('black')
            self.paddle.draw(self.screen, PADDLE_COLOR)
            self.ball.draw(self.screen, BALL_COLOR)

            for b in self.extra_balls:
                b.draw(self.screen, SIMULATED_BALL_COLOR)

            for p in self.powerups:
                p.draw(self.screen)

            for b in self.bricks:
                if b.alive:
                    b.draw(self.screen)

            if self.state == "waiting":
                self.show_start_message()

            self.checking_powerup_time()
            self.show_score()
            self.clock.tick(60)
            pygame.display.flip()

            # --- Win check ---
            if self.is_win():
                self.show_end_message()
                choice = self.wait_for_restart()

                if choice == "restart":
                    return True
                else:
                    return False

            # --- Game over check ---
            if self.is_game_over():
                self.show_end_message()
                choice = self.wait_for_restart()

                if choice == "restart":
                    return True
                else:
                    return False